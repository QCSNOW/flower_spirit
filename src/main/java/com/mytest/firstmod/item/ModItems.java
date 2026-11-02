package com.mytest.firstmod.item;
import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.ModBlocks;
import com.mytest.firstmod.block.ModFlowerBlocks;


import net.minecraft.item.*;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

@SuppressWarnings("all")
public class ModItems {

    //=====方块对应的物品=====
    public static final Item FLOWER_SPIRIT_BLOCK_ITEM;
    public static final Item FLOWER_SPIRIT_CRAFTER_ITEM;

    //=====普通物品=====
    public static final Item FLOWER_SPIRIT;
    public static final Item FLOWER_SPIRIT_INGOT;
    public static final Item FLOWER_SPIRIT_CORE;
    public static final Item FLOWER_CRYSTAL;   // 繁花结晶

    //=====工具武器=====
    public static final Item FLOWER_SPIRIT_SWORD;
    public static final Item FLOWER_SPIRIT_PICKAXE;
    public static final Item FLOWER_SPIRIT_AXE;
    public static final Item FLOWER_SPIRIT_SHOVEL;
    public static final Item FLOWER_SPIRIT_HOE;

    //=====盔甲=====
    public static final Item FLOWER_SPIRIT_HELMET;
    public static final Item FLOWER_SPIRIT_CHESTPLATE;
    public static final Item FLOWER_SPIRIT_LEGGINGS;
    public static final Item FLOWER_SPIRIT_BOOTS;

    //=====繁花收纳袋=====
    public static final Item FLOWER_BAG;

    static {
        FLOWER_SPIRIT_BLOCK_ITEM = Registry.register(Registries.ITEM,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_block"),
                new BlockItem(ModBlocks.FLOWER_SPIRIT_BLOCK, new Item.Settings()));

        FLOWER_SPIRIT_CRAFTER_ITEM = Registry.register(Registries.ITEM,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_crafter"),
                new BlockItem(ModBlocks.FLOWER_SPIRIT_CRAFTER, new Item.Settings().maxCount(64)));

        for (java.util.Map.Entry<String, net.minecraft.block.Block> entry : ModFlowerBlocks.FLOWERS.entrySet()) {
            Registry.register(Registries.ITEM,
                    new Identifier(Firstmod.MOD_ID, entry.getKey()),
                    new BlockItem(entry.getValue(), new Item.Settings().maxCount(64)));
        }

        FLOWER_SPIRIT = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit"), new Item(new Item.Settings().maxCount(64)));
        FLOWER_SPIRIT_INGOT = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_ingot"), new Item(new Item.Settings().maxCount(64)));
        FLOWER_SPIRIT_CORE = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_core"), new Item(new Item.Settings().maxCount(64)));
        FLOWER_CRYSTAL = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_crystal"), new Item(new Item.Settings().maxCount(64)));

        FLOWER_BAG = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_bag"),
                new FlowerBagItem(new Item.Settings().maxCount(1)));

        FLOWER_SPIRIT_SWORD = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_sword"), new SwordItem(ModToolMaterials.FLOWER_SPIRIT_MATERIAL, 3, -2.4F, new Item.Settings()));
        FLOWER_SPIRIT_PICKAXE = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_pickaxe"), new PickaxeItem(ModToolMaterials.FLOWER_SPIRIT_MATERIAL, 1, -2.8F, new Item.Settings()));
        FLOWER_SPIRIT_AXE = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_axe"), new AxeItem(ModToolMaterials.FLOWER_SPIRIT_MATERIAL, 5.0F, -3.1F, new Item.Settings()));
        FLOWER_SPIRIT_SHOVEL = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_shovel"), new ShovelItem(ModToolMaterials.FLOWER_SPIRIT_MATERIAL, 1.5F, -3.0F, new Item.Settings()));
        FLOWER_SPIRIT_HOE = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_hoe"), new HoeItem(ModToolMaterials.FLOWER_SPIRIT_MATERIAL, -2, -1.0F, new Item.Settings()));

        FLOWER_SPIRIT_HELMET = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_helmet"), new ArmorItem(ModArmorMaterials.FLOWER_SPIRIT_ARMOR, ArmorItem.Type.HELMET, new Item.Settings()));
        FLOWER_SPIRIT_CHESTPLATE = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_chestplate"), new ArmorItem(ModArmorMaterials.FLOWER_SPIRIT_ARMOR, ArmorItem.Type.CHESTPLATE, new Item.Settings()));
        FLOWER_SPIRIT_LEGGINGS = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_leggings"), new ArmorItem(ModArmorMaterials.FLOWER_SPIRIT_ARMOR, ArmorItem.Type.LEGGINGS, new Item.Settings()));
        FLOWER_SPIRIT_BOOTS = Registry.register(Registries.ITEM, new Identifier(Firstmod.MOD_ID, "flower_spirit_boots"), new ArmorItem(ModArmorMaterials.FLOWER_SPIRIT_ARMOR, ArmorItem.Type.BOOTS, new Item.Settings()));
    }

    public static void registerAll() {
        // 触发静态代码块
    }
}