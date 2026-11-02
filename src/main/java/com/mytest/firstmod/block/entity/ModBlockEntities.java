package com.mytest.firstmod.block.entity;
import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.ModBlocks;


import net.minecraft.block.entity.BlockEntityType;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public class ModBlockEntities {

    public static BlockEntityType<AbstractWorkBlockEntity> FLOWER_CRAFTER;

    public static void registerAll() {
        FLOWER_CRAFTER = Registry.register(
                Registries.BLOCK_ENTITY_TYPE,
                new Identifier(Firstmod.MOD_ID, "flower_spirit_crafter"),
                BlockEntityType.Builder.create(
                        (pos, state) -> new AbstractWorkBlockEntity(
                                FLOWER_CRAFTER,
                                pos,
                                state,
                                Text.translatable("block.firstmod.flower_spirit_crafter")
                        ),
                        ModBlocks.FLOWER_SPIRIT_CRAFTER
                ).build(null)
        );
    }
}
