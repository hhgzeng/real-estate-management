<template>
  <div class="sales-dashboard">
    <TopHeader :title="`欢迎回来，${username}`" @logout="logout" />

    <div class="main-content">
      <!-- 个人信息部分 -->
      <div class="section">
        <h3>我的信息</h3>
        <div class="card user-info">
          <div class="info-grid">
            <div class="info-item">
              <span class="label">用户名：</span>
              <span class="value">{{ username }}</span>
            </div>
            <div class="info-item">
              <span class="label">角色：</span>
              <span class="value">销售人员</span>
            </div>
            <div class="info-item">
              <button @click="showChangePassword = true" class="btn btn-primary">
                修改密码
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 销售业绩统计 -->
      <div class="section">
        <h3>销售业绩</h3>
        <div v-if="loading.stats" class="loading">
          <div class="spinner"></div>
          <span>加载中...</span>
        </div>
        <div v-else-if="error.stats" class="error-message">
          {{ error.stats }}
        </div>
        <div v-else class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon sales-count">
              <i class="fas fa-handshake"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ salesStats.totalSales || 0 }}</div>
              <div class="stat-label">总成交数</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon sales-amount">
              <i class="fas fa-yen-sign"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">¥ {{ salesStats.totalAmount ? salesStats.totalAmount.toLocaleString('zh-CN') : 0 }}</div>
              <div class="stat-label">总销售额</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon house-count">
              <i class="fas fa-home"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ availableHouses.length }}</div>
              <div class="stat-label">在售房产</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 在售房产 -->
      <div class="section">
        <div class="section-header">
          <h3>在售房产</h3>
          <button class="add-btn" @click="showAddHouseDialog = true">添加房产</button>
        </div>
        <div class="card">
          <HouseFilter @filter="handleFilter" />

          <div class="houses-grid" v-if="displayedAvailableHouses.length > 0">
            <HouseCard 
              v-for="house in displayedAvailableHouses" 
              :key="house.id" 
              :house="house"
            >
              <template #actions>
                <button class="edit-btn" @click="showEditHouseDialog(house)">修改</button>
              </template>
            </HouseCard>
          </div>

          <div v-if="filteredAvailableHouses.length > 8" class="show-more">
            <button @click="toggleShowAllAvailable" class="toggle-btn">
              {{ showAllAvailable ? '收起' : `显示更多` }}
            </button>
          </div>
          <div v-if="filteredAvailableHouses.length === 0" class="no-data">
            暂无符合条件的房产
          </div>
        </div>
      </div>

      <!-- 已售房产 -->
      <div class="section">
        <h3>已售房产</h3>
        <div class="card">
          <div class="houses-grid" v-if="displayedSoldHouses.length > 0">
            <HouseCard 
              v-for="house in displayedSoldHouses" 
              :key="house.id" 
              :house="house"
              :showStatus="true"
            />
          </div>

          <div v-if="soldHouses.length > 8" class="show-more">
            <button @click="toggleShowAllSold" class="toggle-btn">
              {{ showAllSold ? '收起' : `显示更多` }}
            </button>
          </div>
          <div v-if="soldHouses.length === 0" class="no-data">
            暂无已售房产
          </div>
        </div>
      </div>

      <!-- 销售记录 -->
      <div class="section">
        <h3>销售记录</h3>
        <div class="card">
          <table class="data-table" v-if="salesRecords.length">
            <thead>
              <tr>
                <th>订单编号</th>
                <th>房产信息</th>
                <th>客户</th>
                <th>交易日期</th>
                <th>价格</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in displayedSalesRecords" :key="record.id">
                <td>{{ record.id }}</td>
                <td>{{ record.house_info }}</td>
                <td>{{ record.customer_name }}</td>
                <td>{{ formatDate(record.order_date) }}</td>
                <td class="price">¥{{ record.price.toLocaleString('zh-CN') }}</td>
              </tr>
            </tbody>
          </table>
          <div class="show-more" v-if="salesRecords.length > 5">
            <button @click="toggleShowAllRecords" class="toggle-btn">
              {{ showAllRecords ? '收起' : '显示更多' }}
            </button>
          </div>
          <div v-if="salesRecords.length === 0" class="no-data">
            暂无销售记录
          </div>
        </div>
      </div>
    </div>

    <!-- 添加房产对话框 -->
    <div v-if="showAddHouseDialog" class="modal">
      <div class="modal-content">
        <h3>添加房产</h3>
        <form @submit.prevent="submitHouse" class="form">
          <div class="form-group">
            <label>价格</label>
            <input 
              v-model.number="newHouse.price" 
              type="number" 
              required 
              placeholder="请输入价格"
            />
          </div>
          <div class="form-group">
            <label>面积</label>
            <input 
              v-model.number="newHouse.area" 
              type="number" 
              required 
              placeholder="请输入面积"
            />
          </div>
          <div class="form-group">
            <label>楼层</label>
            <input 
              v-model.number="newHouse.floor" 
              type="number" 
              required 
              placeholder="请输入楼层"
            />
          </div>
          <div class="modal-buttons">
            <button type="submit" class="submit-btn" :disabled="submitting">确认</button>
            <button type="button" class="cancel-btn" @click="cancelAddHouse">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 修改房产对话框 -->
    <div v-if="showEditDialog" class="modal">
      <div class="modal-content">
        <h3>修改房产信息</h3>
        <form @submit.prevent="updateHouse" class="form">
          <div class="form-group">
            <label>价格</label>
            <input 
              v-model.number="editingHouse.price" 
              type="number" 
              required 
            />
          </div>
          <div class="form-group">
            <label>面积</label>
            <input 
              v-model.number="editingHouse.area" 
              type="number" 
              required 
            />
          </div>
          <div class="form-group">
            <label>楼层</label>
            <input 
              v-model.number="editingHouse.floor" 
              type="number" 
              required 
            />
          </div>
          <div class="modal-buttons">
            <button type="submit" class="submit-btn">保存</button>
            <button type="button" class="cancel-btn" @click="cancelEdit">取消</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 修改密码对话框 -->
    <div v-if="showChangePassword" class="modal">
      <div class="modal-content">
        <span class="close" @click="showChangePassword = false">&times;</span>
        <ChangePassword @passwordChanged="handlePasswordChanged" />
      </div>
    </div>
  </div>
</template>

<script>
import { getMyHouses, createHouse, updateHouse } from '@/api/house';
import { getSalesStats, getMySales } from '@/api/order';
import ChangePassword from '@/components/common/ChangePassword.vue';
import TopHeader from '@/components/layout/TopHeader.vue';
import HouseFilter from '@/components/house/HouseFilter.vue';
import HouseCard from '@/components/house/HouseCard.vue';

export default {
  name: 'SalesDashboard',
  components: {
    ChangePassword,
    TopHeader,
    HouseFilter,
    HouseCard
  },
  data() {
    return {
      username: localStorage.getItem('username'),
      showChangePassword: false,
      salesStats: {
        totalSales: 0,
        totalAmount: 0
      },
      myHouses: [],
      salesRecords: [],
      showAddHouseDialog: false,
      showEditDialog: false,
      newHouse: {
        price: '',
        area: '',
        floor: ''
      },
      editingHouse: null,
      submitting: false,
      loading: {
        stats: false,
        houses: false,
        records: false
      },
      error: {
        stats: '',
        houses: '',
        records: ''
      },
      showAllRecords: false,
      showAllAvailable: false,
      showAllSold: false,
      filters: {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      }
    };
  },
  computed: {
    availableHouses() {
      return this.myHouses.filter(house => house.status === 'available');
    },
    soldHouses() {
      return this.myHouses.filter(house => house.status === 'sold');
    },
    filteredAvailableHouses() {
      return this.availableHouses.filter(house => {
        const price = parseFloat(house.price);
        const area = parseFloat(house.area);
        
        if (this.filters.minPrice !== '' && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice !== '' && price > this.filters.maxPrice) return false;
        if (this.filters.minArea !== '' && area < this.filters.minArea) return false;
        if (this.filters.maxArea !== '' && area > this.filters.maxArea) return false;
        
        return true;
      });
    },
    displayedAvailableHouses() {
      return this.showAllAvailable ? this.filteredAvailableHouses : this.filteredAvailableHouses.slice(0, 8);
    },
    displayedSoldHouses() {
      return this.showAllSold ? this.soldHouses : this.soldHouses.slice(0, 8);
    },
    displayedSalesRecords() {
      const sortedRecords = [...this.salesRecords].sort((a, b) => 
        new Date(b.order_date) - new Date(a.order_date)
      );
      return this.showAllRecords ? sortedRecords : sortedRecords.slice(0, 5);
    }
  },
  created() {
    this.initialize();
  },
  methods: {
    async initialize() {
      await Promise.all([
        this.fetchSalesStats(),
        this.fetchMyHouses(),
        this.fetchSalesRecords()
      ]);
    },
    formatDate(date) {
      return new Date(date).toLocaleString('zh-CN');
    },
    async fetchSalesStats() {
      this.loading.stats = true;
      this.error.stats = '';
      try {
        const userId = localStorage.getItem('userId');
        const response = await getSalesStats(userId);
        if (response.data.status === 'success') {
          this.salesStats = {
            totalSales: response.data.totalSales,
            totalAmount: response.data.totalAmount
          };
        } else {
          this.error.stats = response.data.message || '获取销售统计失败';
        }
      } catch (error) {
        this.error.stats = '获取销售统计失败，请稍后重试';
      } finally {
        this.loading.stats = false;
      }
    },
    async fetchMyHouses() {
      this.loading.houses = true;
      this.error.houses = '';
      try {
        const userId = localStorage.getItem('userId');
        const response = await getMyHouses(userId);
        this.myHouses = response.data;
      } catch (error) {
        this.error.houses = '获取房产列表失败，请稍后重试';
      } finally {
        this.loading.houses = false;
      }
    },
    async fetchSalesRecords() {
      this.loading.records = true;
      this.error.records = '';
      try {
        const userId = localStorage.getItem('userId');
        const response = await getMySales(userId);
        this.salesRecords = response.data;
      } catch (error) {
        this.error.records = '获取销售记录失败，请稍后重试';
      } finally {
        this.loading.records = false;
      }
    },
    showEditHouseDialog(house) {
      this.editingHouse = { ...house };
      this.showEditDialog = true;
    },
    async updateHouse() {
      if (this.editingHouse.price < 0 || this.editingHouse.area < 0 || this.editingHouse.floor < 0) {
        alert('数值不能为负数！');
        return;
      }

      try {
        const response = await updateHouse(this.editingHouse.id, {
          price: this.editingHouse.price,
          area: this.editingHouse.area,
          floor: this.editingHouse.floor,
          salesperson_id: localStorage.getItem('userId')
        });

        if (response.data.status === 'success') {
          alert('房产信息更新成功！');
          this.showEditDialog = false;
          this.editingHouse = null;
          await this.fetchMyHouses();
        } else {
          alert(response.data.message || '更新失败');
        }
      } catch (error) {
        alert('更新失败，请稍后重试');
      }
    },
    cancelEdit() {
      this.showEditDialog = false;
      this.editingHouse = null;
    },
    async submitHouse() {
      if (this.newHouse.price < 0 || this.newHouse.area < 0 || this.newHouse.floor < 0) {
        alert('数值不能为负数！');
        return;
      }

      this.submitting = true;
      try {
        const userId = localStorage.getItem('userId');
        const response = await createHouse({
          ...this.newHouse,
          salesperson_id: userId
        });

        if (response.data.status === 'success') {
          alert('房产添加成功！');
          this.showAddHouseDialog = false;
          this.newHouse = { price: '', area: '', floor: '' };
          this.fetchMyHouses();
        } else {
          alert(response.data.message || '添加失败');
        }
      } catch (error) {
        alert('添加失败，请稍后重试');
      } finally {
        this.submitting = false;
      }
    },
    cancelAddHouse() {
      this.showAddHouseDialog = false;
      this.newHouse = { price: '', area: '', floor: '' };
    },
    logout() {
      // Handled by TopHeader
    },
    toggleShowAllRecords() {
      this.showAllRecords = !this.showAllRecords;
    },
    toggleShowAllAvailable() {
      this.showAllAvailable = !this.showAllAvailable;
    },
    toggleShowAllSold() {
      this.showAllSold = !this.showAllSold;
    },
    handlePasswordChanged() {
      this.showChangePassword = false;
      alert('密码修改成功！');
    },
    handleFilter(filters) {
      this.filters = { ...filters };
      this.showAllAvailable = false;
    }
  }
};
</script>

<style scoped>
.sales-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.main-content {
  display: grid;
  gap: 20px;
}

.section {
  margin-bottom: 30px;
}

.section h3 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.sales-count { background-color: #2196F3; }
.sales-amount { background-color: #4CAF50; }
.house-count { background-color: #FF9800; }

.stat-info { flex: 1; }

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  color: #666;
  margin-top: 5px;
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

.edit-btn, .add-btn, .submit-btn, .cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: opacity 0.2s;
}

.edit-btn { background-color: #2196F3; color: white; }
.add-btn { background-color: #4CAF50; color: white; }
.submit-btn { background-color: #4CAF50; color: white; }
.cancel-btn { background-color: #9e9e9e; color: white; }

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.price {
  color: #e74c3c;
  font-weight: bold;
}

.modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  position: relative;
}

.close {
  position: absolute;
  right: 15px; top: 10px;
  font-size: 24px;
  cursor: pointer;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.no-data {
  text-align: center;
  color: #666;
  padding: 20px;
}

.show-more {
  text-align: center;
  margin-top: 15px;
}

.toggle-btn {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  align-items: center;
}

.info-item {
  display: flex;
  gap: 10px;
  align-items: center;
}

.info-item .label {
  color: #666;
}

@media (max-width: 1200px) {
  .houses-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 900px) {
  .houses-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .houses-grid { grid-template-columns: 1fr; }
}
</style>