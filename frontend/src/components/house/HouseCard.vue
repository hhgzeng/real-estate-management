<template>
  <div class="house-card">
    <div class="house-info">
      <h4>房产编号: {{ house.id }}</h4>
      <div class="info-row">
        <span class="label">价格：</span>
        <span class="value price">¥ {{ formatPrice(house.price) }}</span>
      </div>
      <div class="info-row">
        <span class="label">面积：</span>
        <span class="value">{{ house.area }}㎡</span>
      </div>
      <div class="info-row">
        <span class="label">楼层：</span>
        <span class="value">{{ house.floor }}层</span>
      </div>
      <div class="info-row" v-if="house.salesperson_name">
        <span class="label">销售人员：</span>
        <span class="value">{{ house.salesperson_name }}</span>
      </div>
      <div class="info-row" v-if="showStatus">
        <span class="label">状态：</span>
        <span class="value">{{ house.status === 'available' ? '在售' : house.status }}</span>
      </div>
    </div>
    <div class="house-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HouseCard',
  props: {
    house: {
      type: Object,
      required: true
    },
    showStatus: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    formatPrice(price) {
      if (price === null || price === undefined || isNaN(price)) {
        return '0';
      }
      return parseFloat(price).toLocaleString('zh-CN');
    }
  }
};
</script>

<style scoped>
.house-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.house-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.house-info {
  margin-bottom: 15px;
}

.house-info h4 {
  margin: 0 0 15px 0;
  color: #2c3e50;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.label {
  color: #666;
}

.value {
  font-weight: 500;
}

.value.price {
  color: #e74c3c;
  font-weight: bold;
}

.house-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
  border-top: 1px solid #eee;
  gap: 8px;
}
</style>
