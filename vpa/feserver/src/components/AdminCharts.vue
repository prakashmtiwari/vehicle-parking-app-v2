<script setup>
import { ref, onMounted, nextTick } from "vue"
import { Chart, registerables } from "chart.js"
import reservationService from "@/services/reservationService"
import { useToast } from "vue-toastification";
import annotationPlugin from 'chartjs-plugin-annotation'

const toast = useToast();

Chart.register(...registerables, annotationPlugin)


const reservations = ref([])
let pieChartInstance = null
let barChartInstance = null

async function loadReservations() {
  try {
    const res = await reservationService.getAllReservations()
    reservations.value = res.data
    await nextTick()
    renderCharts()
  } catch (err) {
    console.error("Error loading reservations:", err)
    toast.error("Error loading reservations")
  }
}

function renderCharts() {
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

  // Destroy old charts if exist
  if (pieChartInstance) pieChartInstance.destroy()
  if (barChartInstance) barChartInstance.destroy()

  // Pie Chart - Reservations per Parking Lot
  const pieCtx = document.getElementById("pieChart")
  pieChartInstance = new Chart(pieCtx, {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Reservations per Parking Lot",
          data: counts,
          backgroundColor: ["#0d6efd", "#198754", "#ffc107", "#dc3545", "#6f42c1"]
        }
      ]
    },
    options: {
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const value = context.raw
              return `${context.label}: ${value} reservations`
            }
          }
        }
      }
    }
  })

  // Bar Chart - Amount Paid per Parking Lot
  const barCtx = document.getElementById("barChart")
  barChartInstance = new Chart(barCtx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Amount Paid per Parking Lot",
          data: amounts,
          backgroundColor: "#0d6efd"
        }
      ]
    },
    options: {
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const value = Number(context.raw) || 0
              return `₹${value.toFixed(2)}`
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (value) => `₹${Number(value).toFixed(0)}`
          }
        }
      }
    }
  })
}

onMounted(loadReservations)
</script>

<template>
 <div class="container my-5">
  <h2 class="text-center custom-text mb-4">Admin Reservation Summary</h2>

  <!-- No Reservations Message -->
  <div v-if="reservations.length === 0" class="text-center text-muted">
    <h6>No reservations found.</h6>
  </div>

  <!-- Charts Row -->
  <div v-else class="row">
    <!-- Pie Chart -->
    <div class="col-12 col-md-6 mb-4">
      <div class="card custom-outline shadow-sm p-3 h-100">
        <h5 class="text-center custom-text">Reservations per Parking Lot</h5>
        <canvas id="pieChart"></canvas>
      </div>
    </div>

    <!-- Bar Chart -->
    <div class="col-12 col-md-6 mb-4">
      <div class="card custom-outline shadow-sm p-3 h-100">
        <h5 class="text-center custom-text">Amount Paid per Parking Lot (₹)</h5>
        <canvas id="barChart"></canvas>
      </div>
    </div>
  </div>
</div>

</template>

<style scoped>

.card {
  background-color: #fff;
}

@media (max-width: 767px) {
  h5 {
    font-size: 1rem;
  }
}



.custom-text {
  color: rgba(56, 53, 206, 0.74);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 1px solid rgb(56, 53, 206, 0.74); 
  margin-bottom: 20px;

}

.custom-outline:focus {
  outline: none;
  border-color: rgb(56, 53, 206, 0.74); 
  box-shadow: 0 0 4px rgb(56, 53, 206, 0.74);
}

</style>