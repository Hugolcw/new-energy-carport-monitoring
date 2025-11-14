<template>
  <div class="video-card card glow-card">
    <div class="card-header">
      <div class="icon-wrapper video-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke-width="2"/>
          <line x1="8" y1="21" x2="16" y2="21" stroke-width="2"/>
          <line x1="12" y1="17" x2="12" y2="21" stroke-width="2"/>
        </svg>
      </div>
      <h3 class="card-title">实时监控</h3>
      <div class="video-status" :class="{ recording: isRecording }">
        <span class="status-dot"></span>
        {{ isRecording ? '录制中' : '监控中' }}
      </div>
    </div>
    
    <div class="video-container">
      <div class="video-screen" :class="{ active: isActive }">
        <div class="video-placeholder" v-if="!isStreamActive">
          <div class="placeholder-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
          </div>
          <div class="placeholder-text">等待视频流...</div>
        </div>
        
        <div class="video-overlay" v-if="isStreamActive">
          <div class="overlay-info">
            <div class="timestamp">{{ currentTime }}</div>
            <div class="location">车棚监控 #1</div>
          </div>
          <div class="overlay-status">
            <div class="quality-indicator">
              <span class="quality-dot"></span>
              <span class="quality-text">高清</span>
            </div>
          </div>
        </div>
        
        <div class="scan-line" :class="{ active: isActive }"></div>
      </div>
    </div>

    <div class="video-controls">
      <button class="control-btn" @click="toggleStream" :class="{ active: isStreamActive }">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" v-if="!isStreamActive">
          <polygon points="5 3 19 12 5 21 5 3" stroke-width="2"/>
        </svg>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" v-else>
          <rect x="6" y="4" width="4" height="16" stroke-width="2"/>
          <rect x="14" y="4" width="4" height="16" stroke-width="2"/>
        </svg>
        {{ isStreamActive ? '暂停' : '播放' }}
      </button>
      
      <button class="control-btn" @click="toggleRecord" :class="{ active: isRecording }">
        <div class="record-icon" :class="{ recording: isRecording }"></div>
        {{ isRecording ? '停止录制' : '开始录制' }}
      </button>
      
      <button class="control-btn" @click="takeSnapshot">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="3" stroke-width="2"/>
          <circle cx="12" cy="12" r="8" stroke-width="2"/>
        </svg>
        截图
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  streamUrl: string
}

const props = defineProps<Props>()

const isStreamActive = ref(false)
const isRecording = ref(false)
const isActive = ref(true)

const currentTime = computed(() => {
  return new Date().toLocaleTimeString('zh-CN')
})

const toggleStream = () => {
  isStreamActive.value = !isStreamActive.value
  console.log('视频流:', isStreamActive.value ? '开启' : '关闭')
}

const toggleRecord = () => {
  isRecording.value = !isRecording.value
  console.log('录制状态:', isRecording.value ? '开始录制' : '停止录制')
}

const takeSnapshot = () => {
  console.log('截图功能触发')
  // 这里可以实现实际的截图功能
}
</script>

<style scoped>
.video-card {
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
  background: linear-gradient(135deg, #ef4444, #dc2626);
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

.video-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 500;
  background: rgba(71, 85, 105, 0.3);
  color: #64748b;
}

.video-status.recording {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  animation: pulse 2s infinite;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.video-container {
  margin-bottom: 20px;
}

.video-screen {
  position: relative;
  width: 100%;
  height: 240px;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  border-radius: 12px;
  border: 2px solid #475569;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-screen.active {
  border-color: #06b6d4;
  box-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
}

.video-placeholder {
  text-align: center;
  color: #64748b;
}

.placeholder-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 12px;
  opacity: 0.6;
}

.placeholder-icon svg {
  width: 100%;
  height: 100%;
}

.placeholder-text {
  font-size: 0.875rem;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px;
  background: linear-gradient(135deg, rgba(0,0,0,0.3), transparent);
}

.overlay-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.timestamp {
  font-size: 0.75rem;
  color: #e2e8f0;
  font-weight: 500;
}

.location {
  font-size: 0.75rem;
  color: #94a3b8;
}

.overlay-status {
  display: flex;
  align-items: center;
}

.quality-indicator {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 12px;
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  font-size: 0.75rem;
  font-weight: 500;
}

.quality-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.scan-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #06b6d4, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.scan-line.active {
  opacity: 1;
  animation: scan 3s linear infinite;
}

@keyframes scan {
  0% {
    top: 0;
  }
  100% {
    top: 100%;
  }
}

.video-controls {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.control-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: 2px solid #475569;
  background: var(--bg-secondary);
  color: #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover {
  border-color: #06b6d4;
  color: #06b6d4;
}

.control-btn.active {
  background: #06b6d4;
  border-color: #06b6d4;
  color: white;
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
}

.control-btn svg {
  width: 16px;
  height: 16px;
}

.record-icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #64748b;
  transition: all 0.3s ease;
}

.record-icon.recording {
  background: #ef4444;
  animation: recordPulse 1s infinite;
}

@keyframes recordPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .video-screen {
    height: 200px;
  }
  
  .video-controls {
    flex-direction: column;
  }
  
  .control-btn {
    justify-content: center;
  }
}
</style>