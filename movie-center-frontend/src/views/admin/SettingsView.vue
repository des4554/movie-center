<template>
  <a-layout>
    <!-- 头部 -->
    <a-layout-header style="
    background: linear-gradient(90deg, #1890ff, #096dd9);
    padding: 0;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    height: 64px; /* 固定高度确保与Ant Design布局一致 */
    display: flex;
    align-items: center; /* 垂直居中 */
    justify-content: center; /* 水平居中 */
">
      <h1 style="
        margin: 0;
        font-size: 24px;
        color: #fff;
        font-weight: 500;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
        transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
        cursor: default;
        line-height: 1; /* 确保文字自身行高正常 */
        transform-origin: center; /* 缩放中心点 */
    "
          class="header-title"> <!-- 改为class方式更规范 -->
        电影数据中控台
      </h1>
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
            <h3>Epsilon隐私保护参数</h3>
            <p style="font-size: 24px; color: #722ed1;">{{ stats.epsilon.toFixed(2) }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <span class="edit-link" @click="openModal">修改</span></p>
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
  <!-- 修改Epsilon的模态框 -->
  <!-- 模态框 -->
  <a-modal
    v-model:visible="modalVisible"
    title="修改Epsilon值"
    :confirm-loading="confirmLoading"
    ok-text="保存"
    cancel-text="取消"
    @ok="submitEpsilon"
  >
    <a-form layout="vertical">
      <a-form-item label="新Epsilon值" required>
        <a-input-number
          v-model:value="tempEpsilon"
          :min="0.01"
          :max="10"
          :step="0.01"
          :precision="2"
          style="width: 100%"
        />
      </a-form-item>
      <a-alert
        type="info"
        message="隐私保护强度与数据可用性的权衡"
        description="较小的ε值提供更强的隐私保护，但会降低数据可用性。推荐范围：0.1 ~ 1.0"
        show-icon
      />
    </a-form>
  </a-modal>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import * as echarts from 'echarts';
import axios from 'axios'
import { message } from 'ant-design-vue'
import { changeEpsilon } from '@/api/settins.ts'
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

// 状态管理
const modalVisible = ref(false);
const confirmLoading = ref(false);
const tempEpsilon = ref(stats.epsilon);

// 打开模态框
const openModal = () => {
  tempEpsilon.value = stats.epsilon;
  modalVisible.value = true;
};

// 提交修改
const submitEpsilon = async () => {
  try {
    confirmLoading.value = true;

    // 验证逻辑
    if (tempEpsilon.value <= 0) {
      throw new Error('值必须大于0');
    }

    // 模拟API请求（实际项目中替换为真实请求）
    changeEpsilon(tempEpsilon.value).then(res=>{
      if (res.data.success) {
        // 更新数据（通过emit或直接修改props，根据项目规范选择）
        message.success('参数更新成功');
        modalVisible.value = false;
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
      }
    })

  } catch (error) {
    message.error(error instanceof Error ? error.message : '修改失败');
  } finally {
    confirmLoading.value = false;
  }
};


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
.header-title:hover {
  transform: scale(1.05);
}
.edit-link {
  color: #2575fc;
  cursor: pointer;
  font-size: 15px;
  margin-left: 12px;
  transition: color 0.3s;
}

.edit-link:hover {
  color: #1890ff;
  text-decoration: underline;
}
</style>
