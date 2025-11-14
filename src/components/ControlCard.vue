<template>
  <div class="control-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper control-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="3" stroke-width="2"/>
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M12 1v6m0 6v6m11-7h-6m-6 0H1"/>
        </svg>
      </div>
      <h3 class="card-title">系统控制</h3>
      <div class="control-status">
        <span class="status-indicator" :class="{ active: mainPower }">
          {{ mainPower ? '系统开启' : '系统关闭' }}
        </span>
      </div>
    </div>
    
    <div class="control-grid">
      <div class="control-section">
        <h4 class="section-title">主电源控制</h4>
        <div class="power-switch">
          <button 
            class="switch-btn main-power" 
            :class="{ active: mainPower }"
            @click="$emit('toggle-power')"
          >
            <div class="switch-indicator">
              <div class="switch-light" :class="{ on: mainPower }"></div>
            </div>
            <span class="switch-label">{{ mainPower ? '关闭电源' : '开启电源' }}</span>
          </button>
        </div>
      </div>

      <div class="control-section">
        <h4 class="section-title">风力发电控制</h4>
        <div class="wind-control">
          <button 
            class="switch-btn wind-control" 
            :class="{ active: windControl, disabled: !mainPower }"
            @click="mainPower && $emit('toggle-wind')"
            :disabled="!mainPower"
          >
            <div class="wind-icon-small" :class="{ spinning: windControl && mainPower }">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9.59 4.59A2 2 0 1111 8H2m10.59 11.41A2 2 0 1014 16H2m15.73-8.27A2.5 2.5 0 1119.5 12H2"/>
              </svg>
            </div>
            <span class="switch-label">{{ windControl ? '停止风机' : '启动风机' }}</span>
          </button>
        </div>
      </div>

      <div class="control-section">
        <h4 class="section-title">紧急控制</h4>
        <div class="emergency-controls">
          <button class="emergency-btn stop-all" @click="emergencyStop">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <rect x="9" y="9" width="6" height="6" stroke-width="2"/>
            </svg>
            紧急停止
          </button>
          
          <button class="emergency-btn reset" @click="systemReset">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            系统重置
          </button>
        </div>
      </div>
    </div>

    <div class="system-info">
      <div class="info-grid">
        <div class="info-item">
          <span class="info-label">运行时间</span>
          <span class="info-value">{{ runtime }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">今日发电</span>
          <span class="info-value">{{ dailyGeneration }} kWh</span>
        </div>
        <div class="info-item">
          <span class="info-label">系统状态</span>
          <span class="info-value" :class="systemStatusClass">{{ systemStatus }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  windControl: boolean
  mainPower: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'toggle-wind': []
  'toggle-power': []
}>()

const runtime = ref('24h 35m')
const dailyGeneration = ref(156.8)

const systemStatus = computed(() => {
  if (!props.mainPower) return '已关闭'
  if (props.windControl) return '正常运行'
  return '待机中'
})

const systemStatusClass = computed(() => {
  if (!props.mainPower) return 'status-offline'
  if (props.windControl) return 'status-online'
  return 'status-standby'
})

const emergencyStop = () => {
  console.log('紧急停止系统')
  emit('toggle-power')
}

const systemReset = () => {
  console.log('系统重置')
  if (!props.mainPower) {
    emit('toggle-power')
  }
}
</script>

<style scoped>
.control-card {
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

.control-status {
  display: flex;
  align-items: center;
}

.status-indicator {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.status-indicator.active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.control-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.control-section {
  background: rgba(71, 85, 105, 0.2);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #475569;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #f8fafc;
  margin-bottom: 16px;
}

.switch-btn {
  width: 100%;
  padding: 16px;
  border: 2px solid #475569;
  background: var(--bg-secondary);
  color: #e2e8f0;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.switch-btn:hover:not(.disabled) {
  border-color: #06b6d4;
  transform: translateY(-2px);
}

.switch-btn.active {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  border-color: #06b6d4;
  color: white;
  box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
}

.switch-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.switch-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
}

.switch-light {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
}

.switch-light.on {
  background: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.6);
}

.wind-icon-small {
  width: 20px;
  height: 20px;
  color: currentColor;
}

.wind-icon-small.spinning {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.emergency-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.emergency-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 2px solid;
  background: var(--bg-secondary);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.emergency-btn.stop-all {
  border-color: #ef4444;
  color: #ef4444;
}

.emergency-btn.stop-all:hover {
  background: rgba(239, 68, 68, 0.1);
  transform: translateY(-1px);
}

.emergency-btn.reset {
  border-color: #f59e0b;
  color: #f59e0b;
}

.emergency-btn.reset:hover {
  background: rgba(245, 158, 11, 0.1);
  transform: translateY(-1px);
}

.emergency-btn svg {
  width: 16px;
  height: 16px;
}

.system-info {
  padding-top: 20px;
  border-top: 1px solid #475569;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: rgba(71, 85, 105, 0.2);
  border-radius: 8px;
}

.info-label {
  font-size: 0.75rem;
  color: #94a3b8;
}

.info-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f8fafc;
}

.status-online { color: #10b981; }
.status-standby { color: #f59e0b; }
.status-offline { color: #ef4444; }

/* 响应式调整 */
@media (max-width: 768px) {
  .control-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>