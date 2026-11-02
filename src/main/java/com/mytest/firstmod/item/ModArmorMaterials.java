package com.mytest.firstmod.item;
import com.mytest.firstmod.Firstmod;


import net.minecraft.item.ArmorItem;
import net.minecraft.item.ArmorMaterial;
import net.minecraft.recipe.Ingredient;
import net.minecraft.sound.SoundEvent;
import net.minecraft.sound.SoundEvents;

public class ModArmorMaterials {

    // 花精盔甲材料，属性对标原版钻石套
    public static final ArmorMaterial FLOWER_SPIRIT_ARMOR = new ArmorMaterial() {

        // 各部位耐久度：头盔、胸甲、护腿、靴子
        private final int[] durabilityValues = new int[]{306, 480, 456, 384};
        // 各部位防御值：头盔、胸甲、护腿、靴子
        private final int[] protectionValues = new int[]{2, 7, 5, 2};

        /**
         * 根据盔甲部位返回对应耐久度
         */
        @Override
        public int getDurability(ArmorItem.Type type) {
            return durabilityValues[type.ordinal()];
        }

        /**
         * 根据盔甲部位返回对应防御值
         * Yarn 映射下方法名为 getProtection，对应 Mojang 映射的 getDefense
         */
        @Override
        public int getProtection(ArmorItem.Type type) {
            return protectionValues[type.ordinal()];
        }

        /**
         * 附魔能力，桶钻石套为 10
         */
        @Override
        public int getEnchantability() {
            return 10;
        }

        /**
         * 穿戴音效，复用钻石套音效
         */
        @Override
        public SoundEvent getEquipSound() {
            return SoundEvents.ITEM_ARMOR_EQUIP_DIAMOND;
        }

        /**
         * 铁砧修复材料
         */
        @Override
        public Ingredient getRepairIngredient() {
            return Ingredient.ofItems(ModItems.FLOWER_SPIRIT_INGOT);
        }

        /**
         * 【1.20.1关键】盔甲贴图依靠getName自动拼接路径！
         * 不要写getTexture！！
         * 自动寻找：
         * assets/firstmod/textures/models/armor/flower_spirit_armor_layer_1.png
         * assets/firstmod/textures/models/armor/flower_spirit_armor_layer_2.png
         */
        @Override
        public String getName() {
            return Firstmod.MOD_ID + ":flower_spirit_armor";
        }

        /**
         * 韧性属性
         */
        @Override
        public float getToughness() {
            return 0.5F;
        }

        /**
         * 抗击退属性
         */
        @Override
        public float getKnockbackResistance() {
            return 0.0F;
        }

    };
}
