package com.mytest.firstmod.screen;
import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.entity.AbstractWorkBlockEntity;


import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.resource.featuretoggle.FeatureSet;
import net.minecraft.screen.PropertyDelegate;
import net.minecraft.screen.ScreenHandlerType;
import net.minecraft.screen.slot.Slot;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.Identifier;
import net.minecraft.registry.tag.ItemTags;

public class ModScreenHandlers {

    public static ScreenHandlerType<GenericWorkScreenHandler> GENERIC_WORK_TYPE;
    public static ScreenHandlerType<FlowerBagScreenHandler> FLOWER_BAG_SCREEN_HANDLER;

    public static void registerAll() {
        GENERIC_WORK_TYPE = Registry.register(
                Registries.SCREEN_HANDLER,
                new Identifier(Firstmod.MOD_ID, "generic_work"),
                new ScreenHandlerType<>(GenericWorkScreenHandler::new, FeatureSet.empty())
        );

        // 【新增】繁花收纳袋的注册
        FLOWER_BAG_SCREEN_HANDLER = Registry.register(
                Registries.SCREEN_HANDLER,
                new Identifier(Firstmod.MOD_ID, "flower_bag"),
                new ScreenHandlerType<>(FlowerBagScreenHandler::new, FeatureSet.empty())
        );
    }

    public static class GenericWorkScreenHandler extends AbstractWorkScreenHandler {

        private static final int BLOCK_SLOT_COUNT = 3;

        // Slot positions
        private static final int BUCKET_X = 12, BUCKET_Y = 72;
        private static final int INPUT_X = 70, INPUT_Y = 72;
        private static final int OUTPUT_X = 116, OUTPUT_Y = 72;

        // Client constructor
        public GenericWorkScreenHandler(int syncId, PlayerInventory inventory) {
            super(GENERIC_WORK_TYPE, syncId, inventory, BlockPos.ORIGIN,
                    new PropertyDelegate() {
                        private final int[] data = new int[AbstractWorkBlockEntity.PROP_COUNT];
                        @Override public int get(int index) { return data[index]; }
                        @Override public void set(int index, int value) { data[index] = value; }
                        @Override public int size() { return data.length; }
                    });
            SimpleInventory dummyInv = new SimpleInventory(AbstractWorkBlockEntity.SLOT_COUNT);
            addBlockSlots(dummyInv);
        }

        // Server constructor
        public GenericWorkScreenHandler(int syncId, PlayerInventory playerInv, BlockPos pos,
                                        SimpleInventory inv, PropertyDelegate propDelegate) {
            super(GENERIC_WORK_TYPE, syncId, playerInv, pos, propDelegate);
            addBlockSlots(inv);
        }

        private void addBlockSlots(SimpleInventory inv) {
            addSlot(new BucketSlot(inv, AbstractWorkBlockEntity.SLOT_BUCKET, BUCKET_X, BUCKET_Y));
            addSlot(new FlowerSlot(inv, AbstractWorkBlockEntity.SLOT_INPUT, INPUT_X, INPUT_Y));
            addSlot(new OutputSlot(inv, AbstractWorkBlockEntity.SLOT_OUTPUT, OUTPUT_X, OUTPUT_Y));
        }

        @Override
        public ItemStack quickMove(PlayerEntity player, int slotIndex) {
            ItemStack result = ItemStack.EMPTY;
            Slot slot = this.slots.get(slotIndex);

            if (slot != null && slot.hasStack()) {
                ItemStack stack = slot.getStack();
                result = stack.copy();

                if (slotIndex < BLOCK_SLOT_COUNT) {
                    if (!this.insertItem(stack, BLOCK_SLOT_COUNT, this.slots.size(), true)) {
                        return ItemStack.EMPTY;
                    }
                } else {
                    if (!this.insertItem(stack, 0, BLOCK_SLOT_COUNT, false)) {
                        if (slotIndex < BLOCK_SLOT_COUNT + 27) {
                            if (!this.insertItem(stack, BLOCK_SLOT_COUNT + 27, this.slots.size(), false)) {
                                return ItemStack.EMPTY;
                            }
                        } else {
                            if (!this.insertItem(stack, BLOCK_SLOT_COUNT, BLOCK_SLOT_COUNT + 27, false)) {
                                return ItemStack.EMPTY;
                            }
                        }
                    }
                }

                if (stack.isEmpty()) {
                    slot.setStack(ItemStack.EMPTY);
                } else {
                    slot.markDirty();
                }
            }
            return result;
        }

        // ===== Custom Slots =====
        // Vanilla pattern (like PlayerScreenHandler armor slots):
        // getBackgroundSprite() returns Pair.of(blocksAtlas, spriteId)
        // Textures live in assets/firstmod/textures/item/, auto-stitched into blocks atlas.

        static class BucketSlot extends Slot {
            public BucketSlot(SimpleInventory inv, int index, int x, int y) {
                super(inv, index, x, y);
            }
            @Override
            public boolean canInsert(ItemStack stack) {
                return stack.isOf(Items.BUCKET) || stack.isOf(Items.WATER_BUCKET);
            }
            @Override
            public int getMaxItemCount() {
                return 1;
            }
            @Override
            public com.mojang.datafixers.util.Pair<net.minecraft.util.Identifier, net.minecraft.util.Identifier> getBackgroundSprite() {
                return com.mojang.datafixers.util.Pair.of(
                        new net.minecraft.util.Identifier("textures/atlas/blocks.png"),
                        new net.minecraft.util.Identifier("firstmod", "item/empty_slot_bucket"));
            }
        }

        static class FlowerSlot extends Slot {
            public FlowerSlot(SimpleInventory inv, int index, int x, int y) {
                super(inv, index, x, y);
            }
            @Override
            public boolean canInsert(ItemStack stack) {
                return stack.isIn(ItemTags.FLOWERS);
            }
            @Override
            public com.mojang.datafixers.util.Pair<net.minecraft.util.Identifier, net.minecraft.util.Identifier> getBackgroundSprite() {
                return com.mojang.datafixers.util.Pair.of(
                        new net.minecraft.util.Identifier("textures/atlas/blocks.png"),
                        new net.minecraft.util.Identifier("firstmod", "item/empty_slot_flower"));
            }
        }

        static class OutputSlot extends Slot {
            public OutputSlot(SimpleInventory inv, int index, int x, int y) {
                super(inv, index, x, y);
            }
            @Override
            public boolean canInsert(ItemStack stack) {
                return false;
            }
            @Override
            public com.mojang.datafixers.util.Pair<net.minecraft.util.Identifier, net.minecraft.util.Identifier> getBackgroundSprite() {
                return com.mojang.datafixers.util.Pair.of(
                        new net.minecraft.util.Identifier("textures/atlas/blocks.png"),
                        new net.minecraft.util.Identifier("firstmod", "item/empty_slot_dust"));
            }
        }
    }
}
