package com.mytest.firstmod.item;

import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.entity.effect.StatusEffectInstance;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.item.Item;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.network.ServerPlayerEntity;

public class ModItemEffects {

    // 每20tick(1秒)执行一次检查，效果持续60tick(3秒)，保证不会断档
    private static final int CHECK_INTERVAL = 20;
    private static final int EFFECT_DURATION = 60;
    private static int serverTickCounter = 0;

    public static void register() {
        ServerTickEvents.END_SERVER_TICK.register((MinecraftServer server) -> {
            serverTickCounter++;
            if (serverTickCounter % CHECK_INTERVAL != 0) {
                return;
            }

            for (ServerPlayerEntity player : server.getPlayerManager().getPlayerList()) {
                doFlowerSpiritEffectCheck(player);
            }
        });
    }

    private static void doFlowerSpiritEffectCheck(ServerPlayerEntity player) {
        int regenerateLevel = 0;

        // 1. 判断是否穿满4件全套盔甲
        int armorCount = 0;
        for (var stack : player.getArmorItems()) {
            Item item = stack.getItem();
            if (isFlowerSpiritArmor(item)) {
                armorCount++;
            }
        }
        if (armorCount >= 4) {
            regenerateLevel += 1;
        }

        // 2. 判断主手是否拿着花精剑/工具
        Item mainHandItem = player.getMainHandStack().getItem();
        if (isFlowerSpiritToolOrSword(mainHandItem)) {
            regenerateLevel += 1;
        }

        if (regenerateLevel > 0) {
            int amplifier = regenerateLevel - 1;
            StatusEffectInstance existing = player.getStatusEffect(StatusEffects.REGENERATION);
            // 只有在没有效果、或者效果剩余时间小于1秒时才刷新，避免每1秒都重置计时
            // 效果持续3秒，每1秒检查一次，剩余<1秒时刷新，保证效果不会断
            if (existing == null || existing.getDuration() < 20) {
                player.addStatusEffect(new StatusEffectInstance(
                        StatusEffects.REGENERATION,
                        EFFECT_DURATION,
                        amplifier,
                        false,
                        true,
                        true
                ));
            }
        }
        // 注意：不主动删除再生效果，避免清掉其他来源（药水、信标等）的再生
        // 套装效果持续3秒，每1秒刷新一次，脱装后最多2秒就会自然过期
    }

    private static boolean isFlowerSpiritArmor(Item item) {
        return item == ModItems.FLOWER_SPIRIT_HELMET
                || item == ModItems.FLOWER_SPIRIT_CHESTPLATE
                || item == ModItems.FLOWER_SPIRIT_LEGGINGS
                || item == ModItems.FLOWER_SPIRIT_BOOTS;
    }

    private static boolean isFlowerSpiritToolOrSword(Item item) {
        return item == ModItems.FLOWER_SPIRIT_SWORD
                || item == ModItems.FLOWER_SPIRIT_PICKAXE
                || item == ModItems.FLOWER_SPIRIT_AXE
                || item == ModItems.FLOWER_SPIRIT_SHOVEL
                || item == ModItems.FLOWER_SPIRIT_HOE;
    }
}
