<template>
  <div class="register-container">
    <div class="register-card">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input type="text" v-model="username" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input type="password" v-model="password" required />
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input type="password" v-model="confirmPassword" required />
        </div>
        <div class="form-group">
          <label>用户类型</label>
          <select v-model="role" required>
            <option value="customer">普通用户</option>
            <option value="salesperson">销售人员</option>
          </select>
        </div>
        <button type="submit" class="register-btn">注册</button>
        <div class="login-link">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      role: 'customer'
    };
  },
  methods: {
    async handleRegister() {
      if (this.password !== this.confirmPassword) {
        alert('两次输入的密码不一致');
        return;
      }

      try {
        const response = await axios.post('http://localhost:8000/accounts/register/', {
          username: this.username,
          password: this.password,
          role: this.role
        });

        if (response.data.status === 'success') {
          alert('注册成功！');
          this.$router.push('/login');
        } else {
          alert(response.data.message || '注册失败，请重试');
        }
      } catch (error) {
        console.error('Registration error:', error);
        alert('注册失败，请重试');
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 20px;
}

.register-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #666;
}

input, select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus, select:focus {
  outline: none;
  border-color: #2196F3;
}

.register-btn {
  width: 100%;
  padding: 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-btn:hover {
  background-color: #1976D2;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link a {
  color: #2196F3;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
  