import axios from 'axios';

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 5000
});

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加 token 等头部信息
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default request;
