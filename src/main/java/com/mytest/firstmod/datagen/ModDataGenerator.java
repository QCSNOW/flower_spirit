package com.mytest.firstmod.datagen;

import net.fabricmc.fabric.api.datagen.v1.DataGeneratorEntrypoint;
import net.fabricmc.fabric.api.datagen.v1.FabricDataGenerator;

/**
 * 数据生成器入口点。
 * 运行方式：gradlew runDatagen
 * 会自动生成所有 JSON 文件（配方、模型、战利品表、标签等）
 */
public class ModDataGenerator implements DataGeneratorEntrypoint {
    @Override
    public void onInitializeDataGenerator(FabricDataGenerator generator) {
        FabricDataGenerator.Pack pack = generator.createPack();

        // 配方生成
        pack.addProvider(ModRecipeProvider::new);
    }
}
