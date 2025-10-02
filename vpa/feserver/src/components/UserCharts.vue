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
    <h2 class="mb-4 text-primary">Reservation Summary</h2>

    <div class="row">
      <!-- Pie Chart -->
      <div class="col-md-6">
        <div class="card shadow-sm p-3">
          <h5 class="text-center">Reservations per Parking Lot</h5>
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
        <div class="card shadow-sm p-3">
          <h5 class="text-center">Amount Paid per Parking Lot (₹)</h5>
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
</template>
