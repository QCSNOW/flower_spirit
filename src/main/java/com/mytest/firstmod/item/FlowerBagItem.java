package com.mytest.firstmod.item;
import com.mytest.firstmod.screen.FlowerBagScreenHandler;


import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.screen.NamedScreenHandlerFactory;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.text.Text;
import net.minecraft.util.Hand;
import net.minecraft.util.TypedActionResult;
import net.minecraft.world.World;
import org.jetbrains.annotations.Nullable;

import java.util.UUID;

public class FlowerBagItem extends Item {
    public FlowerBagItem(Settings settings) {
        super(settings);
    }

    // 获取或生成UUID
    public static UUID getBackpackUuid(ItemStack stack) {
        NbtCompound nbt = stack.getOrCreateNbt();
        if (!nbt.containsUuid("BackpackUUID")) {
            nbt.putUuid("BackpackUUID", UUID.randomUUID());
        }
        return nbt.getUuid("BackpackUUID");
    }

    @Override
    public TypedActionResult<ItemStack> use(World world, PlayerEntity user, Hand hand) {
        ItemStack stack = user.getStackInHand(hand);
        if (!world.isClient()) {
            user.openHandledScreen(new NamedScreenHandlerFactory() {
                @Override
                public Text getDisplayName() {
                    return Text.translatable("container.firstmod.flower_bag");
                }

                @Nullable
                @Override
                public ScreenHandler createMenu(int syncId, PlayerInventory playerInventory, PlayerEntity player) {
                    return new FlowerBagScreenHandler(syncId, playerInventory, stack, hand);
                }
            });
        }
        return TypedActionResult.success(stack, world.isClient());
    }
}