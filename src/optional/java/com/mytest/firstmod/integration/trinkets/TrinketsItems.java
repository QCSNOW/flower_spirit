package com.mytest.firstmod.integration.trinkets;

import com.mytest.firstmod.Firstmod;
import net.minecraft.item.Item;
import net.minecraft.util.Identifier;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;

/**
 * 饰品物品注册（Trinkets 模组集成）
 *
 * 提供两个饰品：
 * - FLOWER_SPIRIT_RING  花精戒指（戒指槽，速度 II）
 * - FLOWER_SPIRIT_AMULET 花精护符（项链槽，生命恢复 I）
 */
public class TrinketsItems {

    public static Item FLOWER_SPIRIT_RING;
    public static Item FLOWER_SPIRIT_AMULET;

    public static void init() {
        FLOWER_SPIRIT_RING = Registry.register(Registries.ITEM,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_ring"),
                new FlowerSpiritRingItem(new Item.Settings().maxCount(1)));

        FLOWER_SPIRIT_AMULET = Registry.register(Registries.ITEM,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_amulet"),
                new FlowerSpiritAmuletItem(new Item.Settings().maxCount(1)));

        Firstmod.LOGGER.info("繁花物语：饰品栏集成已加载（2 件饰品）");
    }
}
