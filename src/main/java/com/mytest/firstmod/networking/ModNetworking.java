package com.mytest.firstmod.networking;
import com.mytest.firstmod.block.entity.AbstractWorkBlockEntity;
import com.mytest.firstmod.screen.ModScreenHandlers;


import net.fabricmc.fabric.api.networking.v1.ServerPlayNetworking;
import net.minecraft.network.PacketByteBuf;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;
import net.minecraft.server.network.ServerPlayNetworkHandler;
import net.minecraft.screen.ScreenHandler;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.BlockPos;

public class ModNetworking {
    public static final Identifier POUR_ACTION = new Identifier("firstmod", "pour_action");
    public static final Identifier SELECT_LAYER = new Identifier("firstmod", "select_layer");
    public static final Identifier MOVE_LAYER = new Identifier("firstmod", "move_layer");

    public static void registerServerReceivers() {
        ServerPlayNetworking.registerGlobalReceiver(POUR_ACTION, (server, player, handler, buf, responseSender) -> {
            int syncId = buf.readInt();
            server.execute(() -> handlePourAction(player, syncId));
        });

        ServerPlayNetworking.registerGlobalReceiver(SELECT_LAYER, (server, player, handler, buf, responseSender) -> {
            int syncId = buf.readInt();
            int layerIndex = buf.readInt();
            server.execute(() -> handleSelectLayer(player, syncId, layerIndex));
        });

        ServerPlayNetworking.registerGlobalReceiver(MOVE_LAYER, (server, player, handler, buf, responseSender) -> {
            int syncId = buf.readInt();
            int direction = buf.readInt();
            server.execute(() -> handleMoveLayer(player, syncId, direction));
        });
    }

    private static AbstractWorkBlockEntity getBlockEntity(ServerPlayerEntity player, int syncId) {
        ScreenHandler sh = player.currentScreenHandler;
        if (sh instanceof ModScreenHandlers.GenericWorkScreenHandler workHandler) {
            if (workHandler.getSyncId() == syncId) {
                BlockPos pos = workHandler.getBlockPos();
                if (player.getWorld().getBlockEntity(pos) instanceof AbstractWorkBlockEntity be) {
                    return be;
                }
            }
        }
        return null;
    }

    private static void handlePourAction(ServerPlayerEntity player, int syncId) {
        AbstractWorkBlockEntity be = getBlockEntity(player, syncId);
        if (be != null) be.handlePourAction();
    }

    private static void handleSelectLayer(ServerPlayerEntity player, int syncId, int layerIndex) {
        AbstractWorkBlockEntity be = getBlockEntity(player, syncId);
        if (be != null) be.handleSelectLayer(layerIndex);
    }

    private static void handleMoveLayer(ServerPlayerEntity player, int syncId, int direction) {
        AbstractWorkBlockEntity be = getBlockEntity(player, syncId);
        if (be != null) be.handleMoveLayer(direction);
    }
}
