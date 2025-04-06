import request from '@/utils/request'

export const changeEpsilon = (epsilon: number) => {
  return request({
    url: '/epsilon/' + epsilon
  })
}
