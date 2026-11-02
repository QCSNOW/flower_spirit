package com.mytest.firstmod.recipe;
import com.mytest.firstmod.fluid.FluidTank;
import com.mytest.firstmod.fluid.ModFluids;
import com.mytest.firstmod.item.ModItems;


import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.recipe.Ingredient;
import net.minecraft.registry.tag.ItemTags;
import java.util.ArrayList;
import java.util.List;

public class WorkRecipes {
    private static final List<WorkRecipe> recipes = new ArrayList<>();

    public static void register() {
        recipes.add(new WorkRecipe(
                Ingredient.fromTag(ItemTags.FLOWERS),
                ModFluids.WATER,
                10,
                new ItemStack(ModItems.FLOWER_SPIRIT, 2)
        ));

        recipes.add(new WorkRecipe(
                Ingredient.fromTag(ItemTags.FLOWERS),
                ModFluids.HONEY,
                10,
                new ItemStack(ModItems.FLOWER_SPIRIT_INGOT, 1)
        ));
    }

    public static WorkRecipe findMatch(ItemStack flower, FluidTank tank) {
        for (WorkRecipe recipe : recipes) {
            if (recipe.matches(flower, tank)) return recipe;
        }
        return null;
    }
}
