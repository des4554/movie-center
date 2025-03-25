<template>
  <a-layout>
    <!-- 头部 -->
    <a-layout-header style="background: #fff; padding: 0 24px;">
      <h1 style="margin: 0;">电影数据中控台</h1>
    </a-layout-header>

    <!-- 内容区 -->
    <a-layout-content style="padding: 24px;">
      <!-- 数据概览 -->
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card>
            <h3>电影总数</h3>
            <p style="font-size: 24px; color: #1890ff;">{{ stats.movieCount }}</p>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <h3>用户总数</h3>
            <p style="font-size: 24px; color: #52c41a;">{{ stats.userCount }}</p>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <h3>平均评分</h3>
            <p style="font-size: 24px; color: #faad14;">{{ stats.averageRating }}</p>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card>
            <h3>Epsilon(该值越小，隐私保护越强)</h3>
            <p style="font-size: 24px; color: #722ed1;">{{ stats.epsilon.toFixed(2) }}</p>
          </a-card>
        </a-col>
      </a-row>

      <!-- 图表区 -->
      <a-row :gutter="16" style="margin-top: 24px;">
        <!-- 评分分布图 -->
        <a-col :span="12">
          <a-card>
            <h3>电影评分分布</h3>
            <div ref="ratingChartRef" style="width: 100%; height: 400px;"></div>
          </a-card>
        </a-col>

        <!-- 电影种类分布图 -->
        <a-col :span="12">
          <a-card>
            <h3>用户喜欢的电影种类分布</h3>
            <div ref="genreChartRef" style="width: 100%; height: 400px;"></div>
          </a-card>
        </a-col>
      </a-row>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios'
// 数据概览
const stats = reactive({
  movieCount: 0,
  userCount: 0,
  averageRating: 0,
  epsilon: 0, // 推荐系统的 epsilon 值
  ratingX: [],
  ratingY: [],
  genreDistribution: [], // 电影种类分布数据
});

// 图表 DOM 引用
const ratingChartRef = ref(null); // 评分分布图
const genreChartRef = ref(null); // 电影种类分布图

// 模拟加载数据
onMounted(() => {
    axios.get(`http://localhost:5000/getSysData`).then((res)=>{
      console.log(res.data)
      stats.movieCount = res.data.stats.movieCount
      stats.userCount = res.data.stats.userCount
      stats.averageRating = res.data.stats.averageRating
      stats.epsilon = res.data.stats.epsilon
      stats.ratingX = res.data.stats.rating_labels
      stats.ratingY = res.data.stats.rating_counts
      stats.genreDistribution = res.data.stats.tags
      renderRatingChart();
      renderGenreChart();
    })

});

// 渲染评分分布图
const renderRatingChart = () => {
  const chart = echarts.init(ratingChartRef.value);
  const option = {
    tooltip: {
      trigger: 'item',
    },
    xAxis: {
      type: 'category',
      data: stats.ratingX,
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        name: '评分分布',
        type: 'bar',
        data: stats.ratingY, // 模拟数据
        itemStyle: {
          color: '#1890ff',
        },
      },
    ],
  };
  chart.setOption(option);
};

// 渲染电影种类分布图
const renderGenreChart = () => {
  const chart = echarts.init(genreChartRef.value);
  const option = {
    tooltip: {
      trigger: 'item',
    },
    legend: {
      bottom: '10%',
      left: 'center',
    },
    series: [
      {
        name: '电影种类分布',
        type: 'pie',
        radius: '50%',
        data: stats.genreDistribution,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };
  chart.setOption(option);
};
</script>

<style scoped>
/* 自定义样式 */
</style>
