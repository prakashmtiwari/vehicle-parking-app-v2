<script setup>
import { ref, onMounted } from "vue"
import { Chart, registerables } from "chart.js"
import reservationService from "@/services/reservationService"

Chart.register(...registerables)

const reservations = ref([])
let pieChartInstance = null
let barChartInstance = null

async function loadReservations() {
  try {
    const res = await reservationService.getAllReservations()
    reservations.value = res.data
    renderCharts()
  } catch (err) {
    console.error("Error loading reservations:", err)
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

    <div class="row">
      <!-- Pie Chart -->
      <div class="col-12 col-md-6 mb-4">
        <div class="card custom-outline shadow-sm p-3">
          <h5 class="text-center custom-text">Reservations per Parking Lot</h5>
          <canvas id="pieChart"></canvas>
        </div>
      </div>

      <!-- Bar Chart -->
      <div class="col-12 col-md-6 mb-4">
        <div class="card custom-outline shadow-sm p-3">
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
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 2px solid rgb(218, 47, 218); 
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}

</style>