package com.mytest.firstmod.client.screen;

import com.mytest.firstmod.screen.FlowerBagScreenHandler;
import com.mojang.blaze3d.systems.RenderSystem;
import net.minecraft.client.gui.DrawContext;
import net.minecraft.client.gui.screen.ingame.HandledScreen;
import net.minecraft.entity.player.PlayerInventory;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

/**
 * 繁花收纳袋 GUI 界面
 * 完全还原原始实现：整张 flower_bag.png 作为背景，4 个图标按钮直接检测鼠标点击
 */
public class FlowerBagScreen extends HandledScreen<FlowerBagScreenHandler> {

    private static final Identifier BASE_TEXTURE = new Identifier("firstmod", "textures/gui/flower_bag.png");

    // 4个按钮的X坐标（相对于GUI左上角），Y固定为7，大小14x14
    private static final int[] BTN_X = {9, 29, 49, 69};
    private static final int BTN_Y = 7;
    private static final int BTN_SIZE = 14;

    private static final Text TITLE_TEXT = Text.literal("繁花收纳袋");
    private static final Text INVENTORY_TEXT = Text.literal("物品栏");

    public FlowerBagScreen(FlowerBagScreenHandler handler, PlayerInventory inventory, Text title) {
        super(handler, inventory, title);
        this.backgroundWidth = 176;
        this.backgroundHeight = 166;
        // 隐藏父类默认的标题和物品栏文字，我们自己绘制
        this.titleX = -10000;
        this.titleY = -10000;
        this.playerInventoryTitleY = -10000;
    }

    @Override
    protected void drawBackground(DrawContext context, float delta, int mouseX, int mouseY) {
        RenderSystem.setShaderColor(1.0f, 1.0f, 1.0f, 1.0f);
        RenderSystem.setShaderTexture(0, BASE_TEXTURE);

        int x = (this.width - this.backgroundWidth) / 2;
        int y = (this.height - this.backgroundHeight) / 2;

        // 绘制整张背景图（左上角 176x166 区域）
        context.drawTexture(BASE_TEXTURE, x, y, 0, 0,
                this.backgroundWidth, this.backgroundHeight, 256, 256);

        // 绘制4个按钮图标

        // 按钮0：吸取开关
        // 开：只画吸取图标；关：吸取图标上叠加红叉
        boolean suckOn = this.handler.propertyDelegate.get(0) == 1;
        drawButtonIcon(context, x + BTN_X[0], y + BTN_Y, 192, 0, true);
        if (!suckOn) {
            // 叠加红色叉号（14x14，贴图坐标 176,16）
            context.drawTexture(BASE_TEXTURE, x + BTN_X[0], y + BTN_Y,
                    176, 16, BTN_SIZE, BTN_SIZE, 256, 256);
        }

        // 按钮1：一键存入
        drawButtonIcon(context, x + BTN_X[1], y + BTN_Y, 208, 0, true);

        // 按钮2：一键取出
        drawButtonIcon(context, x + BTN_X[2], y + BTN_Y, 224, 0, true);

        // 按钮3：排序（3种模式）
        int sortMode = this.handler.propertyDelegate.get(1);
        int sortU;
        int sortV;
        switch (sortMode) {
            case 1 -> { sortU = 240; sortV = 16; }
            case 2 -> { sortU = 224; sortV = 16; }
            default -> { sortU = 240; sortV = 0; }
        }
        drawButtonIcon(context, x + BTN_X[3], y + BTN_Y, sortU, sortV, true);
    }

    /**
     * 绘制按钮图标
     * @param context 绘制上下文
     * @param x 屏幕X
     * @param y 屏幕Y
     * @param u 贴图U坐标
     * @param v 贴图V坐标
     * @param enabled 是否启用（false时叠加灰色遮罩）
     */
    private void drawButtonIcon(DrawContext context, int x, int y, int u, int v, boolean enabled) {
        context.drawTexture(BASE_TEXTURE, x, y, u, v, BTN_SIZE, BTN_SIZE, 256, 256);
        if (!enabled) {
            context.drawTexture(BASE_TEXTURE, x, y, 176, 16, BTN_SIZE, BTN_SIZE, 256, 256);
        }
    }

    @Override
    protected void drawForeground(DrawContext context, int mouseX, int mouseY) {
        // 标题（右上角）
        context.drawText(this.textRenderer, TITLE_TEXT,
                this.backgroundWidth - this.textRenderer.getWidth(TITLE_TEXT) - 7,
                6, 0x404040, false);
        // 物品栏文字
        context.drawText(this.textRenderer, INVENTORY_TEXT,
                8, this.backgroundHeight - 94 + 3, 0x404040, false);
    }

    @Override
    public void render(DrawContext context, int mouseX, int mouseY, float delta) {
        this.renderBackground(context);
        super.render(context, mouseX, mouseY, delta);

        // 绘制按钮 tooltip
        int guiX = (this.width - this.backgroundWidth) / 2;
        int guiY = (this.height - this.backgroundHeight) / 2;

        for (int i = 0; i < 4; i++) {
            int bx = guiX + BTN_X[i];
            int by = guiY + BTN_Y;
            if (mouseX >= bx && mouseX < bx + BTN_SIZE
                    && mouseY >= by && mouseY < by + BTN_SIZE) {

                String title = "";
                String subText = "";
                int subColor = 0xFFFFFF;

                switch (i) {
                    case 0 -> {
                        title = "自动吸取（花朵）";
                        if (this.handler.propertyDelegate.get(0) == 1) {
                            subText = "开";
                            subColor = 0x00AA00; // 绿色
                        } else {
                            subText = "关";
                            subColor = 0xAA0000; // 红色
                        }
                    }
                    case 1 -> title = "一键存入";
                    case 2 -> title = "一键取出";
                    case 3 -> {
                        int mode = this.handler.propertyDelegate.get(1);
                        if (mode == 1) {
                            title = "当前按数量排序";
                        } else if (mode == 2) {
                            title = "当前按物品ID排序";
                        } else {
                            title = "当前按物品名称排序";
                        }
                    }
                }

                drawTooltipBox(context, mouseX + 12, mouseY - 12, title, subText, subColor);
                break;
            }
        }

        this.drawMouseoverTooltip(context, mouseX, mouseY);
    }

    /**
     * 绘制自定义 tooltip（和原版风格一致）
     */
    private void drawTooltipBox(DrawContext context, int x, int y, String title, String subText, int subColor) {
        int titleWidth = this.textRenderer.getWidth(title);
        int subWidth = this.textRenderer.getWidth(subText);
        int totalWidth = titleWidth + subWidth;
        int padding = 4;
        int boxWidth = totalWidth + padding * 2;
        int boxHeight = 9 + padding * 2;

        // 黑色边框
        context.fill(x - 1, y - 1, x + boxWidth + 1, y + boxHeight + 1, 0xFF000000);
        // 半透明深紫背景
        context.fill(x, y, x + boxWidth, y + boxHeight, 0xF0100010);

        int textX = x + padding;
        int textY = y + padding + 1;

        context.drawText(this.textRenderer, title, textX, textY, 0xFFFFFF, false);
        if (!subText.isEmpty()) {
            context.drawText(this.textRenderer, subText, textX + titleWidth, textY, subColor, false);
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        int guiX = (this.width - this.backgroundWidth) / 2;
        int guiY = (this.height - this.backgroundHeight) / 2;

        int mx = (int) mouseX - guiX;
        int my = (int) mouseY - guiY;

        // 检测4个按钮的点击
        if (my >= BTN_Y && my <= BTN_Y + BTN_SIZE) {
            for (int i = 0; i < 4; i++) {
                if (mx >= BTN_X[i] && mx <= BTN_X[i] + BTN_SIZE) {
                    if (this.client != null && this.client.interactionManager != null) {
                        this.client.interactionManager.clickButton(this.handler.syncId, i);
                    }
                    return true;
                }
            }
        }

        return super.mouseClicked(mouseX, mouseY, button);
    }
}
