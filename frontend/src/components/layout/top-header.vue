<template>
  <div class="top-header">
    <div class="logo">
      <h2>{{ title }}</h2>
    </div>
    <div class="user-actions">
      <template v-if="isLoggedIn">
        <span class="welcome">欢迎回来，{{ username }}</span>
        <button class="logout-btn" @click="handleLogout">退出登录</button>
      </template>
      <template v-else>
        <div class="auth-buttons">
          <router-link to="/login" class="btn">登录</router-link>
          <router-link :to="{ path: '/login', query: { tab: 'register' }}" class="btn">注册</router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TopHeader',
  props: {
    title: {
      type: String,
      default: '房产销售系统'
    }
  },
  data() {
    return {
      username: localStorage.getItem('username'),
      isLoggedIn: !!localStorage.getItem('userId')
    };
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      localStorage.removeItem('userId');
      this.isLoggedIn = false;
      this.$router.push('/');
      this.$emit('logout');
    }
  }
};
</script>

<style scoped>
.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 10px 0;
}

.logo h2 {
  margin: 0;
  color: #2c3e50;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome {
  color: #666;
  font-weight: 500;
}

.logout-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #757575;
  color: white;
  transition: opacity 0.2s;
}

.logout-btn:hover {
  opacity: 0.9;
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
</style>
