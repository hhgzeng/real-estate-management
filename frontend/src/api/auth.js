import request from '@/utils/request';

export function login(data) {
  return request({
    url: '/accounts/login/',
    method: 'post',
    data
  });
}

export function register(data) {
  return request({
    url: '/accounts/register/',
    method: 'post',
    data
  });
}

export function getSalespeople() {
  return request({
    url: '/accounts/get_salespeople/',
    method: 'get'
  });
}

export function manageSalesperson(data) {
  return request({
    url: '/accounts/manage_salesperson/',
    method: 'post',
    data
  });
}

export function changePassword(data) {
  return request({
    url: '/accounts/change_password/',
    method: 'post',
    data
  });
}
