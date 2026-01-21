<template>
  <div>
    <h2>欢迎来到房产管理系统</h2>
    <p>您好，{{ userRole }}！以下是可选房产信息：</p>

    <div v-if="houses.length === 0">暂无可售房产信息。</div>
    <div v-else>
      <div v-for="house in houses" :key="house.id" class="house">
        <p>房产ID: {{ house.id }}</p>
        <p>价格: ¥{{ house.price }}</p>
        <p>面积: {{ house.area }} 平方米</p>
        <p>楼层: 第{{ house.floor }}层</p>
        <button @click="placeOrder(house.id)">购买</button>
      </div>
    </div>

    <button @click="logout">退出登录</button>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardPage',
  data() {
    return {
      userRole: '',
      houses: [], // 存储房产信息
      errorMessage: '', // 错误信息
    };
  },
  created() {
    this.userRole = localStorage.getItem('role') || '访客';
    this.fetchHouses(); // 获取房产信息
  },
  methods: {
    async fetchHouses() {
      try {
        const response = await axios.get('http://localhost:8000/houses/get_houses/');
        this.houses = response.data;
      } catch (error) {
        this.errorMessage = '无法获取房产信息，请稍后再试！';
      }
    },
    async placeOrder(houseId) {
      try {
        const customerId = localStorage.getItem('customerId'); // 假设已保存用户ID
        const response = await axios.post('http://localhost:8000/orders/create_order/', {
          house_id: houseId,
          customer_id: customerId,
        });

        if (response.data.status === 'success') {
          alert('下单成功！');
          this.fetchHouses(); // 刷新房产信息
        } else {
          alert(response.data.message || '下单失败！');
        }
      } catch (error) {
        this.errorMessage = '无法下单，请稍后再试！';
      }
    },
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('customerId');
      this.$router.push('/login');
    },
  },
};
</script>

<style>
.house {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
}
</style>
