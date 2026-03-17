import request from '@/utils/request';

export function getHouses() {
  return request({
    url: '/houses/get_houses/',
    method: 'get'
  });
}

export function createHouse(data) {
  return request({
    url: '/houses/create_house/',
    method: 'post',
    data
  });
}

export function updateHouse(id, data) {
  return request({
    url: `/houses/update_house/${id}/`,
    method: 'post',
    data
  });
}

export function deleteHouse(id) {
  return request({
    url: `/houses/delete_house/${id}/`,
    method: 'post'
  });
}

export function getMyHouses(salespersonId) {
  return request({
    url: `/houses/my_houses/?salesperson_id=${salespersonId}`,
    method: 'get'
  });
}
