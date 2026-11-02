package com.mytest.firstmod.integration;

import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.config.ModConfig;
import com.terraformersmc.modmenu.api.ConfigScreenFactory;
import com.terraformersmc.modmenu.api.ModMenuApi;
import me.shedaniel.clothconfig2.api.ConfigBuilder;
import me.shedaniel.clothconfig2.api.ConfigCategory;
import me.shedaniel.clothconfig2.api.ConfigEntryBuilder;
import net.minecraft.text.Text;

/**
 * Mod Menu 集成 + Cloth Config 配置界面。
 *
 * 启用方法：
 * 1. 从 PCL2 下载 Mod Menu 和 Cloth Config 的 jar，放到项目 libs/ 目录
 * 2. 在 build.gradle 里取消 Mod Menu + Cloth Config 的依赖注释
 * 3. 在 build.gradle 里取消 optional 源集的注释
 * 4. 在 fabric.mod.json 的 entrypoints 里取消 modmenu 的注释
 *
 * 玩家打开 Mods → 繁花物语 → 配置按钮，就能看到这个界面。
 */
public class ModMenuIntegration implements ModMenuApi {

    @Override
    public ConfigScreenFactory<?> getModConfigScreenFactory() {
        return parent -> {
            ModConfig config = ModConfig.getInstance();

            ConfigBuilder builder = ConfigBuilder.create()
                    .setParentScreen(parent)
                    .setTitle(Text.literal("繁花物语 - 配置"));

            ConfigEntryBuilder entryBuilder = builder.entryBuilder();

            // ===== 花朵袋子设置 =====
            ConfigCategory bagCategory = builder.getOrCreateCategory(Text.literal("花朵袋子"));

            bagCategory.addEntry(entryBuilder
                    .startIntSlider(Text.literal("袋子容量（格）"), config.bagSize, 9, 108)
                    .setTooltip(Text.literal("花朵袋子的总格子数，默认 54 格"))
                    .setSaveConsumer(value -> config.bagSize = value)
                    .setDefaultValue(54)
                    .build());

            bagCategory.addEntry(entryBuilder
                    .startBooleanToggle(Text.literal("默认开启自动吸取"), config.bagAutoSuck)
                    .setTooltip(Text.literal("新拿到的袋子是否默认开启自动吸取花朵"))
                    .setSaveConsumer(value -> config.bagAutoSuck = value)
                    .setDefaultValue(true)
                    .build());

            // ===== 工具装备设置 =====
            ConfigCategory toolCategory = builder.getOrCreateCategory(Text.literal("工具装备"));

            toolCategory.addEntry(entryBuilder
                    .startFloatSlider(Text.literal("花精工具伤害加成"), config.toolDamageBonus, 0f, 10f)
                    .setTooltip(Text.literal("花精系列工具武器的额外伤害加成"))
                    .setSaveConsumer(value -> config.toolDamageBonus = value)
                    .setDefaultValue(2.0f)
                    .build());

            // ===== 世界生成 =====
            ConfigCategory worldCategory = builder.getOrCreateCategory(Text.literal("世界生成"));

            worldCategory.addEntry(entryBuilder
                    .startFloatSlider(Text.literal("花的生成密度倍率"), config.flowerDensityMultiplier, 0.1f, 5f)
                    .setTooltip(Text.literal("调整模组花朵在世界中的生成密度，1.0 为默认值"))
                    .setSaveConsumer(value -> config.flowerDensityMultiplier = value)
                    .setDefaultValue(1.0f)
                    .build());

            // ===== 视觉效果 =====
            ConfigCategory visualCategory = builder.getOrCreateCategory(Text.literal("视觉效果"));

            visualCategory.addEntry(entryBuilder
                    .startBooleanToggle(Text.literal("花的粒子效果"), config.flowerParticles)
                    .setTooltip(Text.literal("是否显示花的随机粒子效果"))
                    .setSaveConsumer(value -> config.flowerParticles = value)
                    .setDefaultValue(true)
                    .build());

            // 保存回调
            builder.setSavingRunnable(() -> {
                ModConfig.save();
                Firstmod.LOGGER.info("配置已保存");
            });

            return builder.build();
        };
    }
}
