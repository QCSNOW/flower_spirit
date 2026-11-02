package com.mytest.firstmod.integration.trinkets;

import com.google.common.collect.HashMultimap;
import com.google.common.collect.Multimap;
import dev.emi.trinkets.api.SlotReference;
import dev.emi.trinkets.api.TrinketItem;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.attribute.EntityAttribute;
import net.minecraft.entity.attribute.EntityAttributeModifier;
import net.minecraft.item.ItemStack;
import net.minecraft.nbt.NbtCompound;

import java.util.UUID;

/**
 * 繁花吊坠
 * 项链槽位：生命值低于 50% 时，获得 12 点伤害吸收护盾，冷却 45 秒
 */
public class FlowerSpiritAmuletItem extends TrinketItem {

    private static final float ABSORPTION_AMOUNT = 12.0f;
    private static final int COOLDOWN_TICKS = 45 * 20;
    private static final float TRIGGER_THRESHOLD = 0.5f;
    private static final String NBT_COOLDOWN = "AmuletCooldownEnd";

    public FlowerSpiritAmuletItem(Settings settings) {
        super(settings);
    }

    @Override
    public Multimap<EntityAttribute, EntityAttributeModifier> getModifiers(
            ItemStack stack, SlotReference slot, LivingEntity entity, UUID uuid) {
        Multimap<EntityAttribute, EntityAttributeModifier> map = HashMultimap.create();
        map.putAll(super.getModifiers(stack, slot, entity, uuid));
        // 吊坠是被动触发效果，无常驻属性修饰符
        return map;
    }

    @Override
    public void tick(ItemStack stack, SlotReference slot, LivingEntity entity) {
        if (entity.getWorld().isClient) return;

        long currentTick = entity.age;
        long cooldownEnd = getCooldownEnd(stack);

        if (currentTick < cooldownEnd) return;

        float healthRatio = entity.getHealth() / entity.getMaxHealth();

        if (healthRatio < TRIGGER_THRESHOLD) {
            float currentAbsorption = entity.getAbsorptionAmount();
            entity.setAbsorptionAmount(currentAbsorption + ABSORPTION_AMOUNT);
            setCooldownEnd(stack, currentTick + COOLDOWN_TICKS);
        }
    }

    private long getCooldownEnd(ItemStack stack) {
        NbtCompound nbt = stack.getNbt();
        if (nbt != null && nbt.contains(NBT_COOLDOWN)) {
            return nbt.getLong(NBT_COOLDOWN);
        }
        return 0;
    }

    private void setCooldownEnd(ItemStack stack, long tick) {
        NbtCompound nbt = stack.getOrCreateNbt();
        nbt.putLong(NBT_COOLDOWN, tick);
    }
}
