<script setup>
import { ref, onMounted } from "vue"
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale
} from "chart.js"
import ChartDataLabels from "chartjs-plugin-datalabels"
import { Pie, Bar } from "vue-chartjs"
import reservationService from "@/services/reservationService"

// Register Chart.js + datalabels
ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale, ChartDataLabels)

const reservations = ref([])
const lotLabels = ref([])
const reservationCounts = ref([])
const lotPayments = ref([])

async function loadData() {
  try {
    const res = await reservationService.getUserReservations()
    reservations.value = res.data

    const lotMap = {}
    reservations.value.forEach(r => {
      const lotName = r.spot?.lot?.prime_location_name || "Unknown"
      if (!lotMap[lotName]) {
        lotMap[lotName] = { count: 0, amount: 0 }
      }
      lotMap[lotName].count += 1
      lotMap[lotName].amount += r.amount_paid || 0
    })

    lotLabels.value = Object.keys(lotMap)
    reservationCounts.value = Object.values(lotMap).map(v => v.count)
    lotPayments.value = Object.values(lotMap).map(v => v.amount)
  } catch (err) {
    console.error("Error loading reservations:", err)
  }
}

onMounted(loadData)
</script>

<template>
  <div class="container my-5">
    <h2 class="mb-4 custom-text">Reservation Summary</h2>

    <div v-if="reservations.length === 0">
        <h6 colspan="10" class="text-center text-muted">
          No reservations found.
        </h6>
    </div>
     <div v-else>
    <div class="row">
      <!-- Pie Chart -->
      <div class="col-md-6">
        <div class="card custom-outline shadow-sm p-3">
          <h5 class="text-center custom-text">Reservations per Parking Lot</h5>
          <Pie
            v-if="lotLabels.length"
            :data="{
              labels: lotLabels,
              datasets: [
                {
                  label: 'Reservations',
                  data: reservationCounts,
                  backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#20c997'],
                }
              ]
            }"
            :options="{
              plugins: {
                datalabels: {
                  color: '#fff',
                  formatter: (value, context) => {
                    const total = context.chart.data.datasets[0].data.reduce((a,b) => a+b, 0)
                    const percentage = ((value / total) * 100).toFixed(1)
                    return `${value} (${percentage}%)`
                  }
                }
              }
            }"
          />
        </div>
      </div>

      <!-- Bar Chart -->
      <div class="col-md-6">
        <div class="card custom-outline shadow-sm p-3">
          <h5 class="text-center custom-text">Amount Paid per Parking Lot (₹)</h5>
          <Bar
            v-if="lotLabels.length"
            :data="{
              labels: lotLabels,
              datasets: [
                {
                  label: 'Amount Paid',
                  data: lotPayments,
                  backgroundColor: '#17a2b8'
                }
              ]
            }"
            :options="{
              responsive: true,
              plugins: {
                legend: { display: false },
                datalabels: {
                  anchor: 'end',
                  align: 'top',
                  formatter: (value) => `₹${value.toFixed(0)}`
                }
              },
              scales: {
                y: { beginAtZero: true }
              }
            }"
          />
        </div>
      </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.custom-text {
  color: rgb(56, 53, 206, 0.74);
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

.container{
  padding-bottom: 80px;
}

</style>