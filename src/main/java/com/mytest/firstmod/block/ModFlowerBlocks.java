package com.mytest.firstmod.block;
import com.mytest.firstmod.Firstmod;


import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.block.FlowerBlock;
import net.minecraft.entity.effect.StatusEffects;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.sound.BlockSoundGroup;
import net.minecraft.util.Identifier;

import java.util.LinkedHashMap;
import java.util.Map;

public class ModFlowerBlocks {
    public static final Map<String, Block> FLOWERS = new LinkedHashMap<>();

    private static final String[] NORMAL_FLOWER_IDS = {
        "lisianthus", "carnation", "hydrangea", "lily", "dahlia", "gerbera",
        "ping_pong_chrysanthemum", "firework_chrysanthemum", "violet", "astilbe",
        "trachymene", "ranunculus", "wintersweet", "waxflower", "pincushion",
        "king_protea", "hypericum", "anemone", "alstroemeria", "chamomile",
        "baby_breath", "viburnum", "forget_me_not", "gomphrena",
        "celosia", "lupine", "aster", "clematis", "bells_of_ireland",
        "gloriosa", "oncidium", "dancing_lady", "phalaenopsis", "dendrobium"
    };

    static {
        // Register normal FlowerBlock flowers
        for (String id : NORMAL_FLOWER_IDS) {
            Block block = Registry.register(
                    Registries.BLOCK,
                    new Identifier(Firstmod.MOD_ID, id),
                    new FlowerBlock(
                            StatusEffects.REGENERATION,
                            0,
                            AbstractBlock.Settings.create()
                                    .nonOpaque()
                                    .breakInstantly()
                                    .noCollision()
                                    .ticksRandomly()
                                    .sounds(BlockSoundGroup.GRASS)
                    )
            );
            FLOWERS.put(id, block);
        }
    }

    public static void registerAll() {
    }
}
