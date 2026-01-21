<template>
  <div class="login-container">
    <div class="login-card">
      <div class="modal-content">
        <h2 class="title">房产销售管理系统</h2>
        <div class="tabs">
          <button 
            :class="['tab-btn', { active: !isRegistering }]" 
            @click="isRegistering = false"
          >
            登录
          </button>
          <button 
            :class="['tab-btn', { active: isRegistering }]" 
            @click="isRegistering = true"
          >
            注册
          </button>
        </div>
      </div>

      <!-- 登录表单 -->
      <form v-if="!isRegistering" @submit.prevent="login" class="form">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="loginForm.username" 
            type="text" 
            required 
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="loginForm.password" 
            type="password" 
            required 
            placeholder="请输入密码"
          />
        </div>
        <button type="submit" class="submit-btn">登录</button>
        <button type="button" class="back-home-btn" @click="$router.push('/')">返回主页</button>
      </form>

      <!-- 注册表单 -->
      <form v-else @submit.prevent="register" class="form">
        <div class="form-group">
          <label>用户名</label>
          <input 
            v-model="registerForm.username" 
            type="text" 
            required 
            placeholder="请输入用户名"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input 
            v-model="registerForm.password" 
            type="password" 
            required 
            placeholder="请输入密码"
          />
        </div>
        <div class="form-group">
          <label>角色</label>
          <select v-model="registerForm.role" required>
            <option value="">请选择角色</option>
            <option value="customer">客户</option>
            <option value="salesperson">销售人员</option>
          </select>
        </div>
        <button type="submit" class="submit-btn">注册</button>
        <button type="button" class="back-home-btn" @click="$router.push('/')">返回主页</button>
      </form>

      <!-- 错误提示 -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      isRegistering: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        role: ''
      },
      error: ''
    };
  },
  methods: {
    async login() {
      try {
        this.error = '';
        const response = await axios.post('http://localhost:8000/accounts/login/', {
          username: this.loginForm.username,
          password: this.loginForm.password
        });

        if (response.data.status === 'success') {
          // 保存用户信息
          localStorage.setItem('role', response.data.role);
          localStorage.setItem('username', response.data.username);
          localStorage.setItem('userId', response.data.user_id);

          // 根据角色跳转到不同的页面
          switch (response.data.role) {
            case 'admin':
              this.$router.push('/admin-dashboard');
              break;
            case 'customer':
              this.$router.push('/customer-dashboard');
              break;
            case 'salesperson':
              this.$router.push('/sales-dashboard');
              break;
            default:
              this.error = '未知的用户角色';
          }
        } else {
          if (response.data.message === 'Invalid credentials') {
            this.error = '用户名或密码错误';
          } else if (response.data.message === 'User not found') {
            this.error = '用户不存在';
          } else {
            this.error = '登录失败，请稍后重试';
          }
        }
      } catch (error) {
        if (error.response?.status === 401) {
          this.error = '用户名或密码错误';
        } else if (error.response?.status === 404) {
          this.error = '用户不存在';
        } else {
          this.error = '登录失败，请稍后重试';
        }
      }
    },
    async register() {
      try {
        this.error = '';
        const response = await axios.post('http://localhost:8000/accounts/register/', {
          username: this.registerForm.username,
          password: this.registerForm.password,
          role: this.registerForm.role
        });

        if (response.data.message === 'Registration successful') {
          alert('注册成功！请登录');
          this.isRegistering = false;
          this.loginForm.username = this.registerForm.username;
          this.loginForm.password = '';
          // 清空注册表单
          this.registerForm = {
            username: '',
            password: '',
            role: ''
          };
        } else {
          this.error = '注册失败，请稍后重试';
        }
      } catch (error) {
        if (error.response?.data?.message === 'Username already exists') {
          this.error = '用户名已存在，请更换其他用户名';
        } else if (error.response?.data?.message === 'Invalid role') {
          this.error = '请选择正确的用户角色';
        } else if (error.response?.data?.message === 'Username and password are required') {
          this.error = '用户名和密码不能为空';
        } else {
          this.error = '注册失败，请稍后重试';
        }
      }
    }
  },
  created() {
    // 从 URL 参数判断是否显示注册表单
    const urlParams = new URLSearchParams(window.location.search);
    this.isRegistering = urlParams.get('tab') === 'register';
  },
  watch: {
    // 监听路由变化
    '$route.query': {
      handler(query) {
        this.isRegistering = query.tab === 'register';
      },
      immediate: true
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  padding: 30px;
}

.modal-content {
  text-align: center;
  margin-bottom: 30px;
  position: relative;
}

.modal-content h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-btn {
  padding: 8px 20px;
  border: none;
  background: none;
  color: #666;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-btn.active {
  color: #2196F3;
  border-bottom-color: #2196F3;
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
  color: #2c3e50;
  font-weight: 500;
}

input, select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

input:focus, select:focus {
  border-color: #2196F3;
  outline: none;
}

.submit-btn {
  background-color: #2196F3;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #1976D2;
}

.back-btn {
  background-color: #9e9e9e;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.back-btn:hover {
  background-color: #757575;
}

.error-message {
  color: #f44336;
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
}

.back-home-btn {
  width: 100%;
  padding: 12px;
  background-color: #607D8B;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.back-home-btn:hover {
  background-color: #455A64;
}

@media (max-width: 480px) {
  .login-card {
    padding: 20px;
  }

  .tab-btn {
    padding: 8px 15px;
    font-size: 14px;
  }

  input, select, .submit-btn, .back-btn {
    padding: 10px;
    font-size: 14px;
  }
}
</style>
