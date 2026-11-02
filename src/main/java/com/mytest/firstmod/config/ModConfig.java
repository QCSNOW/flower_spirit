package com.mytest.firstmod.config;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mytest.firstmod.Firstmod;
import net.fabricmc.loader.api.FabricLoader;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;

/**
 * 模组配置存储。
 * 纯 Java 实现，不依赖第三方库。
 * 配置文件位置：.minecraft/config/firstmod.json
 *
 * 以后启用 Cloth Config 后，会自动生成配置界面。
 */
public class ModConfig {

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    private static final File CONFIG_FILE = new File(
            FabricLoader.getInstance().getConfigDir().toFile(),
            Firstmod.MOD_ID + ".json");

    // ========== 配置项 ==========

    /** 花朵袋子默认容量（格数） */
    public int bagSize = 54;

    /** 花朵袋子默认是否开启自动吸取 */
    public boolean bagAutoSuck = true;

    /** 花精工具的攻击伤害加成 */
    public float toolDamageBonus = 2.0f;

    /** 是否显示花的粒子效果 */
    public boolean flowerParticles = true;

    /** 世界生成的花密度倍率（0.5=一半，2.0=两倍） */
    public float flowerDensityMultiplier = 1.0f;

    // ========== 读写方法 ==========

    private static ModConfig instance;

    public static ModConfig getInstance() {
        if (instance == null) {
            load();
        }
        return instance;
    }

    public static void load() {
        if (CONFIG_FILE.exists()) {
            try (FileReader reader = new FileReader(CONFIG_FILE)) {
                instance = GSON.fromJson(reader, ModConfig.class);
            } catch (Exception e) {
                Firstmod.LOGGER.error("读取配置文件失败，使用默认配置", e);
                instance = new ModConfig();
            }
        } else {
            instance = new ModConfig();
            save();
        }
    }

    public static void save() {
        try {
            CONFIG_FILE.getParentFile().mkdirs();
            try (FileWriter writer = new FileWriter(CONFIG_FILE)) {
                GSON.toJson(instance, writer);
            }
        } catch (Exception e) {
            Firstmod.LOGGER.error("保存配置文件失败", e);
        }
    }
}
