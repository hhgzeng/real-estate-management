<template>
  <div class="customer-dashboard">
    <TopHeader :title="`欢迎回来，${username}`" @logout="logout" />

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
          <HouseFilter @filter="handleFilter" />

          <div class="houses-grid" v-if="displayedHouses.length > 0">
            <HouseCard 
              v-for="house in displayedHouses" 
              :key="house.id" 
              :house="house"
            >
              <template #actions>
                <button class="buy-btn" @click="initiatePayment(house)">购买</button>
              </template>
            </HouseCard>
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
                <td class="price">¥{{ order.price.toLocaleString('zh-CN') }}</td>
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

    <!-- 支付对话框 -->
    <div v-if="showPaymentDialog" class="payment-dialog">
      <div class="payment-content">
        <h3>房产购买确认</h3>
        <div class="payment-info">
          <p>房产编号：{{ selectedHouse.id }}</p>
          <p>价格：¥{{ selectedHouse.price.toLocaleString('zh-CN') }}</p>
        </div>
        <div v-if="paymentQRCode" class="qr-code">
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
import ChangePassword from '@/components/common/ChangePassword.vue';
import TopHeader from '@/components/layout/TopHeader.vue';
import HouseFilter from '@/components/house/HouseFilter.vue';
import HouseCard from '@/components/house/HouseCard.vue';

export default {
  name: 'CustomerDashboard',
  components: {
    ChangePassword,
    TopHeader,
    HouseFilter,
    HouseCard
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
        
        if (this.filters.minPrice !== '' && price < this.filters.minPrice) return false;
        if (this.filters.maxPrice !== '' && price > this.filters.maxPrice) return false;
        if (this.filters.minArea !== '' && area < this.filters.minArea) return false;
        if (this.filters.maxArea !== '' && area > this.filters.maxArea) return false;
        
        return true;
      });
    },
    displayedHouses() {
      return this.showAllHouses ? this.filteredHouses : this.filteredHouses.slice(0, 8);
    },
    displayedOrders() {
      const sortedOrders = [...this.orders].sort((a, b) => 
        new Date(b.order_date) - new Date(a.order_date)
      );
      return this.showAllOrders ? sortedOrders : sortedOrders.slice(0, 5);
    }
  },
  created() {
    this.fetchHouses();
    this.fetchOrders();
  },
  methods: {
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
        alert('支付初始化失败，请重试');
        this.showPaymentDialog = false;
      }
    },
    async confirmPayment() {
      try {
        const orderResponse = await axios.post('http://localhost:8000/orders/create_order/', {
          house_id: this.selectedHouse.id,
          customer_id: localStorage.getItem('userId')
        });

        if (orderResponse.data.status === 'success') {
          alert('购买成功！');
          this.showPaymentDialog = false;
          this.selectedHouse = null;
          this.fetchHouses();
          this.fetchOrders();
        } else {
          alert(orderResponse.data.message || '购买失败');
        }
      } catch (error) {
        alert('操作失败，请重试');
      }
    },
    handleFilter(filters) {
      this.filters = { ...filters };
      this.showAllHouses = false;
    },
    logout() {
      // Handled by TopHeader
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
      alert('密码修改成功！');
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

.houses-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.buy-btn {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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

.close {
  position: absolute;
  right: 15px;
  top: 10px;
  font-size: 24px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #4CAF50;
  color: white;
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
  