package com.mytest.firstmod.storage;

import net.minecraft.nbt.NbtCompound;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.PersistentState;
import net.minecraft.world.PersistentStateManager;
import net.minecraft.world.World;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class BagStorage extends PersistentState {
    private static final String DATA_NAME = "firstmod_backpacks";
    private final Map<UUID, NbtCompound> backpackData = new HashMap<>();

    public NbtCompound getBackpackData(UUID uuid) {
        return backpackData.getOrDefault(uuid, new NbtCompound());
    }

    public void putBackpackData(UUID uuid, NbtCompound nbt) {
        backpackData.put(uuid, nbt);
        this.markDirty();
    }

    @Override
    public NbtCompound writeNbt(NbtCompound nbt) {
        NbtCompound backpacks = new NbtCompound();
        for (Map.Entry<UUID, NbtCompound> entry : backpackData.entrySet()) {
            backpacks.put(entry.getKey().toString(), entry.getValue());
        }
        nbt.put("Backpacks", backpacks);
        return nbt;
    }

    public static BagStorage createFromNbt(NbtCompound nbt) {
        BagStorage storage = new BagStorage();
        NbtCompound backpacks = nbt.getCompound("Backpacks");
        for (String key : backpacks.getKeys()) {
            storage.backpackData.put(UUID.fromString(key), backpacks.getCompound(key));
        }
        return storage;
    }

    public static BagStorage getServerState(MinecraftServer server) {
        PersistentStateManager manager = server.getWorld(World.OVERWORLD).getPersistentStateManager();
        return manager.getOrCreate(BagStorage::createFromNbt, BagStorage::new, DATA_NAME);
    }
}