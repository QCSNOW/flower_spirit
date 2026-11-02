package com.mytest.firstmod.block;
import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.entity.AbstractWorkBlockEntity;
import com.mytest.firstmod.block.entity.ModBlockEntities;


import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.block.entity.BlockEntity;
import net.minecraft.text.Text;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;
import net.minecraft.util.math.BlockPos;

public class ModBlocks {

    public static final Block FLOWER_SPIRIT_BLOCK;
    public static final Block FLOWER_SPIRIT_CRAFTER;

    static {
        // 普通花精方块
        FLOWER_SPIRIT_BLOCK = Registry.register(
                Registries.BLOCK,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_block"),
                new Block(AbstractBlock.Settings.create()
                        .strength(5.0F, 6.0F)
                        .requiresTool())
        );

        // 花精制作台：用具体子类继承 AbstractWorkBlock，避免抽象类直接 new
        FLOWER_SPIRIT_CRAFTER = Registry.register(
                Registries.BLOCK,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_crafter"),
                new FlowerSpiritCrafterBlock(AbstractBlock.Settings.create()
                        .strength(2.0F, 6.0F)
                        .nonOpaque()
                        .requiresTool())
        );
    }

    public static void registerAll() {
        // 触发静态注册
    }

    // 花精制作台专属具体方块类
    private static class FlowerSpiritCrafterBlock extends AbstractWorkBlock {

        public FlowerSpiritCrafterBlock(Settings settings) {
            super(settings);
        }

        @Override
        public BlockEntity createBlockEntity(BlockPos pos, BlockState state) {
            return new AbstractWorkBlockEntity(
                    ModBlockEntities.FLOWER_CRAFTER,
                    pos,
                    state,
                    Text.translatable("block.firstmod.flower_spirit_crafter")
            );
        }
    }
}
