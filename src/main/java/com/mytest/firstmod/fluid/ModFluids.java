package com.mytest.firstmod.fluid;

import java.util.*;

public class ModFluids {
    public static final FluidType WATER = new FluidType(0, "水", 0x3F76E4);
    public static final FluidType HONEY = new FluidType(1, "蜂蜜", 0xFFAA00);

    private static final Map<Integer, FluidType> BY_ID = new LinkedHashMap<>();

    static {
        BY_ID.put(WATER.getId(), WATER);
        BY_ID.put(HONEY.getId(), HONEY);
    }

    public static FluidType byId(int id) {
        return BY_ID.getOrDefault(id, WATER);
    }

    public static Collection<FluidType> all() {
        return BY_ID.values();
    }
}
