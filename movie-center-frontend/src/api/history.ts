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
