package com.mytest.firstmod.client.render;
import com.mytest.firstmod.block.entity.AbstractWorkBlockEntity;
import com.mytest.firstmod.fluid.FluidTank;


import net.minecraft.client.render.RenderLayer;
import net.minecraft.client.render.VertexConsumer;
import net.minecraft.client.render.VertexConsumerProvider;
import net.minecraft.client.render.block.entity.BlockEntityRenderer;
import net.minecraft.client.render.block.entity.BlockEntityRendererFactory;
import net.minecraft.client.util.math.MatrixStack;
import org.joml.Matrix3f;
import org.joml.Matrix4f;

public class WorkBlockEntityRenderer implements BlockEntityRenderer<AbstractWorkBlockEntity> {

    // Cavity dimensions with small inset to prevent z-fighting with model walls
    private static final float INSET = 0.005f;
    private static final float CAVITY_MIN_X = 4.0f / 16.0f + INSET;
    private static final float CAVITY_MAX_X = 12.0f / 16.0f - INSET;
    private static final float CAVITY_MIN_Z = 4.0f / 16.0f + INSET;
    private static final float CAVITY_MAX_Z = 12.0f / 16.0f - INSET;
    private static final float CAVITY_BOTTOM_Y = 2.0f / 16.0f + INSET;
    private static final float CAVITY_TOP_Y = 10.0f / 16.0f - INSET;

    public WorkBlockEntityRenderer(BlockEntityRendererFactory.Context ctx) {
    }

    @Override
    public void render(AbstractWorkBlockEntity entity, float tickDelta, MatrixStack matrices,
                       VertexConsumerProvider vertexConsumers, int light, int overlay) {
        FluidTank tank = entity.getFluidTank();
        int totalAmount = tank.getTotalAmount();
        if (totalAmount <= 0) return;

        VertexConsumer consumer = vertexConsumers.getBuffer(RenderLayer.getSolid());
        Matrix4f pos = matrices.peek().getPositionMatrix();
        Matrix3f norm = matrices.peek().getNormalMatrix();

        float currentBottom = CAVITY_BOTTOM_Y;
        int layerCount = tank.getLayerCount();

        for (int i = 0; i < layerCount; i++) {
            FluidTank.FluidLayer layer = tank.getLayer(i);
            if (layer == null || layer.getAmount() <= 0) continue;

            float layerHeight = (float) layer.getAmount() / FluidTank.MAX_CAPACITY * (CAVITY_TOP_Y - CAVITY_BOTTOM_Y);
            float layerTop = Math.min(currentBottom + layerHeight, CAVITY_TOP_Y);

            int color = layer.getType().getColor();
            int r = (color >> 16) & 0xFF;
            int g = (color >> 8) & 0xFF;
            int b = color & 0xFF;
            int a = 255;

            drawSides(pos, norm, consumer, currentBottom, layerTop, r, g, b, a, light, overlay);

            if (i == layerCount - 1) {
                drawTop(pos, norm, consumer, layerTop, r, g, b, a, light, overlay);
                // Bright surface highlight for better visibility
                int hr = Math.min(255, r + 60);
                int hg = Math.min(255, g + 60);
                int hb = Math.min(255, b + 60);
                drawTopHighlight(pos, norm, consumer, layerTop + 0.001f, hr, hg, hb, 255, light, overlay);
            }

            currentBottom = layerTop;
        }
    }

    private void drawTop(Matrix4f mat, Matrix3f norm, VertexConsumer c, float y,
                         int r, int g, int b, int a, int light, int overlay) {
        c.vertex(mat, CAVITY_MIN_X, y, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, CAVITY_MAX_X, y, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, CAVITY_MAX_X, y, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, CAVITY_MIN_X, y, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
    }

    private void drawTopHighlight(Matrix4f mat, Matrix3f norm, VertexConsumer c, float y,
                                  int r, int g, int b, int a, int light, int overlay) {
        float inset = 0.5f / 16.0f;
        float minX = CAVITY_MIN_X + inset;
        float maxX = CAVITY_MAX_X - inset;
        float minZ = CAVITY_MIN_Z + inset;
        float maxZ = CAVITY_MAX_Z - inset;
        c.vertex(mat, minX, y, minZ).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, maxX, y, minZ).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, maxX, y, maxZ).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
        c.vertex(mat, minX, y, maxZ).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 1, 0).next();
    }

    private void drawSides(Matrix4f mat, Matrix3f norm, VertexConsumer c,
                           float y1, float y2,
                           int r, int g, int b, int a, int light, int overlay) {
        // North (-Z)
        c.vertex(mat, CAVITY_MIN_X, y1, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, -1).next();
        c.vertex(mat, CAVITY_MAX_X, y1, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, -1).next();
        c.vertex(mat, CAVITY_MAX_X, y2, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, -1).next();
        c.vertex(mat, CAVITY_MIN_X, y2, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, -1).next();

        // South (+Z)
        c.vertex(mat, CAVITY_MIN_X, y1, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, 1).next();
        c.vertex(mat, CAVITY_MAX_X, y1, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, 1).next();
        c.vertex(mat, CAVITY_MAX_X, y2, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, 1).next();
        c.vertex(mat, CAVITY_MIN_X, y2, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 0, 0, 1).next();

        // West (-X)
        c.vertex(mat, CAVITY_MIN_X, y1, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, -1, 0, 0).next();
        c.vertex(mat, CAVITY_MIN_X, y2, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, -1, 0, 0).next();
        c.vertex(mat, CAVITY_MIN_X, y2, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, -1, 0, 0).next();
        c.vertex(mat, CAVITY_MIN_X, y1, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, -1, 0, 0).next();

        // East (+X)
        c.vertex(mat, CAVITY_MAX_X, y1, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 1, 0, 0).next();
        c.vertex(mat, CAVITY_MAX_X, y2, CAVITY_MIN_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 1, 0, 0).next();
        c.vertex(mat, CAVITY_MAX_X, y2, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 1, 0, 0).next();
        c.vertex(mat, CAVITY_MAX_X, y1, CAVITY_MAX_Z).color(r, g, b, a).texture(0, 0).overlay(overlay).light(light).normal(norm, 1, 0, 0).next();
    }

    @Override
    public int getRenderDistance() {
        return 64;
    }
}
