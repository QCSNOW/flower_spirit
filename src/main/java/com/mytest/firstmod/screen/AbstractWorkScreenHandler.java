package com.mytest.firstmod.screen;

import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.screen.PropertyDelegate;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.screen.ScreenHandlerType;
import net.minecraft.screen.slot.Slot;
import net.minecraft.util.math.BlockPos;

public abstract class AbstractWorkScreenHandler extends ScreenHandler {

    protected final BlockPos blockPos;
    protected final PropertyDelegate propertyDelegate;

    protected AbstractWorkScreenHandler(ScreenHandlerType<?> type, int syncId,
                                        PlayerInventory playerInv, BlockPos pos,
                                        PropertyDelegate propDelegate) {
        super(type, syncId);
        this.blockPos = pos;
        this.propertyDelegate = propDelegate;
        this.addProperties(propDelegate);
        addPlayerSlots(playerInv);
    }

    private void addPlayerSlots(PlayerInventory playerInventory) {
        int playerInvY = 118;
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                addSlot(new Slot(playerInventory, col + row * 9 + 9, 8 + col * 18, playerInvY + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            addSlot(new Slot(playerInventory, col, 8 + col * 18, playerInvY + 58));
        }
    }

    @Override
    public boolean canUse(PlayerEntity player) {
        if (blockPos == BlockPos.ORIGIN) return true;
        return player.squaredDistanceTo(
                blockPos.getX() + 0.5, blockPos.getY() + 0.5, blockPos.getZ() + 0.5) <= 64.0;
    }

    public BlockPos getBlockPos() { return this.blockPos; }

    public int getSyncId() { return this.syncId; }

    public int getProperty(int index) { return propertyDelegate.get(index); }
}
