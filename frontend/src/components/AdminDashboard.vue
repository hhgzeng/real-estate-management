<template>
  <div class="admin-dashboard">
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
              <span class="value">管理员</span>
            </div>
            <div class="info-item">
              <button @click="showChangePassword = true" class="btn btn-primary">
                修改密码
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 房产管理部分 -->
      <div class="section">
        <h3>房产管理</h3>
        <div class="card">
          <h4>创建房产信息</h4>
          <form @submit.prevent="createHouse" class="form-grid">
            <div class="form-group">
              <label>价格</label>
              <input v-model="house.price" type="number" placeholder="请输入价格" required />
            </div>
            <div class="form-group">
              <label>面积</label>
              <input v-model="house.area" type="number" placeholder="请输入面积" required />
            </div>
            <div class="form-group">
              <label>楼层</label>
              <input v-model="house.floor" type="number" placeholder="请输入楼层" required />
            </div>
            <div class="form-group">
              <label>销售人员</label>
              <select v-model="house.salespersonId" required>
                <option value="">请选择销售人员</option>
                <option v-for="sp in salespeople" :key="sp.id" :value="sp.id">
                  {{ sp.username }}
                </option>
              </select>
            </div>
            <button type="submit" class="submit-btn">创建房产</button>
          </form>
        </div>

        <!-- 在售房产列表 -->
        <div class="section">
          <div class="section-header">
            <h3>在售房产</h3>
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
              <div v-for="house in displayedHouses" :key="house.id" class="house-card">
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
                    <span class="label">销售人员：</span>
                    <span class="value">{{ house.salesperson_name }}</span>
                  </div>
                </div>
                <div class="house-actions">
                  <button @click="editHouse(house)" class="edit-btn">修改</button>
                  <button @click="confirmDeleteHouse(house)" class="delete-btn">删除</button>
                </div>
              </div>
            </div>

            <div v-if="availableHouses.length > 8" class="show-more">
              <button @click="toggleShowAllHouses" class="toggle-btn">
                {{ showAllHouses ? '收起' : `显示更多` }}
              </button>
            </div>

            <div v-if="availableHouses.length === 0" class="no-data">
              暂无在售房产
            </div>
          </div>
        </div>
      </div>

      <!-- 销售记录部分 -->
      <div class="section">
        <h3>销售记录</h3>
        <div class="card">
          <table class="data-table" v-if="salesRecords.length">
            <thead>
              <tr>
                <th>房产ID</th>
                <th>顾客</th>
                <th>销售人员</th>
                <th>日期</th>
                <th>交易金额</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in filteredSalesRecords" :key="record.id">
                <td>{{ record.house__id }}</td>
                <td>{{ record.customer__username }}</td>
                <td>{{ record.salesperson__username }}</td>
                <td>{{ formatDate(record.order_date) }}</td>
                <td class="price">¥{{ formatPrice(record.house__price) }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="salesRecords.length > 5" class="show-more">
            <button @click="toggleRecords" class="toggle-btn">
              {{ showAllRecords ? '收起' : '显示更多' }}
            </button>
          </div>
          <p v-else class="no-data">暂无销售记录</p>
        </div>
      </div>

      <!-- 销售人员管理部分 -->
      <div class="section">
        <h3>销售人员管理</h3>
        <div class="card">
          <div class="salesperson-forms">
            <form @submit.prevent="createSalesperson" class="form-group">
              <h4>添加销售人员</h4>
              <input v-model="newSalesperson.username" placeholder="用户名" required />
              <input v-model="newSalesperson.password" type="password" placeholder="密码" required />
              <button type="submit" class="submit-btn">添加</button>
            </form>

            <form @submit.prevent="deleteSalesperson" class="form-group">
              <h4>删除销售人员</h4>
              <select v-model="deleteSalespersonId" required>
                <option value="">请选择要删除的销售人员</option>
                <option v-for="sp in salespeople" :key="sp.id" :value="sp.id">
                  {{ sp.username }}
                </option>
              </select>
              <button type="submit" class="delete-btn">删除</button>
            </form>
          </div>

          <!-- 销售人员列表 -->
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>用户名</th>
                <th>销售单数</th>
                <th>销售总额</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sp in salespeople" :key="sp.id">
                <td>{{ sp.id }}</td>
                <td>{{ sp.username }}</td>
                <td>{{ sp.sales_count }}单</td>
                <td>¥{{ formatPrice(sp.sales_amount) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 修改房产的对话框 -->
    <div v-if="showEditDialog" class="modal">
      <div class="modal-content">
        <h3>修改房产信息</h3>
        <form @submit.prevent="updateHouse" class="form-grid">
          <div class="form-group">
            <label>价格</label>
            <input v-model="editingHouse.price" type="number" required />
          </div>
          <div class="form-group">
            <label>面积</label>
            <input v-model="editingHouse.area" type="number" required />
          </div>
          <div class="form-group">
            <label>楼层</label>
            <input v-model="editingHouse.floor" type="number" required />
          </div>
          <div class="form-group">
            <label>销售人员</label>
            <select v-model="editingHouse.salesperson_id" required>
              <option v-for="sp in salespeople" :key="sp.id" :value="sp.id">
                {{ sp.username }}
              </option>
            </select>
          </div>
          <div class="modal-buttons">
            <button type="submit" class="submit-btn">保存</button>
            <button type="button" @click="showEditDialog = false" class="cancel-btn">取消</button>
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
  name: 'AdminDashboardPage',
  components: {
    ChangePassword,
  },
  data() {
    return {
      house: { price: '', area: '', floor: '', salespersonId: '' },
      houses: [],
      salesRecords: [],
      displayedRecords: [],
      showAllRecords: false,
      showAllHouses: false,
      newSalesperson: { username: '', password: '' },
      deleteSalespersonId: '',
      salespeople: [],
      showEditDialog: false,
      editingHouse: null,
      showChangePassword: false,
      username: localStorage.getItem('username'),
      filters: {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      }
    };
  },
  computed: {
    filteredSalesRecords() {
      const sortedRecords = [...this.salesRecords].sort((a, b) => 
        new Date(b.order_date) - new Date(a.order_date)
      );
      return this.showAllRecords ? sortedRecords : sortedRecords.slice(0, 5);
    },
    availableHouses() {
      const houses = this.houses.filter(house => house.status === 'available');
      return houses.filter(house => {
        const price = parseFloat(house.price);
        const area = parseFloat(house.area);
        
        if (this.filters.minPrice && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice && price > this.filters.maxPrice) return false;
        if (this.filters.minArea && area < this.filters.minArea) return false;
        if (this.filters.maxArea && area > this.filters.maxArea) return false;
        
        return true;
      });
    },
    displayedHouses() {
      return this.showAllHouses ? this.availableHouses : this.availableHouses.slice(0, 8);
    }
  },
  created() {
    this.initialize();
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
    toggleRecords() {
      this.showAllRecords = !this.showAllRecords;
    },
    async fetchHouses() {
      try {
        const response = await axios.get('http://localhost:8000/houses/get_houses/');
        this.houses = response.data;
      } catch (error) {
        alert('无法加载房产列表，请稍后重试！');
      }
    },
    async fetchSalespeople() {
      try {
        const response = await axios.get('http://localhost:8000/accounts/get_salespeople/');
        this.salespeople = response.data;
      } catch (error) {
        alert('无法加载销售人员列表，请稍后重试！');
      }
    },
    async createHouse() {
      // 验证输入数据
      if (this.house.price < 0) {
        alert('房产价格不能为负数！');
        return;
      }
      if (this.house.area < 0) {
        alert('房产面积不能为负数！');
        return;
      }
      if (this.house.floor < 0) {
        alert('楼层不能为负数！');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/houses/create_house/', {
          price: this.house.price,
          area: this.house.area,
          floor: this.house.floor,
          salesperson_id: this.house.salespersonId,
        });

        if (response.data.status === 'success') {
          alert('房产创建成功！');
          this.house = { price: '', area: '', floor: '', salespersonId: '' };
          this.fetchHouses();
        } else {
          alert(response.data.message || '创建房产失败！');
        }
      } catch (error) {
        if (error.response) {
          alert(`创建失败: ${error.response.data.message || '未知错误'}`);
        } else {
          alert('无法创建房产，请稍后重试。');
        }
      }
    },
    async fetchSalesRecords() {
      try {
        const response = await axios.get('http://localhost:8000/orders/get_sales_records/');
        this.salesRecords = response.data;
      } catch (error) {
        alert('无法加载销售记录，请稍后重试！');
      }
    },
    async createSalesperson() {
      try {
        const response = await axios.post('http://localhost:8000/accounts/manage_salesperson/', {
          action: 'create',
          username: this.newSalesperson.username,
          password: this.newSalesperson.password
        });
        if (response.data.status === 'success') {
          alert('销售人员创建成功！');
          this.newSalesperson = { username: '', password: '' };
          this.fetchSalespeople();
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        if (error.response && error.response.data) {
          if (error.response.data.message === 'Username already exists') {
            alert('创建失败：该用户名已存在，请使用其他用户名！');
          } else {
            alert(error.response.data.message || '创建失败，请稍后重试！');
          }
        } else {
          alert('创建失败，请稍后重试！');
        }
      }
    },
    async deleteSalesperson() {
      if (!confirm('确定要删除这个销售人员吗？')) return;
      
      try {
        const response = await axios.post('http://localhost:8000/accounts/manage_salesperson/', {
          action: 'delete',
          salesperson_id: this.deleteSalespersonId
        });
        if (response.data.status === 'success') {
          alert('销售人员删除成功！');
          this.deleteSalespersonId = '';
          this.fetchSalespeople();
        } else {
          alert(response.data.message);
        }
      } catch (error) {
        alert('无法删除销售人员，请稍后重试！');
      }
    },
    editHouse(house) {
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
          salesperson_id: this.editingHouse.salesperson_id
        });

        if (response.data.status === 'success') {
          alert('房产信息更新成功！');
          this.showEditDialog = false;
          this.fetchHouses();
        } else {
          alert(response.data.message || '更新失败！');
        }
      } catch (error) {
        alert('无法更新房产信息，请稍后重试！');
      }
    },
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      localStorage.removeItem('userId');
      this.$router.push('/');
    },
    async initialize() {
      await Promise.all([
        this.fetchHouses(),
        this.fetchSalespeople(),
        this.fetchSalesRecords()
      ]);
    },
    formatPrice(price) {
      if (price === null || price === undefined || isNaN(price)) {
        return '0';
      }
      return parseFloat(price).toLocaleString('zh-CN');
    },
    async confirmDeleteHouse(house) {
      if (confirm(`确定要删除房产 #${house.id} 吗？此操作不可撤销。`)) {
        try {
          const response = await axios.post(`http://localhost:8000/houses/delete_house/${house.id}/`);
          if (response.data.status === 'success') {
            alert('房产删除成功！');
            this.fetchHouses();
          } else {
            alert(response.data.message || '删除失败！');
          }
        } catch (error) {
          alert('删除失败，请稍后重试！');
        }
      }
    },
    toggleShowAllHouses() {
      this.showAllHouses = !this.showAllHouses;
    },
    handlePasswordChanged() {
      this.showChangePassword = false;
      // 可以添加其他处理逻辑，比如显示成功消息
    },
    applyFilters() {
      // 重置显示状态，确保从第一页开始显示
      this.showAllHouses = false;
    },
    resetFilters() {
      this.filters = {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      };
      // 重置显示状态
      this.showAllHouses = false;
    },
  },
};
</script>

<style scoped>
.admin-dashboard {
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

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
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

input, select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
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

.submit-btn, .edit-btn, .delete-btn, .refresh-btn, .logout-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.refresh-btn {
  background-color: #607D8B;
  color: white;
}

.logout-btn {
  background-color: #757575;
  color: white;
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
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.salesperson-forms {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.no-data {
  text-align: center;
  color: #666;
  padding: 20px;
}

button:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .salesperson-forms {
    grid-template-columns: 1fr;
  }
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

.action-buttons {
  display: flex;
  gap: 8px;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.delete-btn:hover {
  opacity: 0.9;
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
  gap: 10px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.edit-btn {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn:hover {
  background-color: #2980b9;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.delete-btn:hover {
  background-color: #c0392b;
}

.toggle-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
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

.password-section {
  margin: 20px 0;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  position: relative;
  width: 90%;
  max-width: 500px;
}

.close {
  position: absolute;
  right: 10px;
  top: 10px;
  font-size: 24px;
  cursor: pointer;
}

.close:hover {
  color: #666;
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

.filter-btn:hover {
  background-color: #1976D2;
}

.reset-btn:hover {
  background-color: #757575;
}

@media (max-width: 768px) {
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
