import request from '@/utils/request';

export function getMyOrders(customerId) {
  return request({
    url: `/orders/my_orders/?customer_id=${customerId}`,
    method: 'get'
  });
}

export function createPayment(data) {
  return request({
    url: '/orders/create_payment/',
    method: 'post',
    data
  });
}

export function createOrder(data) {
  return request({
    url: '/orders/create_order/',
    method: 'post',
    data
  });
}

export function getSalesRecords() {
  return request({
    url: '/orders/get_sales_records/',
    method: 'get'
  });
}

export function getSalesStats(salespersonId) {
  return request({
    url: `/orders/sales_stats/?salesperson_id=${salespersonId}`,
    method: 'get'
  });
}

export function getMySales(salespersonId) {
  return request({
    url: `/orders/my_sales/?salesperson_id=${salespersonId}`,
    method: 'get'
  });
}
