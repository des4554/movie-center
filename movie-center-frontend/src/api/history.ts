import request from '@/utils/request' // 假设你使用 axios 封装

// 获取浏览历史
export const getBrowseHistory = (userid) => {
  return request({
    url: `/browse/history/${userid}`,
    method: 'get',
  })
}

// 增加删除历史
export const addBrowseHistory = (params) => {
  return request({
    url: '/addBrowse',
    method: 'POST',
    data: params
  })
}

// 删除单条记录
export const deleteBrowseRecord = (browseId) => {
  return request({
    url: `/browse/history/${browseId}`,
    method: 'delete'
  })
}

export const getRecommendHistory = (userid) => {
  return request({
    url: `/recommend/history/${userid}`,
    method: 'get',
  })
}

// 增加删除历史
export const addRecommendHistory = (params) => {
  return request({
    url: '/recommend/history',
    method: 'POST',
    data: params
  })
}

export function add8HoursToISOTime() {
  const date = new Date();
  // 解析出原始的小时部分
  let hours = date.getUTCHours() + 8; // 增加8小时
  if (hours >= 24) { // 如果小时数超过24小时，则需要调整日期
    hours -= 24;
    date.setDate(date.getDate() + 1); // 增加一天
  }
  // 使用setUTCHours确保我们只修改小时部分，并保持其他部分不变
  date.setUTCHours(hours, date.getUTCMinutes(), date.getUTCSeconds(), date.getUTCMilliseconds());
  // 返回更新后的ISO格式字符串
  return date.toISOString();
}
