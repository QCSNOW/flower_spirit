package com.mytest.firstmod.client.screen;

import com.mytest.firstmod.block.entity.AbstractWorkBlockEntity;
import com.mytest.firstmod.fluid.FluidTank;
import com.mytest.firstmod.fluid.FluidType;
import com.mytest.firstmod.fluid.ModFluids;
import com.mytest.firstmod.networking.ModNetworking;
import com.mytest.firstmod.screen.ModScreenHandlers;

import com.mojang.blaze3d.systems.RenderSystem;
import net.fabricmc.fabric.api.client.networking.v1.ClientPlayNetworking;
import net.fabricmc.fabric.api.networking.v1.PacketByteBufs;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.ingame.HandledScreen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.item.ItemStack;
import net.minecraft.item.Items;
import net.minecraft.network.PacketByteBuf;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

import java.util.ArrayList;
import java.util.List;

public class WorkBlockScreen extends HandledScreen<ModScreenHandlers.GenericWorkScreenHandler> {

    private static final int GUI_WIDTH = 176;
    private static final int GUI_HEIGHT = 200;
    private static final int PLAYER_INV_Y = 118;

    private static final int FLUID_BAR_X = 12, FLUID_BAR_Y = 18, FLUID_BAR_W = 12, FLUID_BAR_H = 44;
    private static final int LAYER_X = 28, LAYER_Y = 32, LAYER_H = 10, LAYER_W = 108;
    private static final int UP_DOWN_X = 140;

    private static final int POUR_BTN_X = 4;
    private static final int POUR_BTN_Y = 94;
    private static final int POUR_BTN_W = 50;
    private static final int POUR_BTN_H = 16;

    private ButtonWidget pourButton;
    private ButtonWidget upButton;
    private ButtonWidget downButton;

    private long lastClickTime = 0;
    private int lastClickedLayer = -1;
    private static final long DOUBLE_CLICK_MS = 500;

    private String buttonText = "存液/取液";

    public WorkBlockScreen(ModScreenHandlers.GenericWorkScreenHandler handler,
                           PlayerInventory inventory,
                           Text title) {
        super(handler, inventory, title);
        this.backgroundWidth = GUI_WIDTH;
        this.backgroundHeight = GUI_HEIGHT;
        this.playerInventoryTitleY = 106;
    }

    @Override
    protected void init() {
        super.init();

        pourButton = addDrawableChild(ButtonWidget.builder(
                Text.empty(),
                button -> sendPourAction()
        ).dimensions(this.x + POUR_BTN_X, this.y + POUR_BTN_Y, POUR_BTN_W, POUR_BTN_H).build());

        upButton = addDrawableChild(ButtonWidget.builder(
                Text.literal("\u2191"),
                button -> sendMoveLayer(0)
        ).dimensions(this.x + UP_DOWN_X, this.y + LAYER_Y, 14, 10).build());

        downButton = addDrawableChild(ButtonWidget.builder(
                Text.literal("\u2193"),
                button -> sendMoveLayer(1)
        ).dimensions(this.x + UP_DOWN_X, this.y + LAYER_Y + 12, 14, 10).build());
    }

    private void sendPourAction() {
        PacketByteBuf buf = PacketByteBufs.create();
        buf.writeInt(handler.getSyncId());
        ClientPlayNetworking.send(ModNetworking.POUR_ACTION, buf);
    }

    private void sendSelectLayer(int layerIndex) {
        PacketByteBuf buf = PacketByteBufs.create();
        buf.writeInt(handler.getSyncId());
        buf.writeInt(layerIndex);
        ClientPlayNetworking.send(ModNetworking.SELECT_LAYER, buf);
    }

    private void sendMoveLayer(int direction) {
        PacketByteBuf buf = PacketByteBufs.create();
        buf.writeInt(handler.getSyncId());
        buf.writeInt(direction);
        ClientPlayNetworking.send(ModNetworking.MOVE_LAYER, buf);
    }

    // ==================== Mouse handling ====================

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        int layer = getLayerAt(mouseX, mouseY);
        if (layer >= 0) {
            long now = System.currentTimeMillis();
            if (layer == lastClickedLayer && now - lastClickTime < DOUBLE_CLICK_MS) {
                sendSelectLayer(layer);
                lastClickedLayer = -1;
                return true;
            }
            lastClickedLayer = layer;
            lastClickTime = now;
        } else {
            lastClickedLayer = -1;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    private int getLayerAt(double mouseX, double mouseY) {
        int rx = (int) (mouseX - this.x);
        int ry = (int) (mouseY - this.y);
        if (rx < LAYER_X || rx > LAYER_X + LAYER_W || ry < LAYER_Y || ry > LAYER_Y + LAYER_H * 4) return -1;
        int idx = (ry - LAYER_Y) / LAYER_H;
        int count = handler.getProperty(AbstractWorkBlockEntity.PROP_LAYER_COUNT);
        if (idx >= 0 && idx < count && idx < AbstractWorkBlockEntity.PROP_MAX_LAYERS) return idx;
        return -1;
    }

    // ==================== Rendering ====================

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        updateButtonState();
        this.renderBackground(context);
        super.render(context, mouseX, mouseY, delta);
        drawButtonText(context);
        this.drawMouseoverTooltip(context, mouseX, mouseY);

        // 按钮 tooltip
        drawButtonTooltips(context, mouseX, mouseY);
    }

    @Override
    protected void drawBackground(DrawContext context, float delta, int mouseX, int mouseY) {
        int x = this.x;
        int y = this.y;

        // 背景面板
        context.fill(x, y, x + GUI_WIDTH, y + GUI_HEIGHT, 0xFFC6C6C6);
        context.fill(x, y, x + GUI_WIDTH, y + 1, 0xFFFFFFFF);
        context.fill(x, y, x + 1, y + GUI_HEIGHT, 0xFFFFFFFF);
        context.fill(x, y + GUI_HEIGHT - 1, x + GUI_WIDTH, y + GUI_HEIGHT, 0xFF555555);
        context.fill(x + GUI_WIDTH - 1, y, x + GUI_WIDTH, y + GUI_HEIGHT, 0xFF555555);

        // 标题
        context.drawText(textRenderer, this.title, x + 8, y + 6, 0xFF404040, false);

        // 玩家背包标题
        context.drawText(textRenderer, this.playerInventoryTitle, x + 8, y + this.playerInventoryTitleY, 0xFF404040, false);

        // 槽位
        drawSlot(context, x + 12, y + 72);
        drawSlot(context, x + 70, y + 72);
        drawSlot(context, x + 116, y + 72);

        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                drawSlot(context, x + 8 + col * 18, y + PLAYER_INV_Y + row * 18);
            }
        }
        for (int col = 0; col < 9; col++) {
            drawSlot(context, x + 8 + col * 18, y + PLAYER_INV_Y + 58);
        }

        // 流体条
        drawFluidBar(context, x + FLUID_BAR_X, y + FLUID_BAR_Y);

        // 流体文本
        int total = handler.getProperty(AbstractWorkBlockEntity.PROP_TOTAL);
        String fluidText = total + "/" + FluidTank.MAX_CAPACITY + "ML";
        context.drawText(textRenderer, fluidText, x + 28, y + 20, 0xFF404040, false);

        // 层级列表
        drawLayers(context, x + LAYER_X, y + LAYER_Y);

        // 进度箭头
        int progress = handler.getProperty(AbstractWorkBlockEntity.PROP_PROGRESS);
        drawProgressArrow(context, x + 92, y + 74, (double) progress / 40.0);
    }

    private void drawButtonText(DrawContext context) {
        int tx = this.x + POUR_BTN_X + POUR_BTN_W / 2 - textRenderer.getWidth(buttonText) / 2;
        int ty = this.y + POUR_BTN_Y + (POUR_BTN_H - 8) / 2;
        context.drawText(textRenderer, buttonText, tx, ty, 0xFFFFFFFF, true);
    }

    private void drawButtonTooltips(DrawContext context, int mouseX, int mouseY) {
        if (pourButton != null && isPointInButton(mouseX, mouseY, pourButton)) {
            ItemStack bucket = handler.getSlot(0).getStack();
            List<Text> tooltip = new ArrayList<>();
            if (bucket.isOf(Items.WATER_BUCKET)) {
                tooltip.add(Text.literal("将水桶中的水倒入储罐"));
            } else if (bucket.isOf(Items.BUCKET)) {
                tooltip.add(Text.literal("用桶从储罐中取出液体"));
            } else {
                tooltip.add(Text.literal("放入水桶或空桶后使用"));
            }
            context.drawTooltip(textRenderer, tooltip, mouseX, mouseY);
        }
        if (upButton != null && upButton.visible && isPointInButton(mouseX, mouseY, upButton)) {
            List<Text> tooltip = new ArrayList<>();
            tooltip.add(Text.literal("将选中液层上移"));
            context.drawTooltip(textRenderer, tooltip, mouseX, mouseY);
        }
        if (downButton != null && downButton.visible && isPointInButton(mouseX, mouseY, downButton)) {
            List<Text> tooltip = new ArrayList<>();
            tooltip.add(Text.literal("将选中液层下移"));
            context.drawTooltip(textRenderer, tooltip, mouseX, mouseY);
        }
    }

    private boolean isPointInButton(int mouseX, int mouseY, ButtonWidget button) {
        return mouseX >= button.getX() && mouseX < button.getX() + button.getWidth()
                && mouseY >= button.getY() && mouseY < button.getY() + button.getHeight();
    }

    // ==================== Drawing helpers ====================

    private void drawSlot(DrawContext context, int x, int y) {
        context.fill(x - 1, y - 1, x + 17, y + 17, 0xFF8B8B8B);
        context.fill(x - 1, y - 1, x, y + 17, 0xFF373737);
        context.fill(x - 1, y - 1, x + 17, y, 0xFF373737);
        context.fill(x + 16, y - 1, x + 17, y + 16, 0xFFFFFFFF);
        context.fill(x - 1, y + 16, x + 16, y + 17, 0xFFFFFFFF);
        context.fill(x, y, x + 16, y + 16, 0xFF8B8B8B);
    }

    private void drawFluidBar(DrawContext context, int x, int y) {
        int w = FLUID_BAR_W;
        int h = FLUID_BAR_H;

        context.fill(x - 1, y - 1, x + w + 1, y + h + 1, 0xFF373737);
        context.fill(x, y, x + w, y + h, 0xFF1A1A2E);

        int currentBottom = y + h;
        int layerCount = handler.getProperty(AbstractWorkBlockEntity.PROP_LAYER_COUNT);
        for (int i = 0; i < layerCount && i < AbstractWorkBlockEntity.PROP_MAX_LAYERS; i++) {
            int typeId = handler.getProperty(4 + i);
            int amount = handler.getProperty(4 + AbstractWorkBlockEntity.PROP_MAX_LAYERS + i);
            if (typeId >= 0 && amount > 0) {
                int layerHeight = (int) ((double) amount / FluidTank.MAX_CAPACITY * h);
                FluidType type = ModFluids.byId(typeId);
                int color = 0xFF000000 | type.getColor();
                context.fill(x, currentBottom - layerHeight, x + w, currentBottom, color);
                context.fill(x, currentBottom - layerHeight, x + w, currentBottom - layerHeight + 1, 0x80FFFFFF);
                currentBottom -= layerHeight;
            }
        }

        for (int i = 1; i < 4; i++) {
            int markY = y + h * i / 4;
            context.fill(x - 3, markY, x, markY + 1, 0xFF999999);
        }
    }

    private void drawLayers(DrawContext context, int x, int y) {
        int layerCount = handler.getProperty(AbstractWorkBlockEntity.PROP_LAYER_COUNT);
        int selected = handler.getProperty(AbstractWorkBlockEntity.PROP_SELECTED);
        boolean blink = (System.currentTimeMillis() / 400) % 2 == 0;

        for (int i = 0; i < layerCount && i < AbstractWorkBlockEntity.PROP_MAX_LAYERS; i++) {
            int typeId = handler.getProperty(4 + i);
            int amount = handler.getProperty(4 + AbstractWorkBlockEntity.PROP_MAX_LAYERS + i);
            int layerY = y + i * LAYER_H;

            if (typeId >= 0) {
                FluidType type = ModFluids.byId(typeId);
                int color = 0xFF000000 | type.getColor();

                context.fill(x, layerY, x + LAYER_W, layerY + LAYER_H - 1, 0xFF404040);
                context.fill(x + 2, layerY + 2, x + 8, layerY + LAYER_H - 2, color);
                String name = type.getName();
                String text = name + " " + amount + "ML";
                context.drawText(textRenderer, text, x + 11, layerY + 1, 0xFFFFFFFF, false);

                if (i == selected && blink) {
                    drawDashedBorder(context, x - 1, layerY - 1, LAYER_W + 2, LAYER_H + 1, 0xFFFFFF00);
                }
            }
        }
    }

    private void drawDashedBorder(DrawContext context, int x, int y, int w, int h, int color) {
        int dash = 3;
        int gap = 2;
        for (int i = 0; i < w; i += dash + gap) {
            int end = Math.min(i + dash, w);
            context.fill(x + i, y, x + end, y + 1, color);
            context.fill(x + i, y + h - 1, x + end, y + h, color);
        }
        for (int i = 0; i < h; i += dash + gap) {
            int end = Math.min(i + dash, h);
            context.fill(x, y + i, x + 1, y + end, color);
            context.fill(x + w - 1, y + i, x + w, y + end, color);
        }
    }

    private void drawProgressArrow(DrawContext context, int x, int y, double progress) {
        int w = 22;
        int h = 16;
        context.fill(x, y, x + w, y + h, 0xFF4A4A4A);
        context.fill(x + 1, y + 1, x + w - 1, y + h - 1, 0xFF2A2A2A);
        int fillW = (int) (w * progress);
        if (fillW > 0) {
            context.fill(x, y, x + fillW, y + h, 0xFF7A7A7A);
            context.fill(x + 1, y + 1, x + Math.max(fillW - 1, 1), y + h - 1, 0xFF9A9A9A);
        }
        int tipX = x + w - 4;
        context.fill(tipX, y + 3, x + w, y + h - 3, 0xFF6A6A6A);
        context.fill(tipX + 1, y + 5, x + w - 1, y + h - 5, 0xFF8A8A8A);
    }

    private void updateButtonState() {
        ItemStack bucket = handler.getSlot(0).getStack();
        if (bucket.isOf(Items.WATER_BUCKET)) {
            buttonText = "倒入";
        } else if (bucket.isOf(Items.BUCKET)) {
            buttonText = "倒出";
        } else {
            buttonText = "存液/取液";
        }

        int selected = handler.getProperty(AbstractWorkBlockEntity.PROP_SELECTED);
        int count = handler.getProperty(AbstractWorkBlockEntity.PROP_LAYER_COUNT);
        boolean showButtons = selected >= 0 && selected < count;
        if (upButton != null) {
            upButton.visible = showButtons;
            upButton.setY(this.y + LAYER_Y + selected * LAYER_H);
        }
        if (downButton != null) {
            downButton.visible = showButtons;
            downButton.setY(this.y + LAYER_Y + selected * LAYER_H + LAYER_H);
        }
    }
}
