package com.mytest.firstmod.datagen;

import com.mytest.firstmod.Firstmod;
import com.mytest.firstmod.block.ModFlowerBlocks;
import com.mytest.firstmod.item.ModItems;
import net.fabricmc.fabric.api.datagen.v1.FabricDataOutput;
import net.fabricmc.fabric.api.datagen.v1.provider.FabricRecipeProvider;
import net.minecraft.block.Blocks;
import net.minecraft.data.server.recipe.RecipeJsonProvider;
import net.minecraft.data.server.recipe.ShapedRecipeJsonBuilder;
import net.minecraft.data.server.recipe.ShapelessRecipeJsonBuilder;
import net.minecraft.item.Item;
import net.minecraft.item.ItemConvertible;
import net.minecraft.item.Items;
import net.minecraft.recipe.Ingredient;
import net.minecraft.recipe.book.RecipeCategory;
import net.minecraft.registry.Registries;
import net.minecraft.registry.tag.ItemTags;
import net.minecraft.util.Identifier;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * 配方生成器。
 * 自动生成所有染料配方、装备工具配方、袋子配方等。
 * 运行：gradlew runDatagen
 */
public class ModRecipeProvider extends FabricRecipeProvider {

    // 花名 -> 染料物品的映射
    private static final Map<String, ItemConvertible> FLOWER_TO_DYE = new LinkedHashMap<>();

    static {
        FLOWER_TO_DYE.put("alstroemeria", Items.PINK_DYE);
        FLOWER_TO_DYE.put("anemone", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("aster", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("astilbe", Items.PINK_DYE);
        FLOWER_TO_DYE.put("baby_breath", Items.WHITE_DYE);
        FLOWER_TO_DYE.put("bells_of_ireland", Items.WHITE_DYE);
        FLOWER_TO_DYE.put("carnation", Items.PINK_DYE);
        FLOWER_TO_DYE.put("celosia", Items.RED_DYE);
        FLOWER_TO_DYE.put("chamomile", Items.LIGHT_GRAY_DYE);
        FLOWER_TO_DYE.put("clematis", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("dahlia", Items.RED_DYE);
        FLOWER_TO_DYE.put("dancing_lady", Items.YELLOW_DYE);
        FLOWER_TO_DYE.put("dendrobium", Items.YELLOW_DYE);
        FLOWER_TO_DYE.put("firework_chrysanthemum", Items.ORANGE_DYE);
        FLOWER_TO_DYE.put("forget_me_not", Items.LIGHT_BLUE_DYE);
        FLOWER_TO_DYE.put("gerbera", Items.ORANGE_DYE);
        FLOWER_TO_DYE.put("gloriosa", Items.ORANGE_DYE);
        FLOWER_TO_DYE.put("gomphrena", Items.MAGENTA_DYE);
        FLOWER_TO_DYE.put("hydrangea", Items.BLUE_DYE);
        FLOWER_TO_DYE.put("hypericum", Items.RED_DYE);
        FLOWER_TO_DYE.put("king_protea", Items.PINK_DYE);
        FLOWER_TO_DYE.put("lily", Items.WHITE_DYE);
        FLOWER_TO_DYE.put("lisianthus", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("lupine", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("oncidium", Items.YELLOW_DYE);
        FLOWER_TO_DYE.put("phalaenopsis", Items.MAGENTA_DYE);
        FLOWER_TO_DYE.put("pincushion", Items.ORANGE_DYE);
        FLOWER_TO_DYE.put("ping_pong_chrysanthemum", Items.LIGHT_GRAY_DYE);
        FLOWER_TO_DYE.put("ranunculus", Items.PINK_DYE);
        FLOWER_TO_DYE.put("trachymene", Items.LIGHT_BLUE_DYE);
        FLOWER_TO_DYE.put("viburnum", Items.WHITE_DYE);
        FLOWER_TO_DYE.put("violet", Items.PURPLE_DYE);
        FLOWER_TO_DYE.put("waxflower", Items.WHITE_DYE);
        FLOWER_TO_DYE.put("wintersweet", Items.YELLOW_DYE);
    }

    public ModRecipeProvider(FabricDataOutput output) {
        super(output);
    }

    @Override
    public void generate(Consumer<RecipeJsonProvider> exporter) {
        // 1. 所有花 → 对应染料的无序配方
        for (Map.Entry<String, ItemConvertible> entry : FLOWER_TO_DYE.entrySet()) {
            String flowerId = entry.getKey();
            ItemConvertible dye = entry.getValue();
            Item flowerItem = Registries.ITEM.get(new Identifier(Firstmod.MOD_ID, flowerId));

            ShapelessRecipeJsonBuilder.create(RecipeCategory.MISC, dye)
                    .input(flowerItem)
                    .criterion(hasItem(flowerItem), conditionsFromItem(flowerItem))
                    .offerTo(exporter, new Identifier(Firstmod.MOD_ID, "dye_from_" + flowerId));
        }

        // 2. 繁花收纳袋配方
        ShapedRecipeJsonBuilder.create(RecipeCategory.TOOLS, ModItems.FLOWER_BAG)
                .pattern(" S ")
                .pattern("LFL")
                .pattern(" L ")
                .input('S', Items.STRING)
                .input('L', Items.LEATHER)
                .input('F', Ingredient.fromTag(ItemTags.FLOWERS))
                .criterion(hasItem(Items.LEATHER), conditionsFromItem(Items.LEATHER))
                .offerTo(exporter);

        // 3. 花精锭配方（花精 + 铁锭 → 花精锭）
        ShapelessRecipeJsonBuilder.create(RecipeCategory.MISC, ModItems.FLOWER_SPIRIT_INGOT)
                .input(ModItems.FLOWER_SPIRIT)
                .input(Items.IRON_INGOT)
                .criterion(hasItem(ModItems.FLOWER_SPIRIT), conditionsFromItem(ModItems.FLOWER_SPIRIT))
                .offerTo(exporter);

        // 4. 花精块 → 花精锭（9个）
        offerReversibleCompactingRecipes(
                exporter,
                RecipeCategory.BUILDING_BLOCKS,
                ModItems.FLOWER_SPIRIT_INGOT,
                RecipeCategory.MISC,
                ModItems.FLOWER_SPIRIT_BLOCK_ITEM
        );

        // 5. 工具武器配方
        offerSwordRecipe(exporter, ModItems.FLOWER_SPIRIT_SWORD, ModItems.FLOWER_SPIRIT_INGOT, Items.STICK);
        offerPickaxeRecipe(exporter, ModItems.FLOWER_SPIRIT_PICKAXE, ModItems.FLOWER_SPIRIT_INGOT, Items.STICK);
        offerAxeRecipe(exporter, ModItems.FLOWER_SPIRIT_AXE, ModItems.FLOWER_SPIRIT_INGOT, Items.STICK);
        offerShovelRecipe(exporter, ModItems.FLOWER_SPIRIT_SHOVEL, ModItems.FLOWER_SPIRIT_INGOT, Items.STICK);
        offerHoeRecipe(exporter, ModItems.FLOWER_SPIRIT_HOE, ModItems.FLOWER_SPIRIT_INGOT, Items.STICK);

        // 6. 盔甲配方
        offerHelmetRecipe(exporter, ModItems.FLOWER_SPIRIT_HELMET, ModItems.FLOWER_SPIRIT_INGOT);
        offerChestplateRecipe(exporter, ModItems.FLOWER_SPIRIT_CHESTPLATE, ModItems.FLOWER_SPIRIT_INGOT);
        offerLeggingsRecipe(exporter, ModItems.FLOWER_SPIRIT_LEGGINGS, ModItems.FLOWER_SPIRIT_INGOT);
        offerBootsRecipe(exporter, ModItems.FLOWER_SPIRIT_BOOTS, ModItems.FLOWER_SPIRIT_INGOT);
    }

    // ===== 辅助方法：生成标准工具配方 =====
    private void offerSwordRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material, ItemConvertible stick) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.COMBAT, output)
                .pattern("M")
                .pattern("M")
                .pattern("S")
                .input('M', material)
                .input('S', stick)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerPickaxeRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material, ItemConvertible stick) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.TOOLS, output)
                .pattern("MMM")
                .pattern(" S ")
                .pattern(" S ")
                .input('M', material)
                .input('S', stick)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerAxeRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material, ItemConvertible stick) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.TOOLS, output)
                .pattern("MM")
                .pattern("MS")
                .pattern(" S")
                .input('M', material)
                .input('S', stick)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerShovelRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material, ItemConvertible stick) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.TOOLS, output)
                .pattern("M")
                .pattern("S")
                .pattern("S")
                .input('M', material)
                .input('S', stick)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerHoeRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material, ItemConvertible stick) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.TOOLS, output)
                .pattern("MM")
                .pattern(" S")
                .pattern(" S")
                .input('M', material)
                .input('S', stick)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerHelmetRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.COMBAT, output)
                .pattern("MMM")
                .pattern("M M")
                .input('M', material)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerChestplateRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.COMBAT, output)
                .pattern("M M")
                .pattern("MMM")
                .pattern("MMM")
                .input('M', material)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerLeggingsRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.COMBAT, output)
                .pattern("MMM")
                .pattern("M M")
                .pattern("M M")
                .input('M', material)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }

    private void offerBootsRecipe(Consumer<RecipeJsonProvider> exporter, ItemConvertible output, ItemConvertible material) {
        ShapedRecipeJsonBuilder.create(RecipeCategory.COMBAT, output)
                .pattern("M M")
                .pattern("M M")
                .input('M', material)
                .criterion(hasItem(material), conditionsFromItem(material))
                .offerTo(exporter);
    }
}
