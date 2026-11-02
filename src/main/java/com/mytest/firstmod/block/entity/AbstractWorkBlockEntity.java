package com.mytest.firstmod.block.entity;
import com.mytest.firstmod.fluid.FluidTank;
import com.mytest.firstmod.fluid.ModFluids;
import com.mytest.firstmod.recipe.WorkRecipe;
import com.mytest.firstmod.recipe.WorkRecipes;
import com.mytest.firstmod.screen.ModScreenHandlers;


import net.minecraft.block.BlockState;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.inventory.SidedInventory;
import net.minecraft.inventory.SimpleInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtList;
import net.minecraft.network.packet.Packet;
import net.minecraft.network.listener.ClientPlayPacketListener;
import net.minecraft.network.packet.s2c.play.BlockEntityUpdateS2CPacket;
import net.minecraft.particle.ParticleTypes;
import net.minecraft.screen.NamedScreenHandlerFactory;
import net.minecraft.screen.PropertyDelegate;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.server.world.ServerWorld;
import net.minecraft.state.property.Properties;
import net.minecraft.text.Text;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.Direction;

public class AbstractWorkBlockEntity extends BlockEntity
        implements NamedScreenHandlerFactory, SidedInventory {

    public static final int SLOT_BUCKET = 0;
    public static final int SLOT_INPUT = 1;
    public static final int SLOT_OUTPUT = 2;
    public static final int SLOT_COUNT = 3;

    public static final int PROP_TOTAL = 0;
    public static final int PROP_LAYER_COUNT = 1;
    public static final int PROP_SELECTED = 2;
    public static final int PROP_PROGRESS = 3;
    public static final int PROP_MAX_LAYERS = 5;
    public static final int PROP_COUNT = 4 + PROP_MAX_LAYERS * 2;

    private final SimpleInventory inventory = new SimpleInventory(SLOT_COUNT);
    private final FluidTank fluidTank = new FluidTank();
    private final int[] propertyData = new int[PROP_COUNT];
    private final PropertyDelegate propertyDelegate = new PropertyDelegate() {
        @Override public int get(int index) { return propertyData[index]; }
        @Override public void set(int index, int value) { propertyData[index] = value; }
        @Override public int size() { return PROP_COUNT; }
    };

    private final Text guiTitle;
    private int craftProgress = 0;
    private WorkRecipe currentRecipe = null;
    private int syncCounter = 0;
    private int prevFluidAmount = 0;

    public AbstractWorkBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state, Text title) {
        super(type, pos, state);
        this.guiTitle = title;
    }

    public PropertyDelegate getPropertyDelegate() {
        return propertyDelegate;
    }

    public FluidTank getFluidTank() {
        return fluidTank;
    }

    public SimpleInventory getInventory() {
        return inventory;
    }

    // ==================== Tick ====================

    public static void tick(net.minecraft.world.World world, BlockPos pos, BlockState state, AbstractWorkBlockEntity be) {
        if (world.isClient) {
            be.clientTick();
        } else {
            be.serverTick();
        }
    }

    private void serverTick() {
        ItemStack input = inventory.getStack(SLOT_INPUT);
        ItemStack output = inventory.getStack(SLOT_OUTPUT);

        WorkRecipe recipe = WorkRecipes.findMatch(input, fluidTank);

        if (recipe == null) {
            if (currentRecipe != null && !input.isEmpty() && currentRecipe.getInput().test(input)) {
                // Input still matches, just no fluid - pause crafting
            } else {
                craftProgress = 0;
                currentRecipe = null;
            }
        } else {
            if (currentRecipe != recipe) {
                currentRecipe = recipe;
                craftProgress = 0;
            }

            ItemStack recipeOutput = recipe.getOutput();
            boolean outputBlocked = !output.isEmpty()
                    && (!output.isOf(recipeOutput.getItem())
                    || output.getCount() + recipeOutput.getCount() > output.getMaxCount());

            if (!outputBlocked) {
                craftProgress++;
                if (craftProgress % 4 == 0) {
                    fluidTank.removeFirst(recipe.getFluid(), 1);
                    sync();
                }
                if (craftProgress >= 40) {
                    inventory.getStack(SLOT_INPUT).decrement(1);
                    if (output.isEmpty()) {
                        inventory.setStack(SLOT_OUTPUT, recipeOutput.copy());
                    } else {
                        output.increment(recipeOutput.getCount());
                    }
                    craftProgress = 0;
                    sync();
                }
                markDirty();
            } else {
                craftProgress = 0;
            }
        }

        updatePropertyDelegate();

        // Auto-pour water bucket when fluid depletes from non-zero to zero
        int currentFluid = fluidTank.getTotalAmount();
        if (prevFluidAmount > 0 && currentFluid == 0) {
            ItemStack bucketStack = inventory.getStack(SLOT_BUCKET);
            if (bucketStack.isOf(Items.WATER_BUCKET)) {
                int added = fluidTank.add(ModFluids.WATER, FluidTank.BUCKET_AMOUNT);
                if (added > 0) {
                    inventory.setStack(SLOT_BUCKET, new ItemStack(Items.BUCKET));
                    sync();
                }
            }
        }
        prevFluidAmount = currentFluid;

        syncCounter++;
        if (syncCounter >= 20) {
            syncCounter = 0;
            sync();
        }
    }

    private void clientTick() {
        if (craftProgress > 0 && fluidTank.getTotalAmount() > 0) {
            double baseY = pos.getY() + 2.0 / 16.0;
            double cavityHeight = 8.0 / 16.0;
            double fluidHeight = cavityHeight * ((double) fluidTank.getTotalAmount() / FluidTank.MAX_CAPACITY);
            double surfaceY = baseY + fluidHeight;

            if (world.random.nextInt(2) == 0) {
                double x = pos.getX() + 4.0 / 16.0 + world.random.nextDouble() * (8.0 / 16.0);
                double z = pos.getZ() + 4.0 / 16.0 + world.random.nextDouble() * (8.0 / 16.0);
                world.addParticle(ParticleTypes.CLOUD, x, surfaceY, z,
                        (world.random.nextDouble() - 0.5) * 0.03,
                        0.04 + world.random.nextDouble() * 0.03,
                        (world.random.nextDouble() - 0.5) * 0.03);
            }

            if (world.random.nextInt(4) == 0) {
                double x = pos.getX() + 4.0 / 16.0 + world.random.nextDouble() * (8.0 / 16.0);
                double z = pos.getZ() + 4.0 / 16.0 + world.random.nextDouble() * (8.0 / 16.0);
                world.addParticle(ParticleTypes.SPLASH, x, surfaceY + 0.05, z,
                        (world.random.nextDouble() - 0.5) * 0.02,
                        0.02 + world.random.nextDouble() * 0.02,
                        (world.random.nextDouble() - 0.5) * 0.02);
            }
        }
    }

    // ==================== Property Delegate ====================

    private void updatePropertyDelegate() {
        propertyData[PROP_TOTAL] = fluidTank.getTotalAmount();
        propertyData[PROP_LAYER_COUNT] = fluidTank.getLayerCount();
        propertyData[PROP_SELECTED] = fluidTank.getSelectedLayer();
        propertyData[PROP_PROGRESS] = craftProgress;
        for (int i = 0; i < PROP_MAX_LAYERS; i++) {
            FluidTank.FluidLayer layer = fluidTank.getLayer(i);
            propertyData[4 + i] = layer != null ? layer.getType().getId() : -1;
            propertyData[4 + PROP_MAX_LAYERS + i] = layer != null ? layer.getAmount() : 0;
        }
    }

    // ==================== Sync ====================

    private void sync() {
        if (world != null && !world.isClient && world instanceof ServerWorld serverWorld) {
            markDirty();
            serverWorld.getChunkManager().markForUpdate(pos);
        }
    }

    @Override
    public NbtCompound toInitialChunkDataNbt() {
        NbtCompound nbt = super.createNbtWithIdentifyingData();
        writeNbt(nbt);
        return nbt;
    }

    @Override
    public Packet<ClientPlayPacketListener> toUpdatePacket() {
        return BlockEntityUpdateS2CPacket.create(this);
    }

    // ==================== NBT ====================

    @Override
    protected void writeNbt(NbtCompound nbt) {
        super.writeNbt(nbt);
        NbtList items = new NbtList();
        for (int i = 0; i < SLOT_COUNT; i++) {
            ItemStack stack = inventory.getStack(i);
            if (!stack.isEmpty()) {
                NbtCompound slotTag = new NbtCompound();
                slotTag.putByte("Slot", (byte) i);
                stack.writeNbt(slotTag);
                items.add(slotTag);
            }
        }
        nbt.put("Items", items);
        nbt.put("FluidTank", fluidTank.writeNbt());
        nbt.putInt("CraftProgress", craftProgress);
    }

    @Override
    public void readNbt(NbtCompound nbt) {
        super.readNbt(nbt);
        inventory.clear();
        NbtList items = nbt.getList("Items", NbtCompound.COMPOUND_TYPE);
        for (int i = 0; i < items.size(); i++) {
            NbtCompound slotTag = items.getCompound(i);
            int slot = slotTag.getByte("Slot") & 0xFF;
            if (slot < SLOT_COUNT) {
                inventory.setStack(slot, ItemStack.fromNbt(slotTag));
            }
        }
        fluidTank.readNbt(nbt.getCompound("FluidTank"));
        craftProgress = nbt.getInt("CraftProgress");
        currentRecipe = null;
        prevFluidAmount = fluidTank.getTotalAmount();
    }

    // ==================== ScreenHandler ====================

    @Override
    public ScreenHandler createMenu(int syncId, PlayerInventory playerInventory, PlayerEntity player) {
        return new ModScreenHandlers.GenericWorkScreenHandler(
                syncId, playerInventory, this.pos, this.inventory, this.propertyDelegate);
    }

    @Override
    public Text getDisplayName() {
        return guiTitle;
    }

    // ==================== Pour/Select/Move Actions ====================

    public void handlePourAction() {
        ItemStack bucketStack = inventory.getStack(SLOT_BUCKET);
        if (bucketStack.isEmpty()) return;

        if (bucketStack.isOf(Items.WATER_BUCKET)) {
            int added = fluidTank.add(ModFluids.WATER, FluidTank.BUCKET_AMOUNT);
            if (added > 0) {
                inventory.setStack(SLOT_BUCKET, new ItemStack(Items.BUCKET));
                sync();
            }
        } else if (bucketStack.isOf(Items.BUCKET)) {
            int index = fluidTank.getSelectedLayer();
            if (index < 0 && fluidTank.getLayerCount() > 0) {
                index = fluidTank.getLayerCount() - 1;
            }
            if (index < 0) return;

            FluidTank.FluidLayer layer = fluidTank.getLayer(index);
            if (layer == null) return;

            if (layer.getAmount() >= FluidTank.BUCKET_AMOUNT) {
                fluidTank.removeFromLayer(index, FluidTank.BUCKET_AMOUNT);
                if (layer.getType().getId() == ModFluids.WATER.getId()) {
                    inventory.setStack(SLOT_BUCKET, new ItemStack(Items.WATER_BUCKET));
                }
                sync();
            } else if (layer.getAmount() > 0) {
                fluidTank.dumpLayer(index);
                sync();
            }
        }
    }

    public void handleSelectLayer(int layerIndex) {
        fluidTank.setSelectedLayer(layerIndex);
        sync();
    }

    public void handleMoveLayer(int direction) {
        int index = fluidTank.getSelectedLayer();
        if (index < 0) return;
        if (direction == 0) {
            fluidTank.moveLayerUp(index);
        } else {
            fluidTank.moveLayerDown(index);
        }
        sync();
    }

    // ==================== SidedInventory ====================

    private Direction getFacing() {
        if (world == null) return Direction.NORTH;
        BlockState state = world.getBlockState(pos);
        return state.get(Properties.HORIZONTAL_FACING);
    }

    private boolean isFrontOrBack(Direction side) {
        Direction facing = getFacing();
        return side == facing || side == facing.getOpposite();
    }

    private boolean isLeftOrRight(Direction side) {
        if (side == Direction.UP || side == Direction.DOWN) return false;
        return !isFrontOrBack(side);
    }

    @Override
    public int[] getAvailableSlots(Direction side) {
        if (side == Direction.DOWN) return new int[]{SLOT_OUTPUT, SLOT_BUCKET};
        if (side == Direction.UP) return new int[]{};
        if (isFrontOrBack(side)) return new int[]{SLOT_INPUT};
        if (isLeftOrRight(side)) return new int[]{SLOT_BUCKET};
        return new int[]{};
    }

    @Override
    public boolean canInsert(int slot, ItemStack stack, Direction dir) {
        if (dir == Direction.UP) return false;
        if (dir == Direction.DOWN) return false;

        if (slot == SLOT_INPUT) {
            // Front and back: accept flower input
            return isFrontOrBack(dir);
        }
        if (slot == SLOT_BUCKET) {
            // Left and right: accept water buckets only
            return isLeftOrRight(dir) && stack.isOf(Items.WATER_BUCKET);
        }
        return false;
    }

    @Override
    public boolean canExtract(int slot, ItemStack stack, Direction dir) {
        if (slot == SLOT_OUTPUT && dir == Direction.DOWN) {
            return true;
        }
        if (slot == SLOT_BUCKET && dir == Direction.DOWN) {
            // Only extract empty buckets from bottom
            return stack.isOf(Items.BUCKET);
        }
        return false;
    }

    // ==================== Inventory delegation ====================

    @Override
    public int size() { return inventory.size(); }

    @Override
    public boolean isEmpty() { return inventory.isEmpty(); }

    @Override
    public ItemStack getStack(int slot) { return inventory.getStack(slot); }

    @Override
    public ItemStack removeStack(int slot, int amount) { return inventory.removeStack(slot, amount); }

    @Override
    public ItemStack removeStack(int slot) { return inventory.removeStack(slot); }

    @Override
    public void setStack(int slot, ItemStack stack) {
        inventory.setStack(slot, stack);
        if (!stack.isEmpty() && stack.getCount() > stack.getMaxCount()) {
            stack.setCount(stack.getMaxCount());
        }
        markDirty();
    }

    @Override
    public void markDirty() {
        super.markDirty();
    }

    @Override
    public boolean canPlayerUse(PlayerEntity player) {
        if (world == null) return false;
        BlockPos pos = this.pos;
        return player.squaredDistanceTo(pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5) <= 64.0;
    }

    @Override
    public void clear() { inventory.clear(); }
}
