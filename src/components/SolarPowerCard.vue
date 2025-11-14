<template>
  <div class="power-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper solar-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="5" stroke-width="2"/>
          <line x1="12" y1="1" x2="12" y2="3" stroke-width="2"/>
          <line x1="12" y1="21" x2="12" y2="23" stroke-width="2"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke-width="2"/>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke-width="2"/>
          <line x1="1" y1="12" x2="3" y2="12" stroke-width="2"/>
          <line x1="21" y1="12" x2="23" y2="12" stroke-width="2"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke-width="2"/>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke-width="2"/>
        </svg>
      </div>
      <h3 class="card-title">太阳能发电</h3>
      <div class="status-badge" :class="{ active: status }">
        {{ status ? '运行中' : '已停止' }}
      </div>
    </div>
    
    <div class="power-display">
      <div class="power-value">
        <span class="value">{{ power.toFixed(1) }}</span>
        <span class="unit">kW</span>
      </div>
      <div class="power-bar">
        <div class="bar-fill" :style="{ width: `${getPowerPercentage(power)}%` }"></div>
      </div>
      <div class="power-range">
        <span>0 kW</span>
        <span>8 kW</span>
      </div>
    </div>

    <div class="solar-indicator">
      <div class="sun-rays" :class="{ active: status }">
        <div class="ray" v-for="i in 8" :key="i" :style="{ transform: `rotate(${i * 45}deg)` }"></div>
      </div>
      <div class="sun-core"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  power: number
  status: boolean
}

defineProps<Props>()

const getPowerPercentage = (power: number): number => {
  return Math.min(100, (power / 8) * 100)
}
</script>

<style scoped>
.power-card {
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
  background: linear-gradient(135deg, #f59e0b, #d97706);
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

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.power-display {
  margin-bottom: 20px;
}

.power-value {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 16px;
}

.value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #f59e0b;
  line-height: 1;
}

.unit {
  font-size: 1rem;
  color: #94a3b8;
  font-weight: 500;
}

.power-bar {
  height: 8px;
  background: rgba(71, 85, 105, 0.3);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #f59e0b, #d97706);
  border-radius: 4px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
}

.power-range {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #64748b;
}

.solar-indicator {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  position: relative;
  height: 80px;
}

.sun-rays {
  position: absolute;
  width: 80px;
  height: 80px;
  animation: rotate 8s linear infinite;
}

.sun-rays.active {
  animation-duration: 4s;
}

.ray {
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 12px;
  background: linear-gradient(to bottom, #f59e0b, transparent);
  transform-origin: 50% 40px;
  border-radius: 1px;
  opacity: 0.7;
}

.sun-core {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: radial-gradient(circle, #f59e0b, #d97706);
  box-shadow: 0 0 20px rgba(245, 158, 11, 0.6);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .value {
    font-size: 2rem;
  }
  
  .solar-indicator {
    height: 60px;
  }
  
  .sun-rays {
    width: 60px;
    height: 60px;
  }
  
  .sun-core {
    width: 30px;
    height: 30px;
  }
}
</style>