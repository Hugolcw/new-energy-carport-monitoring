<template>
  <div class="env-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper env-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
        </svg>
      </div>
      <h3 class="card-title">环境数据</h3>
      <div class="update-time">实时更新</div>
    </div>
    
    <div class="env-data">
      <div class="data-item temperature">
        <div class="data-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M14 14.76V3.5a2.5 2.5 0 00-5 0v11.26a4.5 4.5 0 105 0z"/>
          </svg>
        </div>
        <div class="data-content">
          <div class="data-label">温度</div>
          <div class="data-value">
            <span class="value">{{ temperature.toFixed(1) }}</span>
            <span class="unit">°C</span>
          </div>
        </div>
      </div>
      
      <div class="data-item humidity">
        <div class="data-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"/>
          </svg>
        </div>
        <div class="data-content">
          <div class="data-label">湿度</div>
          <div class="data-value">
            <span class="value">{{ humidity.toFixed(0) }}</span>
            <span class="unit">%</span>
          </div>
        </div>
      </div>
      
      <div class="data-item wind">
        <div class="data-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
          </svg>
        </div>
        <div class="data-content">
          <div class="data-label">风速</div>
          <div class="data-value">
            <span class="value">{{ windSpeed.toFixed(1) }}</span>
            <span class="unit">m/s</span>
          </div>
        </div>
      </div>
    </div>

    <div class="env-chart">
      <div class="chart-title">环境趋势</div>
      <div class="chart-container">
        <div class="chart-line" ref="chartLine"></div>
        <div class="chart-labels">
          <span>温度</span>
          <span>湿度</span>
          <span>风速</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface Props {
  temperature: number
  humidity: number
  windSpeed: number
}

const props = defineProps<Props>()

const chartLine = ref<HTMLElement>()
let animationFrame: number

const createParticle = () => {
  if (!chartLine.value) return
  
  const particle = document.createElement('div')
  particle.className = 'particle'
  particle.style.left = '0px'
  particle.style.top = Math.random() * 100 + 'px'
  particle.style.animationDuration = (Math.random() * 3 + 2) + 's'
  
  chartLine.value.appendChild(particle)
  
  setTimeout(() => {
    if (particle.parentNode) {
      particle.parentNode.removeChild(particle)
    }
  }, 5000)
}

onMounted(() => {
  animationFrame = setInterval(createParticle, 500)
})

onUnmounted(() => {
  clearInterval(animationFrame)
})
</script>

<style scoped>
.env-card {
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
  background: linear-gradient(135deg, #06b6d4, #0891b2);
}

.icon-wrapper svg {
  width: 24px;
  height: 24px;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f8fafc;
  margin: 0;
  flex: 1;
}

.update-time {
  font-size: 0.75rem;
  color: #64748b;
}

.env-data {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.data-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  background: rgba(71, 85, 105, 0.3);
  transition: all 0.3s ease;
}

.data-item:hover {
  background: rgba(71, 85, 105, 0.5);
  transform: translateY(-2px);
}

.data-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
}

.data-icon svg {
  width: 20px;
  height: 20px;
}

.temperature .data-icon {
  color: #ef4444;
}

.humidity .data-icon {
  color: #06b6d4;
}

.wind .data-icon {
  color: #8b5cf6;
}

.data-content {
  flex: 1;
}

.data-label {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 4px;
}

.data-value {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8fafc;
  line-height: 1;
}

.unit {
  font-size: 0.875rem;
  color: #64748b;
}

.env-chart {
  padding-top: 20px;
  border-top: 1px solid #475569;
}

.chart-title {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 12px;
}

.chart-container {
  position: relative;
  height: 80px;
  background: rgba(71, 85, 105, 0.2);
  border-radius: 8px;
  overflow: hidden;
}

.chart-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  width: 2px;
  height: 2px;
  background: #06b6d4;
  border-radius: 50%;
  animation: particleMove 5s linear infinite;
  box-shadow: 0 0 4px #06b6d4;
}

@keyframes particleMove {
  0% {
    left: 0;
    opacity: 1;
  }
  100% {
    left: 100%;
    opacity: 0;
  }
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  margin-top: 8px;
  font-size: 0.75rem;
  color: #64748b;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .env-data {
    gap: 12px;
  }
  
  .data-item {
    padding: 12px;
  }
  
  .value {
    font-size: 1.25rem;
  }
}
</style>