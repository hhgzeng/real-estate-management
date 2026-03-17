<template>
  <div class="change-password-container">
    <h2>修改密码</h2>
    <div class="form-group">
      <label for="oldPassword">旧密码：</label>
      <input
        type="password"
        id="oldPassword"
        v-model="oldPassword"
        class="form-control"
        required
      />
    </div>
    <div class="form-group">
      <label for="newPassword">新密码：</label>
      <input
        type="password"
        id="newPassword"
        v-model="newPassword"
        class="form-control"
        required
      />
    </div>
    <div class="form-group">
      <label for="confirmPassword">确认新密码：</label>
      <input
        type="password"
        id="confirmPassword"
        v-model="confirmPassword"
        class="form-control"
        required
      />
    </div>
    <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    <div class="success-message" v-if="successMessage">{{ successMessage }}</div>
    <button @click="changePassword" class="btn btn-primary">确认修改</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChangePassword',
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    async changePassword() {
      // 重置消息
      this.errorMessage = '';
      this.successMessage = '';

      // 表单验证
      if (!this.oldPassword || !this.newPassword || !this.confirmPassword) {
        this.errorMessage = '请填写所有字段';
        return;
      }

      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = '新密码和确认密码不匹配';
        return;
      }

      try {
        const userId = localStorage.getItem('userId'); // 从本地存储获取用户ID
        const response = await axios.post('http://localhost:8000/accounts/change_password/', {
          user_id: userId,
          old_password: this.oldPassword,
          new_password: this.newPassword
        });

        if (response.data.status === 'success') {
          this.successMessage = '密码修改成功';
          // 清空表单
          this.oldPassword = '';
          this.newPassword = '';
          this.confirmPassword = '';
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.message || '修改密码失败，请重试';
      }
    }
  }
};
</script>

<style scoped>
.change-password-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.error-message {
  color: red;
  margin-bottom: 10px;
}

.success-message {
  color: green;
  margin-bottom: 10px;
}

.btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}
</style> 