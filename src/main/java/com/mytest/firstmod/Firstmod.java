package com.mytest.firstmod;
import com.mytest.firstmod.block.ModBlocks;
import com.mytest.firstmod.block.ModFlowerBlocks;
import com.mytest.firstmod.block.entity.ModBlockEntities;
import com.mytest.firstmod.item.HoeAbility;
import com.mytest.firstmod.item.ModItemEffects;
import com.mytest.firstmod.item.ModItemGroups;
import com.mytest.firstmod.item.ModItems;
import com.mytest.firstmod.networking.ModNetworking;
import com.mytest.firstmod.recipe.WorkRecipes;
import com.mytest.firstmod.screen.ModScreenHandlers;
import com.mytest.firstmod.world.ModBiomeFeatures;
import com.mytest.firstmod.config.ModConfig;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.loader.api.FabricLoader;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Firstmod implements ModInitializer {
	public static final String MOD_ID = "firstmod";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		ModBlocks.registerAll();
		ModFlowerBlocks.registerAll();
		ModBlockEntities.registerAll();
		ModScreenHandlers.registerAll();
		ModItems.registerAll();

		WorkRecipes.register();
		ModNetworking.registerServerReceivers();
		ModBiomeFeatures.registerAll();

		ModItemGroups.registerAll();
		ModItemEffects.register();
		HoeAbility.registerAbility();

		// 加载配置（纯 Java 实现，无依赖）
		ModConfig.load();

		// 饰品栏集成（可选：装了 Trinkets 才启用）
		if (FabricLoader.getInstance().isModLoaded("trinkets")) {
			try {
				Class.forName("com.mytest.firstmod.integration.trinkets.TrinketsItems")
						.getMethod("init").invoke(null);
				LOGGER.info("繁花物语：Trinkets 饰品栏集成已启用");
			} catch (Exception e) {
				LOGGER.error("繁花物语：Trinkets 集成初始化失败", e);
			}
		}

		LOGGER.info("繁花物语：13个花精系列物品全部注册完成！");
	}
}
