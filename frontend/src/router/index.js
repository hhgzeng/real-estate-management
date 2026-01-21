import { createRouter, createWebHistory } from 'vue-router';

// 引入组件
import HomePage from '@/components/HomePage.vue';
import LoginPage from '@/components/Login.vue';
import RegisterPage from '@/components/Register.vue';
import AdminDashboardPage from '@/components/AdminDashboard.vue';
import SalesDashboardPage from '@/components/SalesDashboard.vue';
import CustomerDashboardPage from '@/components/CustomerDashboard.vue';

// 定义路由
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboardPage,
    meta: { requiresAuth: true, role: 'admin' },
  },
  {
    path: '/sales-dashboard',
    name: 'SalesDashboard',
    component: SalesDashboardPage,
    meta: { requiresAuth: true, role: 'salesperson' },
  },
  {
    path: '/customer-dashboard',
    name: 'CustomerDashboard',
    component: CustomerDashboardPage,
    meta: { requiresAuth: true, role: 'customer' },
  }
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 如果是访问登录页，直接放行
  if (to.path === '/login') {
    next();
    return;
  }

  const role = localStorage.getItem('role');
  
  // 如果需要登录才能访问
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!role) {
      // 未登录，跳转到登录页面
      next('/login');
      return;
    }
    
    // 如果路由定义了特定角色，而当前用户角色不符
    if (to.meta.role && to.meta.role !== role) {
      alert('无访问权限');
      // 根据角色重定向到对应的仪表板
      switch (role) {
        case 'admin':
          next('/admin-dashboard');
          break;
        case 'salesperson':
          next('/sales-dashboard');
          break;
        case 'customer':
          next('/customer-dashboard');
          break;
        default:
          next('/login');
      }
      return;
    }
  }
  
  next();
});

export default router;

