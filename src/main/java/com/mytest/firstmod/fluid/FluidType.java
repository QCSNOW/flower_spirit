package com.mytest.firstmod.fluid;

public class FluidType {
    private final int id;
    private final String name;
    private final int color;

    public FluidType(int id, String name, int color) {
        this.id = id;
        this.name = name;
        this.color = color;
    }

    public int getId() { return id; }
    public String getName() { return name; }
    public int getColor() { return color; }

    public int getRed() { return (color >> 16) & 0xFF; }
    public int getGreen() { return (color >> 8) & 0xFF; }
    public int getBlue() { return color & 0xFF; }
}
