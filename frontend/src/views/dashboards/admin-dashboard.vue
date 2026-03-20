<template>
  <div class="admin-dashboard">
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
            <button type="submit" class="submit-btn" style="height: fit-content; align-self: end;">创建房产</button>
          </form>
        </div>

        <!-- 在售房产列表 -->
        <div class="section">
          <div class="section-header">
            <h3>在售房产</h3>
          </div>
          <div class="card">
            <HouseFilter @filter="handleFilter" />

            <div class="houses-grid" v-if="displayedHouses.length > 0">
              <HouseCard 
                v-for="house in displayedHouses" 
                :key="house.id" 
                :house="house"
              >
                <template #actions>
                  <button @click="editHouse(house)" class="edit-btn">修改</button>
                  <button @click="confirmDeleteHouse(house)" class="delete-btn">删除</button>
                </template>
              </HouseCard>
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
                <td class="price">¥{{ record.house__price.toLocaleString('zh-CN') }}</td>
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
              <button type="submit" class="submit-btn" style="width: fit-content; margin-top: 10px;">添加</button>
            </form>

            <form @submit.prevent="deleteSalesperson" class="form-group">
              <h4>删除销售人员</h4>
              <select v-model="deleteSalespersonId" required>
                <option value="">请选择要删除的销售人员</option>
                <option v-for="sp in salespeople" :key="sp.id" :value="sp.id">
                  {{ sp.username }}
                </option>
              </select>
              <button type="submit" class="delete-btn" style="width: fit-content; margin-top: 10px;">删除</button>
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
                <td>¥{{ sp.sales_amount.toLocaleString('zh-CN') }}</td>
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
import { getHouses, createHouse, updateHouse, deleteHouse } from '@/api/house';
import { getSalespeople, manageSalesperson } from '@/api/auth';
import { getSalesRecords } from '@/api/order';
import ChangePassword from '@/components/common/change-password.vue';
import TopHeader from '@/components/layout/top-header.vue';
import HouseFilter from '@/components/house/house-filter.vue';
import HouseCard from '@/components/house/house-card.vue';

export default {
  name: 'AdminDashboardPage',
  components: {
    ChangePassword,
    TopHeader,
    HouseFilter,
    HouseCard
  },
  data() {
    return {
      house: { price: '', area: '', floor: '', salespersonId: '' },
      houses: [],
      salesRecords: [],
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
        
        if (this.filters.minPrice !== '' && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice !== '' && price > this.filters.maxPrice) return false;
        if (this.filters.minArea !== '' && area < this.filters.minArea) return false;
        if (this.filters.maxArea !== '' && area > this.filters.maxArea) return false;
        
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
        const response = await getHouses();
        this.houses = response.data;
      } catch (error) {
        alert('无法加载房产列表，请稍后重试！');
      }
    },
    async fetchSalespeople() {
      try {
        const response = await getSalespeople();
        this.salespeople = response.data;
      } catch (error) {
        alert('无法加载销售人员列表，请稍后重试！');
      }
    },
    async createHouse() {
      if (this.house.price < 0 || this.house.area < 0 || this.house.floor < 0) {
        alert('数值不能为负数！');
        return;
      }

      try {
        const response = await createHouse({
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
        alert('无法创建房产，请稍后重试。');
      }
    },
    async fetchSalesRecords() {
      try {
        const response = await getSalesRecords();
        this.salesRecords = response.data;
      } catch (error) {
        alert('无法加载销售记录，请稍后重试！');
      }
    },
    async createSalesperson() {
      try {
        const response = await manageSalesperson({
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
        alert('创建失败，请稍后重试！');
      }
    },
    async deleteSalesperson() {
      if (!confirm('确定要删除这个销售人员吗？')) return;
      
      try {
        const response = await manageSalesperson({
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
      if (this.editingHouse.price < 0 || this.editingHouse.area < 0 || this.editingHouse.floor < 0) {
        alert('数值不能为负数！');
        return;
      }

      try {
        const response = await updateHouse(this.editingHouse.id, {
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
      // Handled by TopHeader
    },
    async initialize() {
      await Promise.all([
        this.fetchHouses(),
        this.fetchSalespeople(),
        this.fetchSalesRecords()
      ]);
    },
    async confirmDeleteHouse(house) {
      if (confirm(`确定要删除房产 #${house.id} 吗？`)) {
        try {
          const response = await deleteHouse(house.id);
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
    },
    handleFilter(filters) {
      this.filters = { ...filters };
      this.showAllHouses = false;
    }
  },
};
</script>

<style scoped>
.admin-dashboard {
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

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  align-items: flex-end;
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
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.submit-btn, .btn-primary {
  background-color: #2196F3;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.submit-btn:hover, .btn-primary:hover {
  opacity: 0.9;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  right: 15px;
  top: 10px;
  font-size: 24px;
  cursor: pointer;
}

.salesperson-forms {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.houses-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.edit-btn {
  background-color: #4CAF50;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #9e9e9e;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
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
