<template>
  <div class="power-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper wind-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
        </svg>
      </div>
      <h3 class="card-title">风力发电</h3>
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
        <span>5 kW</span>
      </div>
    </div>

    <div class="wind-indicator">
      <div class="wind-icon-animated" :class="{ spinning: status }">
        <svg viewBox="0 0 100 100" fill="none" stroke="currentColor">
          <circle cx="50" cy="50" r="8" stroke-width="3"/>
          <path d="M50 42 L50 15" stroke-width="3"/>
          <path d="M50 58 L50 85" stroke-width="3"/>
          <path d="M42 50 L15 50" stroke-width="3"/>
          <path d="M58 50 L85 50" stroke-width="3"/>
        </svg>
      </div>
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
  return Math.min(100, (power / 5) * 100)
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
  color: #06b6d4;
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
  background: linear-gradient(90deg, #06b6d4, #0891b2);
  border-radius: 4px;
  transition: width 0.5s ease;
  box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
}

.power-range {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #64748b;
}

.wind-indicator {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.wind-icon-animated {
  width: 60px;
  height: 60px;
  color: #06b6d4;
  opacity: 0.8;
}

.wind-icon-animated.spinning {
  animation: rotate 3s linear infinite;
}

.wind-icon-animated svg {
  width: 100%;
  height: 100%;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .value {
    font-size: 2rem;
  }
  
  .wind-icon-animated {
    width: 48px;
    height: 48px;
  }
}
</style>