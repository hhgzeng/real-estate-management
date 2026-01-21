<template>
  <div class="sales-dashboard">
    <div class="header">
      <h2>欢迎回来，{{ username }}</h2>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>

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
              <div class="stat-value">¥ {{ formatPrice(salesStats.totalAmount || 0) }}</div>
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
          <!-- 添加筛选功能 -->
          <div class="filters">
            <div class="filter-group">
              <label>价格区间：</label>
              <input 
                v-model.number="filters.minPrice" 
                type="number" 
                placeholder="最低价" 
              />
              <span>-</span>
              <input 
                v-model.number="filters.maxPrice" 
                type="number" 
                placeholder="最高价" 
              />
            </div>
            <div class="filter-group">
              <label>面积区间：</label>
              <input 
                v-model.number="filters.minArea" 
                type="number" 
                placeholder="最小面积" 
              />
              <span>-</span>
              <input 
                v-model.number="filters.maxArea" 
                type="number" 
                placeholder="最大面积" 
              />
            </div>
            <button class="filter-btn" @click="applyFilters">筛选</button>
            <button class="reset-btn" @click="resetFilters">重置</button>
          </div>

          <div class="houses-grid">
            <div v-for="house in displayedAvailableHouses" :key="house.id" class="house-card">
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
              </div>
              <div class="house-actions">
                <button class="edit-btn" @click="showEditHouseDialog(house)">修改</button>
              </div>
            </div>
          </div>

          <div v-if="filteredAvailableHouses.length > 8" class="show-more">
            <button @click="toggleShowAllAvailable" class="toggle-btn">
              {{ showAllAvailable ? '收起' : `显示更多` }}
            </button>
          </div>
          <div v-if="filteredAvailableHouses.length === 0" class="no-data">
            暂无在售房产
          </div>
        </div>
      </div>

      <!-- 已售房产 -->
      <div class="section">
        <h3>已售房产</h3>
        <div class="card">
          <div class="houses-grid">
            <div v-for="house in displayedSoldHouses" :key="house.id" class="house-card">
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
                  <span class="value status sold">已售出</span>
                </div>
              </div>
            </div>
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
                <td class="price">¥{{ formatPrice(record.price) }}</td>
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
            <button type="submit" class="submit-btn">确认</button>
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
import axios from 'axios';
import ChangePassword from './ChangePassword.vue';

export default {
  name: 'SalesDashboard',
  components: {
    ChangePassword
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
        
        if (this.filters.minPrice && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice && price > this.filters.maxPrice) return false;
        if (this.filters.minArea && area < this.filters.minArea) return false;
        if (this.filters.maxArea && area > this.filters.maxArea) return false;
        
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
      // 先按时间倒序排序
      const sortedRecords = [...this.salesRecords].sort((a, b) => 
        new Date(b.order_date) - new Date(a.order_date)
      );
      
      if (this.showAllRecords) {
        return sortedRecords;
      }
      return sortedRecords.slice(0, 5);
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
    formatPrice(price) {
      return parseFloat(price).toLocaleString('zh-CN');
    },
    formatDate(date) {
      return new Date(date).toLocaleString('zh-CN');
    },
    async fetchSalesStats() {
      this.loading.stats = true;
      this.error.stats = '';
      try {
        const userId = localStorage.getItem('userId');
        const response = await axios.get(`http://localhost:8000/orders/sales_stats/?salesperson_id=${userId}`);
        if (response.data.status === 'success') {
          this.salesStats = {
            totalSales: response.data.totalSales,
            totalAmount: response.data.totalAmount
          };
        } else {
          this.error.stats = response.data.message || '获取销售统计失败';
        }
      } catch (error) {
        console.error('获取销售统计错误:', error);
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
        const response = await axios.get(`http://localhost:8000/houses/my_houses/?salesperson_id=${userId}`);
        this.myHouses = response.data;
      } catch (error) {
        console.error('获取房产列表错误:', error);
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
        const response = await axios.get(`http://localhost:8000/orders/my_sales/?salesperson_id=${userId}`);
        this.salesRecords = response.data;
      } catch (error) {
        console.error('获取销售记录错误:', error);
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
      // 验证输入数据
      if (this.editingHouse.price < 0) {
        alert('房产价格不能为负数！');
        return;
      }
      if (this.editingHouse.area < 0) {
        alert('房产面积不能为负数！');
        return;
      }
      if (this.editingHouse.floor < 0) {
        alert('楼层不能为负数！');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:8000/houses/update_house/${this.editingHouse.id}/`, {
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
        console.error('更新失败:', error);
        alert('更新失败，请稍后重试');
      }
    },
    cancelEdit() {
      this.showEditDialog = false;
      this.editingHouse = null;
    },
    async submitHouse() {
      // 验证输入数据
      if (this.newHouse.price < 0) {
        alert('房产价格不能为负数！');
        return;
      }
      if (this.newHouse.area < 0) {
        alert('房产面积不能为负数！');
        return;
      }
      if (this.newHouse.floor < 0) {
        alert('楼层不能为负数！');
        return;
      }

      try {
        const userId = localStorage.getItem('userId');
        const response = await axios.post('http://localhost:8000/houses/create_house/', {
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
      }
    },
    cancelAddHouse() {
      this.showAddHouseDialog = false;
      this.newHouse = { price: '', area: '', floor: '' };
    },
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      localStorage.removeItem('userId');
      this.$router.push('/');
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
    applyFilters() {
      // 重置显示状态，确保从第一页开始显示
      this.showAllAvailable = false;
    },
    resetFilters() {
      this.filters = {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      };
      // 重置显示状态
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
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h2 {
  margin: 0;
  color: #2c3e50;
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

.sales-count {
  background-color: #2196F3;
}

.sales-amount {
  background-color: #4CAF50;
}

.house-count {
  background-color: #FF9800;
}

.stat-info {
  flex: 1;
}

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

.house-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
}

.house-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.house-info {
  flex: 1;
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

.value.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
}

.value.status.available {
  background-color: #4CAF50;
  color: white;
}

.value.status.sold {
  background-color: #9e9e9e;
  color: white;
}

.house-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
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

.form-group label {
  font-weight: 500;
  color: #2c3e50;
}

input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.logout-btn {
  background-color: #757575;
  color: white;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.edit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
}

.no-data {
  text-align: center;
  color: #666;
  padding: 20px;
}

button:hover:not(:disabled) {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .houses-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 15px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stat-value {
    font-size: 20px;
  }
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #e53935;
  text-align: center;
  padding: 20px;
  background-color: #ffebee;
  border-radius: 4px;
  margin: 10px 0;
}

.show-more {
  text-align: center;
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.toggle-btn {
  background-color: #f0f0f0;
  color: #333;
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background-color: #e0e0e0;
}

.user-info {
  margin-bottom: 20px;
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
  min-width: 70px;
}

.info-item .value {
  font-weight: 500;
  color: #2c3e50;
}

.btn-primary {
  background-color: #007bff;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-group input {
  width: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-btn {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-btn {
  background-color: #9e9e9e;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
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
  font-weight: 500;
  transition: background-color 0.3s;
}

.toggle-btn:hover {
  background-color: #1976D2;
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
  
  .filters {
    flex-direction: column;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .filter-group input {
    flex: 1;
  }
}
</style>
  