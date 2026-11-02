package com.mytest.firstmod.fluid;

import net.minecraft.nbt.NbtCompound;
import net.minecraft.nbt.NbtList;
import java.util.ArrayList;
import java.util.List;

public class FluidTank {
    public static final int MAX_CAPACITY = 2000;
    public static final int BUCKET_AMOUNT = 1000;
    private static final int MAX_LAYERS = 10;

    private final List<FluidLayer> layers = new ArrayList<>();
    private int selectedLayer = -1;

    public static class FluidLayer {
        private final FluidType type;
        private int amount;

        public FluidLayer(FluidType type, int amount) {
            this.type = type;
            this.amount = amount;
        }

        public FluidType getType() { return type; }
        public int getAmount() { return amount; }
        public void setAmount(int amount) { this.amount = amount; }
    }

    public int getTotalAmount() {
        int total = 0;
        for (FluidLayer layer : layers) total += layer.getAmount();
        return total;
    }

    public int getRemainingCapacity() {
        return MAX_CAPACITY - getTotalAmount();
    }

    public int getLayerCount() {
        return layers.size();
    }

    public int getSelectedLayer() {
        return selectedLayer;
    }

    public void setSelectedLayer(int index) {
        this.selectedLayer = (index >= 0 && index < layers.size()) ? index : -1;
    }

    public FluidLayer getLayer(int index) {
        if (index < 0 || index >= layers.size()) return null;
        return layers.get(index);
    }

    public int add(FluidType type, int amount) {
        if (amount <= 0) return 0;
        int canAdd = Math.min(amount, getRemainingCapacity());
        if (canAdd <= 0) return 0;

        if (!layers.isEmpty() && layers.get(layers.size() - 1).getType().getId() == type.getId()) {
            FluidLayer top = layers.get(layers.size() - 1);
            top.setAmount(top.getAmount() + canAdd);
            return canAdd;
        }

        if (layers.size() >= MAX_LAYERS) return 0;
        layers.add(new FluidLayer(type, canAdd));
        return canAdd;
    }

    public int removeFirst(FluidType type, int amount) {
        if (amount <= 0) return 0;
        int removed = 0;
        for (int i = 0; i < layers.size() && removed < amount; i++) {
            FluidLayer layer = layers.get(i);
            if (layer.getType().getId() == type.getId()) {
                int canRemove = Math.min(amount - removed, layer.getAmount());
                layer.setAmount(layer.getAmount() - canRemove);
                removed += canRemove;
                if (layer.getAmount() <= 0) {
                    int removedIndex = i;
                    layers.remove(removedIndex);
                    if (selectedLayer == removedIndex) selectedLayer = -1;
                    else if (selectedLayer > removedIndex) selectedLayer--;
                    i--;
                }
            }
        }
        return removed;
    }

    public int removeFromSelected(int amount) {
        if (selectedLayer < 0 || selectedLayer >= layers.size()) return 0;
        return removeFromLayer(selectedLayer, amount);
    }

    public int removeFromLayer(int index, int amount) {
        if (index < 0 || index >= layers.size()) return 0;
        FluidLayer layer = layers.get(index);
        int canRemove = Math.min(amount, layer.getAmount());
        layer.setAmount(layer.getAmount() - canRemove);
        if (layer.getAmount() <= 0) {
            layers.remove(index);
            if (selectedLayer == index) selectedLayer = -1;
            else if (selectedLayer > index) selectedLayer--;
        }
        return canRemove;
    }

    public void dumpLayer(int index) {
        if (index < 0 || index >= layers.size()) return;
        layers.remove(index);
        if (selectedLayer == index) selectedLayer = -1;
        else if (selectedLayer > index) selectedLayer--;
    }

    public void dumpSelected() {
        if (selectedLayer < 0 || selectedLayer >= layers.size()) return;
        layers.remove(selectedLayer);
        selectedLayer = -1;
    }

    public int getFluidAmount(FluidType type) {
        int total = 0;
        for (FluidLayer layer : layers) {
            if (layer.getType().getId() == type.getId()) total += layer.getAmount();
        }
        return total;
    }

    public boolean hasFluidType(FluidType type) {
        return getFluidAmount(type) > 0;
    }

    public void moveLayerUp(int index) {
        if (index <= 0 || index >= layers.size()) return;
        FluidLayer layer = layers.remove(index);
        layers.add(index - 1, layer);
        if (selectedLayer == index) selectedLayer = index - 1;
        else if (selectedLayer == index - 1) selectedLayer = index;
    }

    public void moveLayerDown(int index) {
        if (index < 0 || index >= layers.size() - 1) return;
        FluidLayer layer = layers.remove(index);
        layers.add(index + 1, layer);
        if (selectedLayer == index) selectedLayer = index + 1;
        else if (selectedLayer == index + 1) selectedLayer = index;
    }

    public NbtCompound writeNbt() {
        NbtCompound nbt = new NbtCompound();
        NbtList list = new NbtList();
        for (FluidLayer layer : layers) {
            NbtCompound layerNbt = new NbtCompound();
            layerNbt.putInt("Type", layer.getType().getId());
            layerNbt.putInt("Amount", layer.getAmount());
            list.add(layerNbt);
        }
        nbt.put("Layers", list);
        nbt.putInt("Selected", selectedLayer);
        return nbt;
    }

    public void readNbt(NbtCompound nbt) {
        layers.clear();
        selectedLayer = -1;
        NbtList list = nbt.getList("Layers", NbtCompound.COMPOUND_TYPE);
        for (int i = 0; i < list.size(); i++) {
            NbtCompound layerNbt = list.getCompound(i);
            FluidType type = ModFluids.byId(layerNbt.getInt("Type"));
            int amount = layerNbt.getInt("Amount");
            if (amount > 0) layers.add(new FluidLayer(type, amount));
        }
        int sel = nbt.getInt("Selected");
        selectedLayer = (sel >= 0 && sel < layers.size()) ? sel : -1;
    }

    public void clear() {
        layers.clear();
        selectedLayer = -1;
    }
}
