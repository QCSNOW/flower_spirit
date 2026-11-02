package com.mytest.firstmod.integration.trinkets;

import com.google.common.collect.HashMultimap;
import com.google.common.collect.Multimap;
import dev.emi.trinkets.api.SlotReference;
import dev.emi.trinkets.api.TrinketItem;
import net.minecraft.client.item.TooltipContext;
import net.minecraft.entity.LivingEntity;
import net.minecraft.entity.attribute.EntityAttribute;
import net.minecraft.entity.attribute.EntityAttributeModifier;
import net.minecraft.entity.attribute.EntityAttributes;
import net.minecraft.item.ItemStack;
import net.minecraft.text.Text;
import net.minecraft.util.Formatting;
import net.minecraft.world.World;

import java.util.List;
import java.util.UUID;

/**
 * 繁花之戒
 * 戒指槽位：+3 最大生命值，每12秒恢复1点生命值
 */
public class FlowerSpiritRingItem extends TrinketItem {

    private static final UUID MAX_HEALTH_UUID = UUID.fromString("a1b2c3d4-e5f6-7890-abcd-ef1234567890");
    private static final int HEAL_INTERVAL = 240; // 12秒 = 240tick

    public FlowerSpiritRingItem(Settings settings) {
        super(settings);
    }

    @Override
    public Multimap<EntityAttribute, EntityAttributeModifier> getModifiers(
            ItemStack stack, SlotReference slot, LivingEntity entity, UUID uuid) {

        Multimap<EntityAttribute, EntityAttributeModifier> map = HashMultimap.create();
        map.putAll(super.getModifiers(stack, slot, entity, uuid));

        // +3 最大生命值
        map.put(EntityAttributes.GENERIC_MAX_HEALTH,
                new EntityAttributeModifier(MAX_HEALTH_UUID, "繁花之戒生命加成",
                        3.0, EntityAttributeModifier.Operation.ADDITION));

        return map;
    }

    @Override
    public void tick(ItemStack stack, SlotReference slot, LivingEntity entity) {
        if (entity.getWorld().isClient) return;

        // 每 12 秒回 1 血（与套装再生效果独立，直接回血不加状态）
        if (entity.age % HEAL_INTERVAL == 0) {
            if (entity.getHealth() < entity.getMaxHealth()) {
                entity.setHealth(Math.min(entity.getHealth() + 1.0f, entity.getMaxHealth()));
            }
        }
    }

    @Override
    public void onEquip(ItemStack stack, SlotReference slot, LivingEntity entity) {
        if (!entity.getWorld().isClient) {
            entity.setHealth(Math.min(entity.getHealth() + 3, entity.getMaxHealth()));
        }
    }

    @Override
    public void onUnequip(ItemStack stack, SlotReference slot, LivingEntity entity) {
        if (!entity.getWorld().isClient) {
            if (entity.getHealth() > entity.getMaxHealth()) {
                entity.setHealth(entity.getMaxHealth());
            }
        }
    }
}
