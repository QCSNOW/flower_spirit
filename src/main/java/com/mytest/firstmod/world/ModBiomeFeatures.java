package com.mytest.firstmod.world;
import com.mytest.firstmod.Firstmod;


import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.minecraft.registry.RegistryKey;
import net.minecraft.registry.RegistryKeys;
import net.minecraft.util.Identifier;
import net.minecraft.world.biome.Biome;
import net.minecraft.world.biome.BiomeKeys;
import net.minecraft.world.gen.GenerationStep;
import net.minecraft.world.gen.feature.PlacedFeature;

import java.util.ArrayList;
import java.util.List;

/**
 * 花朵世界生成
 * 按群系类型分组：每组共享一个生成roll，roll到了再从组内随机选一种花
 * 大幅降低花朵密度，同时保持花的多样性
 */
public class ModBiomeFeatures {

    // 花朵密集群系：这些群系里花的生成密度更高
    @SuppressWarnings("unchecked")
    private static final RegistryKey<Biome>[] DENSE_BIOMES = new RegistryKey[] {
        BiomeKeys.FLOWER_FOREST,
        BiomeKeys.MEADOW,
        BiomeKeys.CHERRY_GROVE,
        BiomeKeys.SUNFLOWER_PLAINS,
    };

    // 9个群系组，每个组对应一个 flower_group_xxx 的 placed_feature
    private static final String[] BIOME_GROUPS = {
        "PLAINS", "FOREST", "SWAMP", "SAVANNA", "JUNGLE",
        "DESERT", "WINDSWEPT_HILLS", "TAIGA", "RIVER"
    };

    public static void registerAll() {
        for (String biomeType : BIOME_GROUPS) {
            String groupName = biomeType.toLowerCase();

            RegistryKey<PlacedFeature> normalKey = RegistryKey.of(
                    RegistryKeys.PLACED_FEATURE,
                    new Identifier(Firstmod.MOD_ID, "flower_group_" + groupName)
            );
            RegistryKey<PlacedFeature> denseKey = RegistryKey.of(
                    RegistryKeys.PLACED_FEATURE,
                    new Identifier(Firstmod.MOD_ID, "flower_group_" + groupName + "_dense")
            );

            BiomeGroup group = getBiomeGroup(biomeType);
            if (group == null) continue;

            // 普通群系：普通密度
            if (!group.normalBiomes.isEmpty()) {
                BiomeModifications.addFeature(
                        BiomeSelectors.includeByKey(group.normalBiomes),
                        GenerationStep.Feature.VEGETAL_DECORATION,
                        normalKey
                );
            }

            // 花朵密集群系：高密度版本
            if (!group.denseBiomes.isEmpty()) {
                BiomeModifications.addFeature(
                        BiomeSelectors.includeByKey(group.denseBiomes),
                        GenerationStep.Feature.VEGETAL_DECORATION,
                        denseKey
                );
            }
        }
    }

    private static class BiomeGroup {
        final List<RegistryKey<Biome>> normalBiomes;
        final List<RegistryKey<Biome>> denseBiomes;

        BiomeGroup(List<RegistryKey<Biome>> normalBiomes, List<RegistryKey<Biome>> denseBiomes) {
            this.normalBiomes = normalBiomes;
            this.denseBiomes = denseBiomes;
        }
    }

    private static boolean isDenseBiome(RegistryKey<Biome> key) {
        for (RegistryKey<Biome> dense : DENSE_BIOMES) {
            if (dense.equals(key)) return true;
        }
        return false;
    }

    @SafeVarargs
    private static BiomeGroup splitDense(RegistryKey<Biome>... allBiomes) {
        List<RegistryKey<Biome>> normal = new ArrayList<>();
        List<RegistryKey<Biome>> dense = new ArrayList<>();
        for (RegistryKey<Biome> key : allBiomes) {
            if (isDenseBiome(key)) dense.add(key);
            else normal.add(key);
        }
        return new BiomeGroup(normal, dense);
    }

    private static BiomeGroup getBiomeGroup(String type) {
        switch (type) {
            case "PLAINS":
                return splitDense(
                        BiomeKeys.PLAINS,
                        BiomeKeys.SUNFLOWER_PLAINS,
                        BiomeKeys.MEADOW
                );
            case "FOREST":
                return splitDense(
                        BiomeKeys.FOREST,
                        BiomeKeys.FLOWER_FOREST,
                        BiomeKeys.BIRCH_FOREST,
                        BiomeKeys.OLD_GROWTH_BIRCH_FOREST,
                        BiomeKeys.DARK_FOREST
                );
            case "SWAMP":
                return splitDense(
                        BiomeKeys.SWAMP,
                        BiomeKeys.MANGROVE_SWAMP
                );
            case "JUNGLE":
                return splitDense(
                        BiomeKeys.JUNGLE,
                        BiomeKeys.BAMBOO_JUNGLE,
                        BiomeKeys.SPARSE_JUNGLE
                );
            case "SAVANNA":
                return splitDense(
                        BiomeKeys.SAVANNA,
                        BiomeKeys.SAVANNA_PLATEAU,
                        BiomeKeys.WINDSWEPT_SAVANNA
                );
            case "DESERT":
                return splitDense(
                        BiomeKeys.DESERT
                );
            case "WINDSWEPT_HILLS":
                return splitDense(
                        BiomeKeys.WINDSWEPT_HILLS,
                        BiomeKeys.WINDSWEPT_GRAVELLY_HILLS,
                        BiomeKeys.WINDSWEPT_FOREST,
                        BiomeKeys.CHERRY_GROVE
                );
            case "TAIGA":
                return splitDense(
                        BiomeKeys.TAIGA,
                        BiomeKeys.SNOWY_TAIGA,
                        BiomeKeys.OLD_GROWTH_PINE_TAIGA,
                        BiomeKeys.OLD_GROWTH_SPRUCE_TAIGA
                );
            case "RIVER":
                return splitDense(
                        BiomeKeys.RIVER,
                        BiomeKeys.FROZEN_RIVER
                );
            default:
                return null;
        }
    }
}
