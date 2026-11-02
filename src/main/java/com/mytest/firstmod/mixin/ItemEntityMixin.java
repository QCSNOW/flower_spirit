package com.mytest.firstmod.mixin;

import com.mytest.firstmod.storage.BagStorage;
import com.mytest.firstmod.item.FlowerBagItem;
import com.mytest.firstmod.screen.FlowerBagScreenHandler;
import com.mytest.firstmod.item.ModItems;
import net.minecraft.entity.ItemEntity;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.registry.tag.ItemTags;
import net.minecraft.server.network.ServerPlayerEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

import java.util.UUID;

@SuppressWarnings("all")
@Mixin(ItemEntity.class)
public abstract class ItemEntityMixin {

    @Shadow private int pickupDelay;

    @Inject(method = "onPlayerCollision", at = @At("HEAD"), cancellable = true)
    private void onPlayerCollision(PlayerEntity player, CallbackInfo ci) {
        ItemEntity itemEntity = (ItemEntity) (Object) this;
        ItemStack itemStack = itemEntity.getStack();

        // ===== 步骤1：完全复刻原版所有前置条件 =====
        if (itemEntity.getWorld().isClient()) return;
        if (itemStack.isEmpty()) return;
        if (this.pickupDelay > 0) return;
        if (!itemStack.isIn(ItemTags.FLOWERS)) return;
        if (!(player instanceof ServerPlayerEntity serverPlayer)) return;

        // ===== 步骤2：按顺序检查袋子，计算总共能吸入多少 =====
        int totalSucked = 0;

        // 快捷栏
        for (int i = 0; i <= 8; i++) {
            ItemStack bagStack = player.getInventory().getStack(i);
            if (bagStack.getItem() == ModItems.FLOWER_BAG) {
                totalSucked += trySuckIntoBag(serverPlayer, bagStack, itemStack, totalSucked);
                if (totalSucked >= itemStack.getCount()) break;
            }
        }
        // 主背包
        if (totalSucked < itemStack.getCount()) {
            for (int i = 9; i <= 35; i++) {
                ItemStack bagStack = player.getInventory().getStack(i);
                if (bagStack.getItem() == ModItems.FLOWER_BAG) {
                    totalSucked += trySuckIntoBag(serverPlayer, bagStack, itemStack, totalSucked);
                    if (totalSucked >= itemStack.getCount()) break;
                }
            }
        }
        // 副手
        if (totalSucked < itemStack.getCount()) {
            ItemStack offHand = player.getOffHandStack();
            if (offHand.getItem() == ModItems.FLOWER_BAG) {
                totalSucked += trySuckIntoBag(serverPlayer, offHand, itemStack, totalSucked);
            }
        }

        // ===== 步骤3：处理结果 =====
        if (totalSucked > 0) {
            int originalCount = itemStack.getCount();
            itemStack.decrement(totalSucked);

            // 播放已吸入部分的拾取动画
            serverPlayer.sendPickup(itemEntity, totalSucked);

            if (itemStack.isEmpty()) {
                // 全部吸完了，删除掉落物，取消原版逻辑
                itemEntity.discard();
                ci.cancel();
            }
            // 如果还有剩余，不 cancel，让原版继续把剩余物品捡进玩家背包
        }
    }

    /**
     * 尝试把花朵吸入袋子，返回实际吸入的数量。
     * 不会修改 itemStack，只计算和存储。
     * @param alreadySucked 之前已经吸入的总数（用来计算本次还能吸多少）
     */
    private int trySuckIntoBag(ServerPlayerEntity player, ItemStack bagStack, ItemStack itemStack, int alreadySucked) {
        if (player.getServer() == null) return 0;
        if (itemStack.isEmpty()) return 0;

        UUID uuid = FlowerBagItem.getBackpackUuid(bagStack);
        BagStorage storage = BagStorage.getServerState(player.getServer());
        NbtCompound data = storage.getBackpackData(uuid);

        if (data.getByte("SuckEnabled") != 1) return 0;

        FlowerBagScreenHandler.FlowerBagInventory inv = new FlowerBagScreenHandler.FlowerBagInventory();
        inv.readNbt(data);

        // 用副本操作，绝不修改原始 itemStack
        int remaining = itemStack.getCount() - alreadySucked;
        if (remaining <= 0) return 0;
        ItemStack tempStack = itemStack.copy();
        tempStack.setCount(remaining);

        int originalTemp = tempStack.getCount();
        ItemStack leftover = inv.addStack(tempStack);
        int sucked = originalTemp - leftover.getCount();

        if (sucked > 0) {
            storage.putBackpackData(uuid, inv.writeNbt());
        }

        return sucked;
    }
}
