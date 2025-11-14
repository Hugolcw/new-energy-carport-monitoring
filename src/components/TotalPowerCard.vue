<template>
  <div class="total-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper total-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M13 10V3L4 14h7v7l9-11h-7z"/>
        </svg>
      </div>
      <h3 class="card-title">功率统计</h3>
      <div class="efficiency-badge">
        {{ efficiency }}%
      </div>
    </div>
    
    <div class="power-stats">
      <div class="stat-item total">
        <div class="stat-label">总发电量</div>
        <div class="stat-value">
          <span class="value">{{ power.toFixed(1) }}</span>
          <span class="unit">kW</span>
        </div>
        <div class="stat-bar">
          <div class="bar-fill" :style="{ width: `${getPercentage(power, 10)}%` }"></div>
        </div>
      </div>
      
      <div class="stat-item output">
        <div class="stat-label">输出功率</div>
        <div class="stat-value">
          <span class="value">{{ output.toFixed(1) }}</span>
          <span class="unit">kW</span>
        </div>
        <div class="stat-bar">
          <div class="bar-fill" :style="{ width: `${getPercentage(output, 10)}%` }"></div>
        </div>
      </div>
    </div>

    <div class="power-circle">
      <div class="circle-container">
        <svg class="circle-svg" viewBox="0 0 100 100">
          <circle class="circle-bg" cx="50" cy="50" r="45"/>
          <circle class="circle-progress" cx="50" cy="50" r="45" 
                  :stroke-dasharray="circleCircumference" 
                  :stroke-dashoffset="circleOffset"/>
        </svg>
        <div class="circle-content">
          <div class="circle-label">效率</div>
          <div class="circle-value">{{ efficiency }}%</div>
        </div>
      </div>
    </div>

    <div class="power-breakdown">
      <div class="breakdown-item">
        <div class="breakdown-label">风力发电</div>
        <div class="breakdown-bar">
          <div class="bar-fill wind" :style="{ width: `${windPercentage}%` }"></div>
        </div>
        <div class="breakdown-value">{{ windPower.toFixed(1) }}kW</div>
      </div>
      
      <div class="breakdown-item">
        <div class="breakdown-label">太阳能发电</div>
        <div class="breakdown-bar">
          <div class="bar-fill solar" :style="{ width: `${solarPercentage}%` }"></div>
        </div>
        <div class="breakdown-value">{{ solarPower.toFixed(1) }}kW</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  power: number
  output: number
}

const props = defineProps<Props>()

const efficiency = computed(() => {
  if (props.power === 0) return 0
  return Math.min(100, Math.round((props.output / props.power) * 100))
})

const windPower = computed(() => props.power * 0.4) // 模拟风力发电占比
const solarPower = computed(() => props.power * 0.6) // 模拟太阳能发电占比

const windPercentage = computed(() => (windPower.value / props.power) * 100)
const solarPercentage = computed(() => (solarPower.value / props.power) * 100)

const getPercentage = (value: number, max: number): number => {
  return Math.min(100, (value / max) * 100)
}

const circleCircumference = 2 * Math.PI * 45
const circleOffset = computed(() => {
  const progress = efficiency.value / 100
  return circleCircumference * (1 - progress)
})
</script>

<style scoped>
.total-card {
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

.efficiency-badge {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.power-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 8px;
}

.stat-value {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 4px;
  margin-bottom: 12px;
}

.stat-value .value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8fafc;
  line-height: 1;
}

.stat-value .unit {
  font-size: 0.875rem;
  color: #64748b;
}

.stat-bar {
  height: 6px;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.stat-bar .bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.total .bar-fill {
  background: linear-gradient(90deg, #8b5cf6, #7c3aed);
  box-shadow: 0 0 8px rgba(139, 92, 246, 0.5);
}

.output .bar-fill {
  background: linear-gradient(90deg, #06b6d4, #0891b2);
  box-shadow: 0 0 8px rgba(6, 182, 212, 0.5);
}

.power-circle {
  display: flex;
  justify-content: center;
  margin: 24px 0;
}

.circle-container {
  position: relative;
  width: 120px;
  height: 120px;
}

.circle-svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.circle-bg {
  fill: none;
  stroke: rgba(71, 85, 105, 0.3);
  stroke-width: 6;
}

.circle-progress {
  fill: none;
  stroke: url(#gradient);
  stroke-width: 6;
  stroke-linecap: round;
  transition: stroke-dashoffset 0.5s ease;
}

.circle-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.circle-label {
  font-size: 0.875rem;
  color: #94a3b8;
  margin-bottom: 4px;
}

.circle-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #f8fafc;
}

.power-breakdown {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #475569;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.breakdown-label {
  font-size: 0.875rem;
  color: #94a3b8;
  min-width: 80px;
}

.breakdown-bar {
  flex: 1;
  height: 6px;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.breakdown-bar .bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.breakdown-bar .bar-fill.wind {
  background: linear-gradient(90deg, #06b6d4, #0891b2);
}

.breakdown-bar .bar-fill.solar {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.breakdown-value {
  font-size: 0.875rem;
  color: #f8fafc;
  font-weight: 600;
  min-width: 60px;
  text-align: right;
}

/* 添加渐变定义 */
.total-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:%238b5cf6"/><stop offset="100%" style="stop-color:%237c3aed"/></linearGradient></defs></svg>');
  pointer-events: none;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .power-stats {
    flex-direction: column;
    gap: 16px;
  }
  
  .circle-container {
    width: 100px;
    height: 100px;
  }
  
  .circle-value {
    font-size: 1.1rem;
  }
}
</style>