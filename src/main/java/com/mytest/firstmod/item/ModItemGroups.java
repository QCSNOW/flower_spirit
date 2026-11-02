package com.mytest.firstmod.item;
import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.ModFlowerBlocks;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.item.Item;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public class ModItemGroups {

    public static void registerAll() {
        Registry.register(
                Registries.ITEM_GROUP,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_group"),
                FabricItemGroup.builder()
                        .icon(() -> new ItemStack(ModItems.FLOWER_SPIRIT_INGOT))
                        .displayName(Text.translatable("itemgroup.firstmod.flower_spirit"))
                        .entries((displayContext, entries) -> {
                            // 1. 普通材料
                            entries.add(ModItems.FLOWER_SPIRIT);
                            entries.add(ModItems.FLOWER_SPIRIT_INGOT);
                            entries.add(ModItems.FLOWER_SPIRIT_CORE);
                            entries.add(ModItems.FLOWER_CRYSTAL);

                            // 2. 繁花收纳袋
                            entries.add(ModItems.FLOWER_BAG);

                            // 3. 花朵方块
                            for (java.util.Map.Entry<String, net.minecraft.block.Block> entry : ModFlowerBlocks.FLOWERS.entrySet()) {
                                entries.add(new ItemStack(entry.getValue()));
                            }

                            // 4. 特殊方块物品
                            entries.add(ModItems.FLOWER_SPIRIT_BLOCK_ITEM);
                            entries.add(ModItems.FLOWER_SPIRIT_CRAFTER_ITEM);

                            // 5. 工具武器
                            entries.add(ModItems.FLOWER_SPIRIT_SWORD);
                            entries.add(ModItems.FLOWER_SPIRIT_PICKAXE);
                            entries.add(ModItems.FLOWER_SPIRIT_AXE);
                            entries.add(ModItems.FLOWER_SPIRIT_SHOVEL);
                            entries.add(ModItems.FLOWER_SPIRIT_HOE);

                            // 6. 盔甲
                            entries.add(ModItems.FLOWER_SPIRIT_HELMET);
                            entries.add(ModItems.FLOWER_SPIRIT_CHESTPLATE);
                            entries.add(ModItems.FLOWER_SPIRIT_LEGGINGS);
                            entries.add(ModItems.FLOWER_SPIRIT_BOOTS);

                            // 7. 饰品（装了 Trinkets 才显示）
                            if (FabricLoader.getInstance().isModLoaded("trinkets")) {
                                try {
                                    Class<?> trinketsItems = Class.forName(
                                            "com.mytest.firstmod.integration.trinkets.TrinketsItems");
                                    Item ring = (Item) trinketsItems.getField("FLOWER_SPIRIT_RING").get(null);
                                    Item amulet = (Item) trinketsItems.getField("FLOWER_SPIRIT_AMULET").get(null);
                                    entries.add(ring);
                                    entries.add(amulet);
                                } catch (Exception ignored) {}
                            }
                        })
                        .build()
        );
    }
}
