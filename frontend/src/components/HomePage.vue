<template>
  <div class="home">
    <div class="header">
      <h2>欢迎来到房产销售系统</h2>
      <div class="auth-buttons">
        <router-link to="/login" class="btn">登录</router-link>
        <router-link :to="{ path: '/login', query: { tab: 'register' }}" class="btn">注册</router-link>
      </div>
    </div>

    <!-- 在售房产列表 -->
    <div class="section">
      <h3>在售房产</h3>
      <div class="filter-section">
        <div class="price-filter">
          <label>价格范围：</label>
          <input type="number" v-model="minPrice" placeholder="最低价格" @input="applyFilters" />
          <span>-</span>
          <input type="number" v-model="maxPrice" placeholder="最高价格" @input="applyFilters" />
        </div>
        <div class="area-filter">
          <label>面积范围：</label>
          <input type="number" v-model="minArea" placeholder="最小面积" @input="applyFilters" />
          <span>-</span>
          <input type="number" v-model="maxArea" placeholder="最大面积" @input="applyFilters" />
        </div>
        <div class="filter-buttons">
          <button @click="applyFilters" class="filter-btn">筛选</button>
          <button @click="resetFilters" class="filter-btn reset">重置</button>
        </div>
      </div>
      <div class="card">
        <div class="houses-grid">
          <div v-for="house in filteredHouses" :key="house.id" class="house-card">
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
              <div class="info-row">
                <span class="label">状态：</span>
                <span class="value">在售</span>
              </div>
            </div>
            <div class="house-actions">
              <router-link to="/login" class="action-btn">登录后购买</router-link>
            </div>
          </div>
        </div>

        <div v-if="houses.length > 8" class="show-more">
          <button @click="toggleShowAllHouses" class="toggle-btn">
            {{ showAllHouses ? '收起' : `显示更多` }}
          </button>
        </div>

        <div v-if="houses.length === 0" class="no-data">
          暂无在售房产
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      houses: [],
      showAllHouses: false,
      minPrice: '',
      maxPrice: '',
      minArea: '',
      maxArea: '',
      filteredResults: [],
    };
  },
  watch: {
    minPrice() { this.applyFilters(); },
    maxPrice() { this.applyFilters(); },
    minArea() { this.applyFilters(); },
    maxArea() { this.applyFilters(); }
  },
  computed: {
    filteredHouses() {
      return this.showAllHouses ? this.filteredResults : this.filteredResults.slice(0, 8);
    }
  },
  methods: {
    formatPrice(price) {
      return parseFloat(price).toLocaleString('zh-CN');
    },
    toggleShowAllHouses() {
      this.showAllHouses = !this.showAllHouses;
    },
    applyFilters() {
      let filtered = this.houses;
      
      if (this.minPrice && !isNaN(parseFloat(this.minPrice))) {
        filtered = filtered.filter(house => parseFloat(house.price) >= parseFloat(this.minPrice));
      }
      if (this.maxPrice && !isNaN(parseFloat(this.maxPrice))) {
        filtered = filtered.filter(house => parseFloat(house.price) <= parseFloat(this.maxPrice));
      }
      if (this.minArea && !isNaN(parseFloat(this.minArea))) {
        filtered = filtered.filter(house => parseFloat(house.area) >= parseFloat(this.minArea));
      }
      if (this.maxArea && !isNaN(parseFloat(this.maxArea))) {
        filtered = filtered.filter(house => parseFloat(house.area) <= parseFloat(this.maxArea));
      }
      
      this.filteredResults = filtered;
    },
    resetFilters() {
      this.minPrice = '';
      this.maxPrice = '';
      this.minArea = '';
      this.maxArea = '';
      this.filteredResults = this.houses;
    },
    async fetchHouses() {
      try {
        const response = await axios.get('http://localhost:8000/houses/get_houses/');
        this.houses = response.data.filter(house => house.status === 'available');
        this.filteredResults = this.houses;
      } catch (error) {
        console.error('Error fetching houses:', error);
      }
    }
  },
  created() {
    this.fetchHouses();
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f5f5f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  background-color: #2196F3;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #1976D2;
}

.section {
  margin-bottom: 30px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.houses-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

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
}

.action-btn {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.3s;
}

.action-btn:hover {
  background-color: #1976D2;
}

.show-more {
  text-align: center;
  margin-top: 20px;
}

.toggle-btn {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.toggle-btn:hover {
  background-color: #1976D2;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}

@media (max-width: 1200px) {
  .houses-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 900px) {
  .houses-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .houses-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}

.filter-section {
  margin: 20px 0;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.price-filter, .area-filter {
  display: flex;
  align-items: center;
  gap: 10px;
}

.price-filter input, .area-filter input {
  width: 120px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
}

.price-filter input:focus, .area-filter input:focus {
  border-color: #2196F3;
}

.price-filter label, .area-filter label {
  color: #666;
  font-weight: 500;
}

@media (max-width: 600px) {
  .filter-section {
    flex-direction: column;
  }
  
  .price-filter, .area-filter {
    width: 100%;
  }
  
  .price-filter input, .area-filter input {
    flex: 1;
  }
}

.filter-buttons {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.filter-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  background-color: #2196F3;
  color: white;
}

.filter-btn:hover {
  background-color: #1976D2;
}

.filter-btn.reset {
  background-color: #9e9e9e;
}

.filter-btn.reset:hover {
  background-color: #757575;
}

@media (max-width: 600px) {
  .filter-buttons {
    width: 100%;
    justify-content: space-between;
  }
  
  .filter-btn {
    flex: 1;
  }
}
</style> 