<template>
  <div class="flex flex-col  items-center gap-2">
    <button
      :disabled="exporting"
      class="px-4 py-2 rounded-lg custom-outline text-black"
      :class="exporting ? 'bg-gray-400' : 'bg-blue-600 hover:bg-blue-700'"
      @click="triggerExport"
    >
      {{ exporting ? 'Exporting...' : 'Export My Parking History' }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()
const exporting = ref(false)
const API_URL = import.meta.env.VITE_API_URL || ''

const triggerExport = async () => {
  exporting.value = true
  toast.info('🚀 Starting export...')

  try {
    // 1️⃣ Trigger export job
    const res = await fetch(`${API_URL}/api/export-history`, { method: 'POST' })
    const data = await res.json()
    const jobId = data.job_id

    // 2️⃣ Poll every 3 seconds for job status
    const interval = setInterval(async () => {
      const statusRes = await fetch(`/api/export-status/${jobId}`)
      const statusData = await statusRes.json()

      if (statusData.status === 'SUCCESS') {
        clearInterval(interval)
        exporting.value = false
        const url = statusData.result.download_url

        toast.success(`✅ Export complete!`, {
          timeout: 8000,
          closeOnClick: false,
          onClick: () => window.open(url, '_blank')
        })
      } else if (statusData.status === 'FAILURE') {
        clearInterval(interval)
        exporting.value = false
        toast.error('❌ Export failed. Please try again.')
      }
    }, 3000)
  } catch (err) {
    console.error(err)
    exporting.value = false
    toast.error('⚠️ Something went wrong starting the export.')
  }
}
</script>

<style scoped>
button {
  transition: all 0.3s ease;
}

.custom-text {
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 1px solid rgb(218, 47, 218); 
  margin-bottom: 20px;
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}
</style>
