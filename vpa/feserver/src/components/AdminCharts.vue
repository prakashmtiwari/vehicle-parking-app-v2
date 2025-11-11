<script setup>
import { ref, onMounted, nextTick } from "vue"
import { Chart, registerables } from "chart.js"
import reservationService from "@/services/reservationService"
import { useToast } from "vue-toastification";
import annotationPlugin from 'chartjs-plugin-annotation'

const toast = useToast();

Chart.register(...registerables, annotationPlugin)

const reservations = ref([])
const loading = ref(true)
let pieChartInstance = null
let barChartInstance = null

async function loadReservations() {
  loading.value = true
  try {
    const res = await reservationService.getAllReservations()
    
    // FIX: Check if data is in res.data or directly in res
    // Also check if it's an array
    if (Array.isArray(res.data)) {
      reservations.value = res.data
    } else if (Array.isArray(res)) {
      reservations.value = res
    } else {
      reservations.value = []
      console.warn("Unexpected response format:", res)
    }
    
    console.log("Loaded reservations:", reservations.value) // Debug log
    
    if (reservations.value.length > 0) {
      await nextTick()
      // Add a small delay to ensure DOM is fully rendered
      setTimeout(() => {
        renderCharts()
      }, 100)
      // toast.success(`Loaded ${reservations.value.length} reservations`)
    } else {
      toast.info("No reservations found")
    }
  } catch (err) {
    console.error("Error loading reservations:", err)
    toast.error("Failed to load reservations")
    reservations.value = [] // Ensure it's empty on error
  } finally {
    loading.value = false
  }
}

function renderCharts() {
  console.log("renderCharts called") // Debug log
  
  // Group data by lot
  const lotCounts = {}
  const lotAmounts = {}

  reservations.value.forEach(r => {
    const lotName = r.lot_name || "Unknown"
    lotCounts[lotName] = (lotCounts[lotName] || 0) + 1
    lotAmounts[lotName] = (lotAmounts[lotName] || 0) + (Number(r.amount_paid) || 0)
  })

  const labels = Object.keys(lotCounts)
  const counts = Object.values(lotCounts)
  const amounts = Object.values(lotAmounts)

  console.log("Chart data:", { labels, counts, amounts }) // Debug log

  // Destroy old charts if exist
  if (pieChartInstance) {
    pieChartInstance.destroy()
    pieChartInstance = null
  }
  if (barChartInstance) {
    barChartInstance.destroy()
    barChartInstance = null
  }

  // Modern gradient colors
  const gradientColors = [
    '#667eea',
    '#764ba2', 
    '#f093fb',
    '#4facfe',
    '#43e97b',
    '#fa709a',
    '#fee140'
  ]

  // Check if canvas elements exist
  const pieCtx = document.getElementById("pieChart")
  const barCtx = document.getElementById("barChart")
  
  console.log("Canvas elements:", { pieCtx, barCtx }) // Debug log
  
  if (!pieCtx || !barCtx) {
    console.error("Canvas elements not found in DOM")
    return
  }

  // Pie Chart - Reservations per Parking Lot
  pieChartInstance = new Chart(pieCtx, {
    type: "doughnut",
    data: {
      labels,
      datasets: [
        {
          label: "Reservations per Parking Lot",
          data: counts,
          backgroundColor: gradientColors,
          borderWidth: 3,
          borderColor: '#ffffff',
          hoverOffset: 10
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            padding: 15,
            font: {
              family: "'Poppins', sans-serif",
              size: 12
            },
            usePointStyle: true,
            pointStyle: 'circle'
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            family: "'Poppins', sans-serif",
            size: 14
          },
          bodyFont: {
            family: "'Poppins', sans-serif",
            size: 13
          },
          callbacks: {
            label: (context) => {
              const value = context.raw
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${context.label}: ${value} (${percentage}%)`
            }
          }
        }
      }
    }
  })

  // Bar Chart - Amount Paid per Parking Lot
  // Create gradient for bars
  const barContext = barCtx.getContext('2d')
  const gradient = barContext.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, '#667eea')
  gradient.addColorStop(1, '#764ba2')

  barChartInstance = new Chart(barCtx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Amount Paid (₹)",
          data: amounts,
          backgroundColor: gradient,
          borderRadius: 8,
          borderSkipped: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 12,
          titleFont: {
            family: "'Poppins', sans-serif",
            size: 14
          },
          bodyFont: {
            family: "'Poppins', sans-serif",
            size: 13
          },
          callbacks: {
            label: (context) => {
              const value = Number(context.raw) || 0
              return `Revenue: ₹${value.toFixed(2)}`
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.05)',
            drawBorder: false
          },
          ticks: {
            font: {
              family: "'Poppins', sans-serif",
              size: 11
            },
            callback: (value) => `₹${Number(value).toFixed(0)}`
          }
        },
        x: {
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            font: {
              family: "'Poppins', sans-serif",
              size: 11
            }
          }
        }
      }
    }
  })
}

onMounted(loadReservations)
</script>

<template>
  <div class="charts-component">
    <!-- Header Section -->
    <div class="charts-header">
      <h2 class="charts-title">Revenue Analytics</h2>
      <p class="charts-subtitle">Visual breakdown of reservations and revenue by parking lot</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="loading-text">Loading analytics...</p>
    </div>

    <!-- No Reservations Message -->
    <div v-else-if="reservations.length === 0" class="empty-state-card">
      <div class="empty-content">
        <div class="empty-icon">📊</div>
        <p class="empty-text">No reservations found</p>
        <p class="empty-subtext">Analytics will appear here once reservations are made</p>
      </div>
    </div>

    <!-- Charts Grid -->
    <div v-else class="charts-grid">
      <!-- Pie Chart Card -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-icon">🥧</div>
          <div>
            <h3 class="chart-title">Reservations Distribution</h3>
            <p class="chart-subtitle">Number of reservations per parking lot</p>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="pieChart"></canvas>
        </div>
      </div>

      <!-- Bar Chart Card -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-icon">💰</div>
          <div>
            <h3 class="chart-title">Revenue Analysis</h3>
            <p class="chart-subtitle">Total amount collected per parking lot</p>
          </div>
        </div>
        <div class="chart-body">
          <canvas id="barChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Component Container */
.charts-component {
  font-family: 'Poppins', sans-serif;
}

/* Header Section */
.charts-header {
  margin-bottom: 2rem;
}

.charts-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.charts-title::before {
  content: '';
  width: 4px;
  height: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.charts-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  padding-left: 1rem;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
  border-color: #667eea;
  border-right-color: transparent;
}

/* Empty State */
.empty-state-card {
  background: white;
  border-radius: 1rem;
  padding: 4rem 2rem;
  border: 1px solid #e2e8f0;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.empty-text {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

.empty-subtext {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
}

/* Chart Card */
.chart-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chart-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* Chart Header */
.chart-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.chart-icon {
  font-size: 2rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  padding: 0.75rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 3.5rem;
  height: 3.5rem;
}

.chart-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.chart-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
  font-weight: 400;
}

/* Chart Body */
.chart-body {
  position: relative;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-body canvas {
  max-height: 350px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .charts-header {
    margin-bottom: 1.5rem;
  }

  .charts-title {
    font-size: 1.25rem;
  }

  .charts-subtitle {
    font-size: 0.85rem;
  }

  .chart-card {
    padding: 1.5rem;
  }

  .chart-icon {
    font-size: 1.5rem;
    min-width: 3rem;
    height: 3rem;
    padding: 0.5rem;
  }

  .chart-title {
    font-size: 1rem;
  }

  .chart-subtitle {
    font-size: 0.8rem;
  }

  .chart-body {
    min-height: 250px;
  }

  .chart-body canvas {
    max-height: 300px;
  }
}

@media (max-width: 480px) {
  .charts-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .empty-icon {
    font-size: 3rem;
  }

  .empty-text {
    font-size: 1rem;
  }
}
</style>