package com.mytest.firstmod.screen;
import com.mytest.firstmod.item.FlowerBagItem;
import com.mytest.firstmod.storage.BagStorage;


import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtList;
import net.minecraft.registry.tag.ItemTags;
import net.minecraft.screen.ArrayPropertyDelegate;
import net.minecraft.screen.PropertyDelegate;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.screen.slot.Slot;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.Hand;
import net.minecraft.registry.Registries;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.UUID;

@SuppressWarnings("all")
public class FlowerBagScreenHandler extends ScreenHandler {
    private final FlowerBagInventory inventory;
    public final PropertyDelegate propertyDelegate;
    private final UUID backpackUuid;
    private final Hand hand;

    public static class FlowerBagInventory extends SimpleInventory {
        private int suckEnabled;
        private int sortMode;

        public FlowerBagInventory() { super(18); }

        @Override
        public boolean isValid(int slot, ItemStack stack) {
            return stack.isIn(ItemTags.FLOWERS);
        }

        public int getSuckEnabled() { return suckEnabled; }
        public int getSortMode() { return sortMode; }
        public void setSuckEnabled(int v) { suckEnabled = v; }
        public void setSortMode(int v) { sortMode = v; }

        public void readNbt(NbtCompound nbt) {
            if (nbt.contains("Items", 9)) {
                NbtList list = nbt.getList("Items", 10);
                for (int i = 0; i < list.size(); i++) {
                    NbtCompound itemNbt = list.getCompound(i);
                    int slot = itemNbt.getByte("Slot") & 255;
                    if (slot < this.size()) this.setStack(slot, ItemStack.fromNbt(itemNbt));
                }
            }
            suckEnabled = nbt.getByte("SuckEnabled");
            sortMode = nbt.getByte("SortMode");
        }

        public NbtCompound writeNbt() {
            NbtCompound nbt = new NbtCompound();
            NbtList list = new NbtList();
            for (int i = 0; i < this.size(); i++) {
                ItemStack itemStack = this.getStack(i);
                if (!itemStack.isEmpty()) {
                    NbtCompound itemNbt = new NbtCompound();
                    itemNbt.putByte("Slot", (byte) i);
                    itemStack.writeNbt(itemNbt);
                    list.add(itemNbt);
                }
            }
            nbt.put("Items", list);
            nbt.putByte("SuckEnabled", (byte) suckEnabled);
            nbt.putByte("SortMode", (byte) sortMode);
            return nbt;
        }
    }

    public FlowerBagScreenHandler(int syncId, PlayerInventory playerInventory) {
        this(syncId, playerInventory, ItemStack.EMPTY, Hand.MAIN_HAND);
    }

    public FlowerBagScreenHandler(int syncId, PlayerInventory playerInventory, ItemStack bagStack, Hand hand) {
        super(ModScreenHandlers.FLOWER_BAG_SCREEN_HANDLER, syncId);
        this.hand = hand;
        this.backpackUuid = FlowerBagItem.getBackpackUuid(bagStack);
        this.inventory = new FlowerBagInventory();
        this.propertyDelegate = new ArrayPropertyDelegate(4);

        if (!playerInventory.player.getWorld().isClient()) {
            MinecraftServer server = playerInventory.player.getServer();
            if (server != null) {
                BagStorage storage = BagStorage.getServerState(server);
                NbtCompound data = storage.getBackpackData(backpackUuid);
                this.inventory.readNbt(data);
                propertyDelegate.set(0, inventory.getSuckEnabled());
                propertyDelegate.set(1, inventory.getSortMode());
            }
        }

        for (int row = 0; row < 2; ++row)
            for (int col = 0; col < 9; ++col)
                this.addSlot(new Slot(this.inventory, col + row * 9, 9 + col * 18, 27 + row * 18));

        for (int row = 0; row < 3; ++row)
            for (int col = 0; col < 9; ++col)
                this.addSlot(new Slot(playerInventory, col + row * 9 + 9, 9 + col * 18, 85 + row * 18));

        for (int col = 0; col < 9; ++col)
            this.addSlot(new Slot(playerInventory, col, 9 + col * 18, 143));

        this.addProperties(this.propertyDelegate);
    }

    @Override
    public boolean canUse(PlayerEntity player) { return true; }

    @Override
    public boolean onButtonClick(PlayerEntity player, int buttonId) {
        switch (buttonId) {
            case 0:
                inventory.setSuckEnabled(propertyDelegate.get(0) == 1 ? 0 : 1);
                propertyDelegate.set(0, inventory.getSuckEnabled());
                break;
            case 1: moveToBag(player); break;
            case 2: moveToPlayer(player); break;
            case 3:
                inventory.setSortMode((propertyDelegate.get(1) + 1) % 3);
                propertyDelegate.set(1, inventory.getSortMode());
                sortInventory();
                break;
        }
        saveToStorage(player);
        return true;
    }

    @Override
    public void onClosed(PlayerEntity player) {
        super.onClosed(player);
        if (!player.getWorld().isClient()) saveToStorage(player);
    }

    private void saveToStorage(PlayerEntity player) {
        MinecraftServer server = player.getServer();
        if (server != null) {
            BagStorage storage = BagStorage.getServerState(server);
            storage.putBackpackData(backpackUuid, inventory.writeNbt());
        }
    }

    // =====================================================================
    // 一键存入：只从主背包（9~35）拿，按顺序，袋子满了立刻停，物品一个不丢
    // =====================================================================
    private void moveToBag(PlayerEntity player) {
        PlayerInventory playerInv = player.getInventory();

        // 只遍历主背包 9~35
        for (int i = 9; i <= 35; i++) {
            ItemStack invStack = playerInv.getStack(i);
            if (invStack.isEmpty()) continue;
            if (!invStack.isIn(ItemTags.FLOWERS)) continue;

            // 第一步：尝试与袋子已有的同类物品堆叠
            for (int j = 0; j < inventory.size() && !invStack.isEmpty(); j++) {
                ItemStack bagStack = inventory.getStack(j);
                if (bagStack.isEmpty()) continue;
                if (!ItemStack.canCombine(bagStack, invStack)) continue;

                int space = bagStack.getMaxCount() - bagStack.getCount();
                if (space <= 0) continue;

                int move = Math.min(space, invStack.getCount());
                bagStack.setCount(bagStack.getCount() + move);
                invStack.setCount(invStack.getCount() - move);
            }

            // 第二步：尝试放入袋子的空槽
            for (int j = 0; j < inventory.size() && !invStack.isEmpty(); j++) {
                if (!inventory.getStack(j).isEmpty()) continue;
                inventory.setStack(j, invStack.copy());
                invStack.setCount(0);
            }

            // 第三步：处理玩家背包这格
            if (invStack.isEmpty()) {
                playerInv.setStack(i, ItemStack.EMPTY);
            } else {
                // 袋子满了，把剩余量写回，并且停止存入
                playerInv.setStack(i, invStack);
                break;
            }
        }
        this.sendContentUpdates();
    }

    // =====================================================================
    // 一键取出：从袋子 0→17 按顺序取，只放到玩家主背包(0~35)，不含盔甲和副手
    // =====================================================================
    private void moveToPlayer(PlayerEntity player) {
        PlayerInventory playerInv = player.getInventory();

        for (int i = 0; i < inventory.size(); i++) {
            ItemStack bagStack = inventory.getStack(i);
            if (bagStack.isEmpty()) continue;

            // 第一步：先与玩家已有的同类物品堆叠（只遍历主背包 0~35）
            for (int j = 0; j < 36 && !bagStack.isEmpty(); j++) {
                ItemStack invStack = playerInv.getStack(j);
                if (invStack.isEmpty()) continue;
                if (!ItemStack.canCombine(invStack, bagStack)) continue;

                int space = invStack.getMaxCount() - invStack.getCount();
                if (space <= 0) continue;

                int move = Math.min(space, bagStack.getCount());
                invStack.setCount(invStack.getCount() + move);
                bagStack.setCount(bagStack.getCount() - move);
            }

            // 第二步：尝试放入玩家背包的空槽（只遍历主背包 0~35）
            for (int j = 0; j < 36 && !bagStack.isEmpty(); j++) {
                if (!playerInv.getStack(j).isEmpty()) continue;
                playerInv.setStack(j, bagStack.copy());
                bagStack.setCount(0);
            }

            // 第三步：处理袋子这格
            if (bagStack.isEmpty()) {
                inventory.setStack(i, ItemStack.EMPTY);
            } else {
                // 玩家背包满了，把剩余量写回袋子，停止取出
                inventory.setStack(i, bagStack);
                break;
            }
        }
        this.sendContentUpdates();
    }

    private void sortInventory() {
        int mode = propertyDelegate.get(1);
        List<ItemStack> stacks = new ArrayList<>();
        for (int i = 0; i < inventory.size(); i++) {
            if (!inventory.getStack(i).isEmpty()) stacks.add(inventory.getStack(i));
        }
        if (mode == 0) stacks.sort(Comparator.comparing(a -> a.getName().getString()));
        else if (mode == 1) stacks.sort((a, b) -> Integer.compare(b.getCount(), a.getCount()));
        else if (mode == 2) stacks.sort(Comparator.comparing(a -> Registries.ITEM.getId(a.getItem()).toString()));

        for (int i = 0; i < inventory.size(); i++) inventory.setStack(i, ItemStack.EMPTY);
        for (int i = 0; i < stacks.size() && i < inventory.size(); i++) inventory.setStack(i, stacks.get(i));
        this.sendContentUpdates();
    }

    @Override
    public ItemStack quickMove(PlayerEntity player, int slot) {
        ItemStack result = ItemStack.EMPTY;
        Slot slotObj = this.slots.get(slot);
        if (slotObj.hasStack()) {
            ItemStack stack = slotObj.getStack();
            result = stack.copy();
            if (slot < 18) {
                if (!this.insertItem(stack, 18, this.slots.size(), true)) return ItemStack.EMPTY;
            } else {
                if (!this.insertItem(stack, 0, 18, false)) return ItemStack.EMPTY;
            }
            if (stack.isEmpty()) slotObj.setStack(ItemStack.EMPTY);
            else slotObj.markDirty();
        }
        return result;
    }
}