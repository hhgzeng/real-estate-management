<template>
  <div class="customer-dashboard">
    <div class="header">
      <h2>欢迎回来，{{ username }}</h2>
      <button class="logout-btn" @click="logout">退出登录</button>
    </div>

    <div class="main-content">
      <!-- 用户信息卡片 -->
      <div class="section">
        <div class="card user-info">
          <h3>我的信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">用户名：</span>
              <span class="value">{{ username }}</span>
            </div>
            <div class="info-item">
              <span class="label">角色：</span>
              <span class="value">客户</span>
            </div>
            <div class="info-item">
              <button @click="showChangePassword = true" class="btn btn-primary">
                修改密码
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 在售房产列表 -->
      <div class="section">
        <h3>在售房产</h3>
        <div class="card">
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
                <button class="buy-btn" @click="initiatePayment(house)">购买</button>
              </div>
            </div>
          </div>

          <div v-if="filteredHouses.length > 8" class="show-more">
            <button @click="toggleShowAllHouses" class="toggle-btn">
              {{ showAllHouses ? '收起' : `显示更多` }}
            </button>
          </div>

          <div v-if="filteredHouses.length === 0" class="no-data">
            暂无符合条件的房产
          </div>
        </div>
      </div>

      <!-- 我的订单 -->
      <div class="section">
        <h3>我的订单</h3>
        <div class="card">
          <table class="data-table" v-if="orders.length">
            <thead>
              <tr>
                <th>订单编号</th>
                <th>房产信息</th>
                <th>销售人员</th>
                <th>交易日期</th>
                <th>价格</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in displayedOrders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ order.house_info }}</td>
                <td>{{ order.salesperson_name }}</td>
                <td>{{ formatDate(order.order_date) }}</td>
                <td class="price">¥{{ formatPrice(order.price) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="show-more" v-if="orders.length > 5">
            <button @click="toggleShowAllOrders" class="toggle-btn">
              {{ showAllOrders ? '收起' : '显示更多' }}
            </button>
          </div>
          <div v-if="orders.length === 0" class="no-data">
            暂无购买记录
          </div>
        </div>
      </div>
    </div>

    <!-- 购买确认对话框 -->
    <div v-if="showBuyDialog" class="modal">
      <div class="modal-content">
        <h3>确认购买</h3>
        <div class="confirm-content">
          <p>您确定要购买以下房产吗？</p>
          <div class="house-details" v-if="selectedHouse">
            <div class="detail-row">
              <span class="label">房产编号：</span>
              <span class="value">{{ selectedHouse.id }}</span>
            </div>
            <div class="detail-row">
              <span class="label">价格：</span>
              <span class="value price">¥{{ formatPrice(selectedHouse.price) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">面积：</span>
              <span class="value">{{ selectedHouse.area }}㎡</span>
            </div>
            <div class="detail-row">
              <span class="label">楼层：</span>
              <span class="value">{{ selectedHouse.floor }}层</span>
            </div>
          </div>
        </div>
        <div class="modal-buttons">
          <button class="confirm-btn" @click="confirmPurchase">确认购买</button>
          <button class="cancel-btn" @click="showBuyDialog = false">取消</button>
        </div>
      </div>
    </div>

    <!-- 支付对话框 -->
    <div v-if="showPaymentDialog" class="payment-dialog">
      <div class="payment-content">
        <h3>房产购买确认</h3>
        <div class="payment-info">
          <p>房产编号：{{ selectedHouse.id }}</p>
          <p>价格：¥{{ formatPrice(selectedHouse.price) }}</p>
        </div>
        <div class="qr-code" v-if="paymentQRCode">
          <img :src="'data:image/png;base64,' + paymentQRCode" alt="支付二维码">
          <p>请使用微信扫码支付</p>
        </div>
        <div class="payment-actions">
          <button @click="cancelPayment">取消</button>
          <button @click="confirmPayment" class="confirm-btn">确认已支付</button>
        </div>
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
  name: 'CustomerDashboard',
  components: {
    ChangePassword,
  },
  data() {
    return {
      username: localStorage.getItem('username'),
      houses: [],
      orders: [],
      filters: {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      },
      showBuyDialog: false,
      selectedHouse: null,
      showPaymentDialog: false,
      paymentQRCode: null,
      orderNumber: null,
      showAllOrders: false,
      showAllHouses: false,
      showChangePassword: false
    };
  },
  computed: {
    filteredHouses() {
      return this.houses.filter(house => {
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
      return this.showAllHouses ? this.filteredHouses : this.filteredHouses.slice(0, 8);
    },
    displayedOrders() {
      // 先按时间倒序排序
      const sortedOrders = [...this.orders].sort((a, b) => 
        new Date(b.order_date) - new Date(a.order_date)
      );
      
      if (this.showAllOrders) {
        return sortedOrders;
      }
      return sortedOrders.slice(0, 5);
    }
  },
  created() {
    this.fetchHouses();
    this.fetchOrders();
  },
  methods: {
    formatPrice(price) {
      return parseFloat(price).toLocaleString('zh-CN');
    },
    formatDate(date) {
      return new Date(date).toLocaleString('zh-CN');
    },
    async fetchHouses() {
      try {
        const response = await axios.get('http://localhost:8000/houses/get_houses/');
        this.houses = response.data;
      } catch (error) {
        alert('获取房产列表失败，请稍后重试');
      }
    },
    async fetchOrders() {
      try {
        const userId = localStorage.getItem('userId');
        const response = await axios.get(`http://localhost:8000/orders/my_orders/?customer_id=${userId}`);
        this.orders = response.data;
      } catch (error) {
        alert('获取订单列表失败，请稍后重试');
      }
    },
    showBuyConfirm(house) {
      this.selectedHouse = house;
      this.showBuyDialog = true;
    },
    async confirmPurchase() {
      // 调用支付接口
      await this.initiatePayment(this.selectedHouse);
      this.showBuyDialog = false;
    },
    async initiatePayment(house) {
      this.selectedHouse = house;
      this.showPaymentDialog = true;
      
      try {
        const response = await axios.post('http://localhost:8000/orders/create_payment/', {
          house_id: house.id,
          amount: house.price
        });
        
        if (response.data.status === 'success') {
          this.paymentQRCode = response.data.qr_code;
          this.orderNumber = response.data.order_number;
        } else {
          alert('生成支付二维码失败，请重试');
          this.showPaymentDialog = false;
        }
      } catch (error) {
        console.error('支付初始化失败:', error);
        alert('支付初始化失败，请重试');
        this.showPaymentDialog = false;
      }
    },
    async confirmPayment() {
      try {
        // 直接创建订单
        const orderResponse = await axios.post('http://localhost:8000/orders/create_order/', {
          house_id: this.selectedHouse.id,
          customer_id: localStorage.getItem('userId')
        });

        if (orderResponse.data.status === 'success') {
          alert('购买成功！');
          this.showPaymentDialog = false;
          this.selectedHouse = null;
          // 刷新房产和订单列表
          this.fetchHouses();
          this.fetchOrders();
        } else {
          alert(orderResponse.data.message || '购买失败');
        }
      } catch (error) {
        console.error('操作失败:', error);
        alert('操作失败，请重试');
      }
    },
    applyFilters() {
      // 过滤功能已通过计算属性实现
    },
    resetFilters() {
      this.filters = {
        minPrice: '',
        maxPrice: '',
        minArea: '',
        maxArea: ''
      };
    },
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      localStorage.removeItem('userId');
      this.$router.push('/');
    },
    cancelPayment() {
      this.showPaymentDialog = false;
      this.selectedHouse = null;
      this.paymentQRCode = null;
      this.orderNumber = null;
    },
    toggleShowAllOrders() {
      this.showAllOrders = !this.showAllOrders;
    },
    handlePasswordChanged() {
      this.showChangePassword = false;
      // 可以添加其他处理逻辑，比如显示成功消息
    },
    toggleShowAllHouses() {
      this.showAllHouses = !this.showAllHouses;
    }
  }
};
</script>

<style scoped>
.customer-dashboard {
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

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

.house-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: auto;
}

.buy-btn {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.buy-btn:hover {
  background-color: #388E3C;
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

.confirm-content {
  margin: 20px 0;
}

.house-details {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  margin-top: 10px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.logout-btn {
  background-color: #757575;
  color: white;
}

.filter-btn {
  background-color: #2196F3;
  color: white;
}

.reset-btn {
  background-color: #9e9e9e;
  color: white;
}

.confirm-btn {
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

button:hover {
  opacity: 0.9;
}

.payment-dialog {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.payment-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

.payment-info {
  margin: 20px 0;
}

.qr-code {
  margin: 20px 0;
}

.qr-code img {
  max-width: 200px;
  margin: 10px auto;
}

.payment-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
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
  