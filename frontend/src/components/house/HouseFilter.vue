<template>
  <div class="house-filter">
    <div class="filter-group">
      <label>价格区间：</label>
      <input 
        v-model.number="localFilters.minPrice" 
        type="number" 
        placeholder="最低价" 
        @input="emitFilters"
      />
      <span>-</span>
      <input 
        v-model.number="localFilters.maxPrice" 
        type="number" 
        placeholder="最高价" 
        @input="emitFilters"
      />
    </div>
    <div class="filter-group">
      <label>面积区间：</label>
      <input 
        v-model.number="localFilters.minArea" 
        type="number" 
        placeholder="最小面积" 
        @input="emitFilters"
      />
      <span>-</span>
      <input 
        v-model.number="localFilters.maxArea" 
        type="number" 
        placeholder="最大面积" 
        @input="emitFilters"
      />
    </div>
    <div class="filter-buttons">
      <button class="filter-btn" @click="emitFilters">筛选</button>
      <button class="reset-btn" @click="resetFilters">重置</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HouseFilter',
  props: {
    initialFilters: {
      type: Object,
      default: () => ({
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      })
    }
  },
  data() {
    return {
      localFilters: { ...this.initialFilters }
    };
  },
  methods: {
    emitFilters() {
      this.$emit('filter', { ...this.localFilters });
    },
    resetFilters() {
      this.localFilters = {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      };
      this.$emit('filter', { ...this.localFilters });
    }
  }
};
</script>

<style scoped>
.house-filter {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: center;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group input {
  width: 120px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-group label {
  color: #666;
  font-weight: 500;
}

.filter-buttons {
  display: flex;
  gap: 10px;
}

.filter-btn, .reset-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.filter-btn {
  background-color: #2196F3;
  color: white;
}

.filter-btn:hover {
  background-color: #1976D2;
}

.reset-btn {
  background-color: #9e9e9e;
  color: white;
}

.reset-btn:hover {
  background-color: #757575;
}

@media (max-width: 600px) {
  .house-filter {
    flex-direction: column;
    align-items: flex-start;
  }
  .filter-group, .filter-buttons {
    width: 100%;
  }
  .filter-group input {
    flex: 1;
  }
  .filter-buttons button {
    flex: 1;
  }
}
</style>
