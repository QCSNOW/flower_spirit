package com.mytest.firstmod.client;

import com.mytest.firstmod.block.ModBlocks;
import com.mytest.firstmod.block.ModFlowerBlocks;
import com.mytest.firstmod.block.entity.ModBlockEntities;
import com.mytest.firstmod.client.render.WorkBlockEntityRenderer;
import com.mytest.firstmod.client.screen.FlowerBagScreen;
import com.mytest.firstmod.client.screen.WorkBlockScreen;
import com.mytest.firstmod.screen.ModScreenHandlers;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.blockrenderlayer.v1.BlockRenderLayerMap;
import net.fabricmc.fabric.api.client.item.v1.ItemTooltipCallback;
import net.fabricmc.fabric.api.client.rendering.v1.BlockEntityRendererRegistry;
import net.fabricmc.fabric.api.client.screenhandler.v1.ScreenRegistry;
import net.minecraft.block.Block;
import net.minecraft.client.render.RenderLayer;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;
import net.minecraft.util.Identifier;
import net.minecraft.registry.Registries;

import java.util.List;

/**
 * 客户端初始化
 */
public class FirstmodClient implements ClientModInitializer {

    private static final String RING_ID = "firstmod:flower_spirit_ring";
    private static final String AMULET_ID = "firstmod:flower_spirit_amulet";

    // 自定义相位，确保在 Trinkets 之后执行（这样才能删掉 Trinkets 加的描述）
    private static final Identifier TOOLTIP_PHASE = new Identifier("firstmod", "tooltip_post");

    @Override
    public void onInitializeClient() {
        // 注册花朵方块的 cutout 渲染类型（解决黑底问题）
        for (Block flower : ModFlowerBlocks.FLOWERS.values()) {
            BlockRenderLayerMap.INSTANCE.putBlock(flower, RenderLayer.getCutout());
        }

        // 花精制作台使用 cutout 渲染类型（玻璃罩透明）
        BlockRenderLayerMap.INSTANCE.putBlock(ModBlocks.FLOWER_SPIRIT_CRAFTER, RenderLayer.getCutout());

        // 注册花精制作台 GUI
        ScreenRegistry.register(
                ModScreenHandlers.GENERIC_WORK_TYPE,
                WorkBlockScreen::new
        );

        // 注册花精制作台方块实体渲染器（内底面、流体等）
        BlockEntityRendererRegistry.register(
                ModBlockEntities.FLOWER_CRAFTER,
                WorkBlockEntityRenderer::new
        );

        // 注册繁花收纳袋 GUI
        ScreenRegistry.register(
                ModScreenHandlers.FLOWER_BAG_SCREEN_HANDLER,
                FlowerBagScreen::new
        );

        // 饰品 tooltip 定制（在默认相位之后执行，确保 Trinkets 先加完我们再改）
        ItemTooltipCallback.EVENT.addPhaseOrdering(
                new Identifier("fabric", "default"),
                TOOLTIP_PHASE
        );
        ItemTooltipCallback.EVENT.register(TOOLTIP_PHASE, (stack, context, lines) -> {
            Identifier id = Registries.ITEM.getId(stack.getItem());
            if (id == null) return;
            String idStr = id.toString();

            if (RING_ID.equals(idStr)) {
                modifyRingTooltip(lines);
            } else if (AMULET_ID.equals(idStr)) {
                modifyAmuletTooltip(lines);
            }
        });
    }

    /**
     * 戒指 tooltip：删除所有 Trinkets 自动加的装备描述，换成我们自定义的
     */
    private void modifyRingTooltip(List<Text> lines) {
        removeAllEquipSections(lines);
        lines.add(Text.literal(""));
        lines.add(Text.literal("装备时：").formatted(Formatting.GRAY));
        lines.add(Text.literal("  +3 最大生命值").formatted(Formatting.BLUE));
        lines.add(Text.literal("  +0.1 再生力（每12秒回复1生命）").formatted(Formatting.BLUE));
    }

    /**
     * 吊坠 tooltip：删除所有 Trinkets 自动加的装备描述，换成我们自定义的
     */
    private void modifyAmuletTooltip(List<Text> lines) {
        removeAllEquipSections(lines);
        lines.add(Text.literal(""));
        lines.add(Text.literal("装备时：").formatted(Formatting.GRAY));
        lines.add(Text.literal("  生命值低于50%时获得12点伤害吸收护盾").formatted(Formatting.BLUE));
        lines.add(Text.literal("  冷却时间：45秒").formatted(Formatting.BLUE));
    }

    /**
     * 彻底删除所有"装备时："相关的段落（包括 Trinkets 加的各种属性行）
     */
    private void removeAllEquipSections(List<Text> lines) {
        int i = lines.size() - 1;
        while (i >= 0) {
            String text = lines.get(i).getString();
            if (isEquipTitle(text)) {
                int start = i;
                int end = i + 1;
                while (end < lines.size()) {
                    String s = lines.get(end).getString().trim();
                    if (s.isEmpty()) break;
                    if (!s.startsWith("+") && !s.startsWith("＋") && !containsAttributeKeyword(s)) break;
                    end++;
                }
                for (int j = end - 1; j >= start; j--) {
                    lines.remove(j);
                }
                i = start - 1;
            } else {
                i--;
            }
        }
        while (!lines.isEmpty() && lines.get(lines.size() - 1).getString().isEmpty()) {
            lines.remove(lines.size() - 1);
        }
    }

    private boolean isEquipTitle(String text) {
        String trimmed = text.trim();
        return trimmed.equals("装备时：") ||
               trimmed.equals("装备时:") ||
               trimmed.equals("When equipped:") ||
               trimmed.equals("When equipped") ||
               trimmed.contains("装备时") ||
               trimmed.contains("When equipped");
    }

    private boolean containsAttributeKeyword(String s) {
        return s.contains("最大生命") || s.contains("health") ||
               s.contains("攻击") || s.contains("attack") ||
               s.contains("防御") || s.contains("defense") ||
               s.contains("速度") || s.contains("speed") ||
               s.contains("伤害吸收") || s.contains("absorption") ||
               s.contains("再生") || s.contains("regen");
    }
}
