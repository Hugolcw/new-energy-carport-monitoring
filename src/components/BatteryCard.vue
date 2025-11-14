<template>
  <div class="battery-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper battery-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <rect x="1" y="6" width="18" height="12" rx="2" ry="2" stroke-width="2"/>
          <line x1="23" y1="11" x2="23" y2="13" stroke-width="2"/>
          <rect x="3" y="9" width="6" height="6" rx="1" ry="1" fill="currentColor"/>
        </svg>
      </div>
      <h3 class="card-title">电池状态</h3>
      <div class="battery-percentage">{{ level }}%</div>
    </div>
    
    <div class="battery-display">
      <div class="battery-container">
        <div class="battery-body">
          <div class="battery-level" :style="{ height: `${level}%`, background: getBatteryColor(level) }">
            <div class="battery-fill-animation"></div>
          </div>
        </div>
        <div class="battery-terminal"></div>
      </div>
      
      <div class="battery-info">
        <div class="info-item">
          <span class="label">电量</span>
          <span class="value">{{ level }}%</span>
        </div>
        <div class="info-item">
          <span class="label">电压</span>
          <span class="value">{{ voltage.toFixed(1) }}V</span>
        </div>
        <div class="info-item">
          <span class="label">状态</span>
          <span class="value" :class="getBatteryStatus(level)">{{ getBatteryStatusText(level) }}</span>
        </div>
      </div>
    </div>

    <div class="battery-chart">
      <div class="chart-title">电量趋势</div>
      <div class="chart-bars">
        <div class="bar" v-for="(value, index) in batteryHistory" :key="index" 
             :style="{ height: `${value}%`, background: getBatteryColor(value) }">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  level: number
  voltage: number
}

const props = defineProps<Props>()

const batteryHistory = ref<number[]>([])
let historyInterval: number

const getBatteryColor = (level: number): string => {
  if (level > 80) return 'linear-gradient(180deg, #10b981, #059669)'
  if (level > 50) return 'linear-gradient(180deg, #f59e0b, #d97706)'
  if (level > 20) return 'linear-gradient(180deg, #f97316, #ea580c)'
  return 'linear-gradient(180deg, #ef4444, #dc2626)'
}

const getBatteryStatus = (level: number): string => {
  if (level > 80) return 'status-good'
  if (level > 50) return 'status-normal'
  if (level > 20) return 'status-warning'
  return 'status-danger'
}

const getBatteryStatusText = (level: number): string => {
  if (level > 80) return '充足'
  if (level > 50) return '良好'
  if (level > 20) return '一般'
  return '不足'
}

const updateBatteryHistory = () => {
  batteryHistory.value.push(props.level)
  if (batteryHistory.value.length > 12) {
    batteryHistory.value.shift()
  }
}

onMounted(() => {
  // 初始化历史数据
  for (let i = 0; i < 12; i++) {
    batteryHistory.value.push(Math.max(0, props.level - (12 - i) * 2))
  }
  
  historyInterval = setInterval(updateBatteryHistory, 5000)
})

onUnmounted(() => {
  clearInterval(historyInterval)
})
</script>

<style scoped>
.battery-card {
  position: relative;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.icon-wrapper svg {
  width: 24px;
  height: 24px;
  color: white;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f8fafc;
  margin: 0;
  flex: 1;
}

.battery-percentage {
  font-size: 1.5rem;
  font-weight: 700;
  color: #8b5cf6;
}

.battery-display {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 20px;
}

.battery-container {
  position: relative;
  display: flex;
  align-items: center;
}

.battery-body {
  width: 60px;
  height: 100px;
  border: 3px solid #475569;
  border-radius: 8px;
  position: relative;
  background: rgba(71, 85, 105, 0.2);
  overflow: hidden;
}

.battery-level {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-radius: 4px;
  transition: all 0.5s ease;
  overflow: hidden;
}

.battery-fill-animation {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, 
    rgba(255,255,255,0.3) 0%, 
    transparent 50%, 
    rgba(255,255,255,0.1) 100%);
  animation: fillWave 2s ease-in-out infinite;
}

@keyframes fillWave {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.battery-terminal {
  width: 20px;
  height: 8px;
  background: #475569;
  border-radius: 2px 2px 0 0;
  margin-left: -2px;
}

.battery-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #94a3b8;
  font-size: 0.875rem;
}

.value {
  font-weight: 600;
  color: #f8fafc;
}

.status-good { color: #10b981; }
.status-normal { color: #f59e0b; }
.status-warning { color: #f97316; }
.status-danger { color: #ef4444; }

.battery-chart {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #475569;
}

.chart-title {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 12px;
}

.chart-bars {
  display: flex;
  align-items: end;
  gap: 4px;
  height: 60px;
}

.bar {
  flex: 1;
  border-radius: 2px 2px 0 0;
  transition: all 0.3s ease;
  min-height: 2px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .battery-display {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .battery-info {
    width: 100%;
  }
  
  .battery-percentage {
    font-size: 1.25rem;
  }
}
</style>