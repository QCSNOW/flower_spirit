package com.mytest.firstmod.recipe;
import com.mytest.firstmod.fluid.FluidTank;
import com.mytest.firstmod.fluid.FluidType;


import net.minecraft.item.ItemStack;
import net.minecraft.recipe.Ingredient;

public class WorkRecipe {
    private final Ingredient input;
    private final FluidType fluid;
    private final int fluidAmount;
    private final ItemStack output;

    public WorkRecipe(Ingredient input, FluidType fluid, int fluidAmount, ItemStack output) {
        this.input = input;
        this.fluid = fluid;
        this.fluidAmount = fluidAmount;
        this.output = output;
    }

    public boolean matches(ItemStack flowerStack, FluidTank tank) {
        return !flowerStack.isEmpty() && input.test(flowerStack) && tank.getFluidAmount(fluid) > 0;
    }

    public Ingredient getInput() { return input; }
    public FluidType getFluid() { return fluid; }
    public int getFluidAmount() { return fluidAmount; }
    public ItemStack getOutput() { return output; }
}
