<template>
  <div class="dashboard">
    <!-- 页面头部 -->
    <header class="dashboard-header">
      <h1 class="title">
        <span class="text-gradient">风光互补充电车棚监控系统</span>
      </h1>
      <div class="header-info">
        <div class="time-display">{{ currentTime }}</div>
        <div class="status-indicator" :class="{ online: systemOnline }">
          <span class="status-dot"></span>
          {{ systemOnline ? '系统在线' : '系统离线' }}
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="dashboard-main">
      <!-- 顶部状态卡片 -->
      <div class="status-cards">
        <WindPowerCard :power="windPower" :status="windStatus" />
        <SolarPowerCard :power="solarPower" :status="solarStatus" />
        <BatteryCard :level="batteryLevel" :voltage="batteryVoltage" />
        <TotalPowerCard :power="totalPower" :output="outputPower" />
      </div>

      <!-- 中间监控区域 -->
      <div class="monitor-section">
        <!-- 环境数据 -->
        <div class="environment-panel">
          <EnvironmentCard 
            :temperature="temperature" 
            :humidity="humidity"
            :windSpeed="windSpeed"
          />
        </div>

        <!-- 视频监控 -->
        <div class="video-panel">
          <VideoMonitor :streamUrl="videoStreamUrl" />
        </div>
      </div>

      <!-- 控制面板 -->
      <div class="control-panel">
        <ControlCard 
          :windControl="windControl"
          :mainPower="mainPower"
          @toggle-wind="toggleWind"
          @toggle-power="togglePower"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import WindPowerCard from '@/components/WindPowerCard.vue'
import SolarPowerCard from '@/components/SolarPowerCard.vue'
import BatteryCard from '@/components/BatteryCard.vue'
import TotalPowerCard from '@/components/TotalPowerCard.vue'
import EnvironmentCard from '@/components/EnvironmentCard.vue'
import VideoMonitor from '@/components/VideoMonitor.vue'
import ControlCard from '@/components/ControlCard.vue'

// 实时数据
const windPower = ref(2.4) // kW
const solarPower = ref(3.8) // kW
const batteryLevel = ref(78) // %
const batteryVoltage = ref(48.2) // V
const totalPower = ref(6.2) // kW
const outputPower = ref(4.1) // kW
const temperature = ref(23.5) // °C
const humidity = ref(65) // %
const windSpeed = ref(5.2) // m/s
const windStatus = ref(true)
const solarStatus = ref(true)
const windControl = ref(true)
const mainPower = ref(true)
const systemOnline = ref(true)
const videoStreamUrl = ref('http://localhost:5000/video_feed')

// 时间显示
const currentTime = ref('')
let timeInterval: number

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 模拟实时数据更新
let dataInterval: number

const updateData = () => {
  // 风力功率波动
  windPower.value = Math.max(0, windPower.value + (Math.random() - 0.5) * 0.3)
  
  // 太阳能功率波动（考虑时间因素）
  const hour = new Date().getHours()
  const solarMultiplier = hour >= 6 && hour <= 18 ? 1 : 0.1
  solarPower.value = Math.max(0, solarPower.value + (Math.random() - 0.5) * 0.4 * solarMultiplier)
  
  // 电池电量变化
  const netPower = windPower.value + solarPower.value - outputPower.value
  if (netPower > 0) {
    batteryLevel.value = Math.min(100, batteryLevel.value + netPower * 0.1)
  } else {
    batteryLevel.value = Math.max(0, batteryLevel.value + netPower * 0.15)
  }
  
  // 总功率计算
  totalPower.value = windPower.value + solarPower.value
  
  // 输出功率波动
  outputPower.value = Math.max(0, outputPower.value + (Math.random() - 0.5) * 0.5)
  
  // 环境数据波动
  temperature.value += (Math.random() - 0.5) * 0.5
  humidity.value = Math.max(0, Math.min(100, humidity.value + (Math.random() - 0.5) * 2))
  windSpeed.value = Math.max(0, windSpeed.value + (Math.random() - 0.5) * 0.8)
}

// 控制功能
const toggleWind = () => {
  windControl.value = !windControl.value
  windStatus.value = windControl.value
  console.log('风机控制:', windControl.value ? '启动' : '停止')
}

const togglePower = () => {
  mainPower.value = !mainPower.value
  if (!mainPower.value) {
    windControl.value = false
    windStatus.value = false
    solarStatus.value = false
  }
  console.log('总电源:', mainPower.value ? '开启' : '关闭')
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  dataInterval = setInterval(updateData, 2000)
})

onUnmounted(() => {
  clearInterval(timeInterval)
  clearInterval(dataInterval)
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 1px solid #475569;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 24px;
}

.time-display {
  font-size: 1.1rem;
  color: #94a3b8;
  font-weight: 500;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  font-weight: 600;
}

.status-indicator.online {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.dashboard-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.status-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.monitor-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-top: 20px;
}

.environment-panel,
.video-panel {
  min-height: 400px;
}

.control-panel {
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .monitor-section {
    grid-template-columns: 1fr;
  }
  
  .status-cards {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .status-cards {
    grid-template-columns: 1fr;
  }
}
</style>