<template>
  <div class="home">
    <TopHeader title="欢迎来到房产销售系统" />

    <!-- 在售房产列表 -->
    <div class="section">
      <h3>在售房产</h3>
      <HouseFilter @filter="handleFilter" />
      
      <div class="card">
        <div class="houses-grid" v-if="filteredHouses.length > 0">
          <HouseCard 
            v-for="house in filteredHouses" 
            :key="house.id" 
            :house="house"
            :showStatus="true"
          >
            <template #actions>
              <router-link to="/login" class="action-btn">登录后购买</router-link>
            </template>
          </HouseCard>
        </div>

        <div v-if="houses.length > 8 && filteredResults.length > 8" class="show-more">
          <button @click="toggleShowAllHouses" class="toggle-btn">
            {{ showAllHouses ? '收起' : `显示更多` }}
          </button>
        </div>

        <div v-if="filteredResults.length === 0" class="no-data">
          暂无符合条件的在售房产
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import TopHeader from '@/components/layout/TopHeader.vue';
import HouseFilter from '@/components/house/HouseFilter.vue';
import HouseCard from '@/components/house/HouseCard.vue';

export default {
  name: 'HomePage',
  components: {
    TopHeader,
    HouseFilter,
    HouseCard
  },
  data() {
    return {
      houses: [],
      showAllHouses: false,
      filteredResults: [],
    };
  },
  computed: {
    filteredHouses() {
      return this.showAllHouses ? this.filteredResults : this.filteredResults.slice(0, 8);
    }
  },
  methods: {
    toggleShowAllHouses() {
      this.showAllHouses = !this.showAllHouses;
    },
    handleFilter(filters) {
      let filtered = this.houses;
      
      if (filters.minPrice !== '') {
        filtered = filtered.filter(house => parseFloat(house.price) >= parseFloat(filters.minPrice));
      }
      if (filters.maxPrice !== '') {
        filtered = filtered.filter(house => parseFloat(house.price) <= parseFloat(filters.maxPrice));
      }
      if (filters.minArea !== '') {
        filtered = filtered.filter(house => parseFloat(house.area) >= parseFloat(filters.minArea));
      }
      if (filters.maxArea !== '') {
        filtered = filtered.filter(house => parseFloat(house.area) <= parseFloat(filters.maxArea));
      }
      
      this.filteredResults = filtered;
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
  min-height: 100vh;
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

.action-btn {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.3s;
  font-size: 14px;
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
}
</style>
 