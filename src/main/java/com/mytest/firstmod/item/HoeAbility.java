package com.mytest.firstmod.item;

import net.fabricmc.fabric.api.event.player.UseBlockCallback;
import net.minecraft.block.*;
import net.minecraft.entity.player.PlayerEntity;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ActionResult;
import net.minecraft.util.Hand;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import java.util.HashSet;
import java.util.Set;

public class HoeAbility {
    //简单冷却，防止短时间疯狂触发卡顿
    private static final int COOLDOWN_TICKS = 8;

    public static void registerAbility() {
        //使用方块事件：玩家右键方块触发
        UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
            ItemStack stack = player.getStackInHand(hand);
            BlockPos clickPos = hitResult.getBlockPos();
            BlockState clickState = world.getBlockState(clickPos);
            Block clickBlock = clickState.getBlock();

            //客户端直接放行，逻辑全部服务端
            if (world.isClient()) {
                return ActionResult.PASS;
            }
            //不是花精锄直接跳过
            if (stack.getItem() != ModItems.FLOWER_SPIRIT_HOE) {
                return ActionResult.PASS;
            }
            //冷却判断，防止疯狂点击造成卡顿
            if(player.getItemCooldownManager().isCoolingDown(stack.getItem())){
                return ActionResult.PASS;
            }

            //判断点击的方块是否属于可收割目标，成熟农作物 / 花 /蕨 /高花 /树苗
            boolean validTarget = false;
            if(clickBlock instanceof CropBlock crop){
                if(crop.isMature(clickState)) validTarget = true;
            }
            if(clickBlock instanceof FlowerBlock
                    || clickBlock instanceof FernBlock
                    || clickBlock instanceof TallPlantBlock
                    || clickBlock instanceof SaplingBlock){
                validTarget = true;
            }
            //西瓜、南瓜、可可豆、甘蔗、仙人掌（已移除下界疣）
            if(clickBlock instanceof MelonBlock
                    || clickBlock instanceof PumpkinBlock
                    || clickBlock instanceof CocoaBlock
                    || clickBlock instanceof SugarCaneBlock
                    || clickBlock instanceof CactusBlock){
                validTarget = true;
            }

            if(!validTarget){
                return ActionResult.PASS;
            }

            // ========== 以点击方块clickPos为中心，XZ平面3×3范围，Y不变 ==========
            int brokenCount = 0;
            int range = 1;
            //记录本次已经处理过的方块，避免同一轮重复处理同一个pos
            Set<BlockPos> handledPos = new HashSet<>();

            for(int dx = -range; dx <= range; dx++){
                for(int dz = -range; dz <= range; dz++){
                    BlockPos pos = clickPos.add(dx,0,dz);
                    //已经处理过直接跳过
                    if(handledPos.contains(pos)) continue;

                    BlockState state = world.getBlockState(pos);
                    Block block = state.getBlock();

                    //普通农作物（小麦土豆胡萝卜）
                    if(block instanceof CropBlock cropBlock){
                        if(cropBlock.isMature(state)){
                            world.breakBlock(pos,true);
                            world.setBlockState(pos,cropBlock.withAge(0));
                            handledPos.add(pos);
                            brokenCount++;
                        }
                        continue;
                    }

                    //可可豆：成熟重置为0
                    if(block instanceof CocoaBlock cocoa){
                        int age = state.get(CocoaBlock.AGE);
                        if(age >= 2){
                            world.breakBlock(pos,true);
                            world.setBlockState(pos,state.with(CocoaBlock.AGE,0));
                            handledPos.add(pos);
                            brokenCount++;
                        }
                        continue;
                    }

                    //西瓜、南瓜：直接破坏方块，本体消失
                    if(block instanceof MelonBlock || block instanceof PumpkinBlock){
                        world.breakBlock(pos,true);
                        handledPos.add(pos);
                        brokenCount++;
                        continue;
                    }

                    //甘蔗、仙人掌：整方块破坏
                    if(block instanceof SugarCaneBlock || block instanceof CactusBlock){
                        world.breakBlock(pos,true);
                        handledPos.add(pos);
                        brokenCount++;
                        continue;
                    }

                    //花草树苗
                    boolean isPlant = block instanceof FlowerBlock
                            || block instanceof FernBlock
                            || block instanceof TallPlantBlock
                            || block instanceof SaplingBlock;
                    if(isPlant){
                        world.breakBlock(pos,true);
                        handledPos.add(pos);
                        brokenCount++;
                    }
                }
            }

            if(brokenCount > 0){
                //扣耐久
                stack.damage(brokenCount,player,p->p.sendToolBreakStatus(hand));
                //疲劳消耗
                player.addExhaustion(0.025F * brokenCount);
                //设置物品冷却，防止连续疯狂点击卡顿
                player.getItemCooldownManager().set(stack.getItem(),COOLDOWN_TICKS);
            }

            return ActionResult.SUCCESS;
        });
    }
}
