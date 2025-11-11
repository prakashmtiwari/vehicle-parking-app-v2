<template>
  <div class="search-component">
    <!-- Header Section -->
    <div class="search-header">
      <h2 class="search-title">🔍 Search</h2>
      <p class="search-subtitle">Find parking lots, spots, and users across the system</p>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <select v-model="filter" class="filter-select">
        <option disabled value="">Select Filter</option>
        <option value="lots">Parking Lots</option>
        <option value="spots">Parking Spots</option>
        <option value="users">Users</option>
      </select>

      <!-- Status dropdown for parking spots -->
      <select v-if="filter === 'spots'" v-model="status" class="filter-select">
        <option disabled value="">Select Status</option>
        <option value="available">Available</option>
        <option value="occupied">Occupied</option>
      </select>

      <!-- Query Input -->
      <input
        v-if="filter !== 'spots'"
        v-model="query"
        placeholder="Enter search query"
        class="search-input"
        @keyup.enter="triggerSearch"
      />
    </div>
  
    <!-- Search Button -->
    <div class="button-wrapper">
      <button
        :disabled="!filter"
        @click="triggerSearch"
        class="search-button"
        :class="{ 'button-disabled': !filter }"
      >
        Search
      </button>
    </div>

    <!-- Results Section -->
    <div v-if="results.length" class="results-section">
      <h3 class="results-title">Search Results</h3>

      <!-- Parking Lots -->
      <div v-if="filter === 'lots'" class="lots-grid">
        <div v-for="lot in results" :key="lot.id" class="lot-card">
          <h5 class="lot-title">📍 {{ lot.name }}</h5>
          <p class="lot-address">{{ lot.address }}</p>
          <p class="lot-pincode"><strong>Pincode:</strong> {{ lot.pincode }}</p>
        </div>
      </div>

      <!-- Parking Spots -->
      <div v-else-if="filter === 'spots'" class="table-card">
        <div class="table-wrapper">
          <table class="results-table">
            <thead>
              <tr>
                <th>Spot ID</th>
                <th>Lot ID</th>
                <th>Location</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="spot in results" :key="spot.id">
                <td><span class="spot-badge">{{ spot.id }}</span></td>
                <td><span class="id-badge">{{ spot.lot_id }}</span></td>
                <td class="location-cell">{{ spot.location }}</td>
                <td>
                  <span :class="['status-badge', spot.status == 'O' ? 'status-occupied' : 'status-available']">
                    {{ spot.status == 'O' ? 'Occupied' : 'Available' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Users -->
      <div v-else-if="filter === 'users'" class="users-grid">
        <div v-for="user in results" :key="user.id" class="user-card">
          <h5 class="user-name">👤 {{ user.username }}</h5>
          <p class="user-email">{{ user.email }}</p>
          <p class="user-fullname">{{ user.first_name }} {{ user.last_name }}</p>
        </div>
      </div>
    </div>

    <div v-else-if="searched" class="empty-state">
      <p class="empty-text">No results found.</p>
      <p class="empty-subtext">Try adjusting your search criteria.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import { useToast } from "vue-toastification"
import AdminSearchService from "@/services/adminSearchService.js"

const filter = ref("")
const query = ref("")
const status = ref("")
const results = ref([])
const searched = ref(false)
const toast = useToast()

async function triggerSearch() {
  try {
    if (!filter.value) {
      toast.warning("Please select a filter type.")
      return
    }

    const data = await AdminSearchService.search(
      filter.value,
      query.value,
      status.value
    )

    results.value = data
    searched.value = true

    if (data.length > 0) {
      toast.success(`Found ${data.length} ${filter.value}.`)
    } else {
      toast.warning("No results found.")
    }
  } catch (err) {
    if (err.message.includes("login")) {
      toast.error("Session expired. Please log in again.")
    } else {
      toast.error(err.message || "Failed to search. Please try again.")
    }
    console.error("Search Error:", err)
  }
}

watch(filter, () => {
  results.value = []
  query.value = ""
  status.value = ""
  searched.value = false
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Component Container */
.search-component {
  font-family: 'Poppins', sans-serif;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header Section */
.search-header {
  margin-bottom: 2rem;
}

.search-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.search-title::before {
  content: '';
  width: 4px;
  height: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.search-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  padding-left: 1rem;
}

/* Filter Section */
.filter-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-select,
.search-input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-family: 'Poppins', sans-serif;
  font-size: 0.9rem;
  color: #334155;
  transition: all 0.2s ease;
  background: white;
}

.filter-select {
  min-width: 200px;
}

.search-input {
  flex: 1;
  min-width: 250px;
}

.filter-select:focus,
.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Button */
.button-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.search-button {
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
}

.search-button:hover:not(.button-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px -2px rgba(102, 126, 234, 0.4);
}

.search-button:active:not(.button-disabled) {
  transform: translateY(0);
}

.button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Results Section */
.results-section {
  margin-top: 2rem;
}

.results-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1.5rem 0;
  text-align: center;
}

/* Parking Lots Grid */
.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.lot-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.lot-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #667eea;
  margin: 0 0 0.75rem 0;
}

.lot-address {
  color: #64748b;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.lot-pincode {
  color: #334155;
  margin: 0;
  font-size: 0.85rem;
}

/* Users Grid */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.user-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.75rem 0;
}

.user-email {
  color: #64748b;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.user-fullname {
  color: #334155;
  margin: 0;
  font-size: 0.85rem;
}

/* Table Card (for Spots) */
.table-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.table-wrapper {
  overflow-x: auto;
}

/* Table Styles */
.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.results-table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.results-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: white;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.results-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.results-table tbody tr:hover {
  background-color: #f8fafc;
}

.results-table tbody tr:last-child {
  border-bottom: none;
}

.results-table td {
  padding: 1rem;
  color: #334155;
  vertical-align: middle;
}

/* Badges */
.id-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f1f5f9;
  color: #475569;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.8rem;
}

.spot-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.8rem;
}

.location-cell {
  color: #475569;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.status-available {
  background: #d1fae5;
  color: #065f46;
}

.status-occupied {
  background: #fee2e2;
  color: #991b1b;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  margin-top: 2rem;
}

.empty-text {
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
  margin: 0 0 0.5rem 0;
}

.empty-subtext {
  color: #94a3b8;
  font-size: 0.85rem;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .search-component {
    padding: 1rem;
  }

  .search-title {
    font-size: 1.25rem;
  }

  .filter-section {
    flex-direction: column;
  }

  .filter-select,
  .search-input {
    width: 100%;
  }

  .lots-grid,
  .users-grid {
    grid-template-columns: 1fr;
  }

  .results-table {
    font-size: 0.75rem;
  }

  .results-table th,
  .results-table td {
    padding: 0.75rem 0.5rem;
  }
}
</style>