package com.mytest.firstmod.item;

import net.minecraft.item.ToolMaterial;
import net.minecraft.recipe.Ingredient;

public class ModToolMaterials {

    // 花精工具材料，属性完全对标钻石工具
    public static final ToolMaterial FLOWER_SPIRIT_MATERIAL = new ToolMaterial() {

        /**
         * 挖掘等级：3 对应钻石级，可挖掘黑曜石等方块
         */
        @Override
        public int getMiningLevel() {
            return 3;
        }

        /**
         * 耐久度：二倍铁制为 500
         */
        @Override
        public int getDurability() {
            return 500;
        }

        /**
         * 挖掘速度倍率：强于铁为 7.0
         */
        @Override
        public float getMiningSpeedMultiplier() {
            return 7.0F;
        }

        /**
         * 攻击伤害加成：同铁工具基础加成为 2.0
         */
        @Override
        public float getAttackDamage() {
            return 2.0F;
        }

        /**
         * 附魔能力：同钻石为 10
         */
        @Override
        public int getEnchantability() {
            return 10;
        }

        /**
         * 铁砧修复材料：花精锭
         */
        @Override
        public Ingredient getRepairIngredient() {
            return Ingredient.ofItems(ModItems.FLOWER_SPIRIT_INGOT);
        }
    };
}
