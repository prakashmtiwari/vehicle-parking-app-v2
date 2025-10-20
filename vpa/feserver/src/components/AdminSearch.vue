<template>
  <div class="d-flex items-center justify-center min-h-screen">
  <div class="p-6 max-w-2xl mx-auto">
    <div class="d-flex justify-content-center">
    <h2 class="text-2xl text-custom font-semibold mb-6">🔍 Search</h2>
    </div><br>

    <!-- Filter Selector -->
    <div class="d-flex gap-3 mb-5 justify-content-center">
      <select v-model="filter" class="custom-outline p-2 rounded w-1/3">
        <option disabled value="">Select Filter</option>
        <option value="lots">Parking Lots</option>
        <option value="spots">Parking Spots</option>
        <option value="users">Users</option>
      </select>

      <!-- Status dropdown for parking spots -->
      <select v-if="filter === 'spots'" v-model="status" class="custom-outline p-2 rounded w-1/3">
        <option disabled value="">Select Status</option>
        <option value="available">Available</option>
        <option value="occupied">Occupied</option>
      </select>

      <!-- Query Input -->
      <input
        v-if="filter !== 'spots'"
        v-model="query"
        placeholder="Enter search query"
        class="custom-outline p-2 rounded flex-grow"
        @keyup.enter="triggerSearch"
      />
    </div>
  
    <!-- Search Button -->
    <div class="d-flex align-items-center justify-content-center">
    <button
      :disabled="!filter"
      @click="triggerSearch"
      class="bg-blue-600 search custom-outline text-black"
    >
      Search
    </button>
    </div>

    <!-- Results Section -->
   <div v-if="results.length" class="mt-5">
  <h3 class="text-center text-custom mb-4 fw-semibold">Search Results</h3>

  <!-- Parking Lots -->
  <div v-if="filter === 'lots'" class="row g-3">
    <div v-for="lot in results" :key="lot.id" class="col-12 col-md-6 col-lg-12">
      <div class="card  h-100 shadow-sm border-0">
        <div class="card-body custom-outline text-center">
          <h5 class="card-title custom-text fw-bold text-primary">Location: {{ lot.name }}</h5>
          <p class="card-text text-muted mb-1">
            <i class="bi bi-geo-alt-fill text-danger me-1"></i>Address: {{ lot.address }}
          </p>
          <p class="card-text mb-0">
            <strong>Pincode:</strong> {{ lot.pincode }}
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- Parking Spots -->
  <div v-else-if="filter === 'spots'" class="table-responsive">
    <table class="table table-hover custom-outline align-middle shadow-sm">
      <thead class="table-white">
        <tr>
          <th scope="col">Spot ID</th>
          <th scope="col">Lot ID</th>
          <th scope="col">Location</th>
          <th scope="col">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="spot in results" :key="spot.id">
          <td>{{ spot.id }}</td>
          <td>{{ spot.lot_id }}</td>
          <td>{{ spot.location }}</td>
          <td>
            <span
              class="badge px-3 py-2"
              :class="spot.is_occupied ? 'bg-danger' : 'bg-success'"
            >
              {{ spot.is_occupied ? 'Occupied' : 'Available' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Users -->
  <div v-else-if="filter === 'users'" class="row g-3  ">
    <div v-for="user in results" :key="user.id" class="col-12 col-md-6 col-lg-12">
      <div class="card h-100 border-1 text-center shadow-sm">
        <div class="card-body custom-outline">
          <h5 class="card-title fw-bold text-dark">
            <i class="bi bi-person-circle me-2 text-primary"></i>Username: {{ user.username }}
          </h5>
          <p class="card-text text-muted mb-1">Email: {{ user.email }}</p>
          <p class="card-text small">
            Name: {{ user.first_name }} {{ user.last_name }}
          </p>
        </div>
      </div>
    </div>
  </div>
</div>

  <div v-else-if="searched" class="noresults">  
      <p  class="mt-6 text-gray-500 italic">No results found.</p>
  </div>

  </div>
</div>
</template>


<script setup>
import { ref,  watch } from "vue";
import axios from "axios";
import { useToast } from "vue-toastification";

const filter = ref("");
const query = ref("");
const status = ref("");
const results = ref([]);
const searched = ref(false);
const toast = useToast();

async function triggerSearch() {
  if (!filter.value) {
    toast.warning("Please select a filter type.");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    console.log("TOKEN:", token);

    let API_URL_BASE = `http://localhost:5000`
    let endpoint = `/search/${filter.value}`;
    const params = {};

    if (filter.value === "spots") {
      params.status = status.value;
      if (!status.value) {
        toast.warning("Please select a spot status.");
        return;
      }
    } else {
      params.query = query.value;
      if (!query.value.trim()) {
        toast.warning("Please enter a search term.");
        return;
      }
    }

    if (!token) {
        toast.error("Session expired. Please log in again.");
        return;
    }

    const res = await axios.get(`${API_URL_BASE}${endpoint}`, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });

    results.value = res.data;
    searched.value = true;

    if (res.data.length > 0) {
      toast.success(`Found ${res.data.length} ${filter.value}.`);
    } else {
      toast.info("No results found.");
    }
  } catch (err) {
    toast.error("Failed to search. Please try again.");
    console.error(err);
  }
}

watch(filter, () => {
  results.value = [];
  query.value = "";
  status.value = "";
  searched.value = false;
});



</script>

<style scoped>
select, input {
  min-width: 150px;
  font-family: sans-serif;
  border: 1px solid rgb(218, 47, 218);
}

.search {
  background-color: white;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
  border-radius: 5rem;
  cursor: pointer;
}

.custom-outline {
  border: 1px solid rgb(218, 47, 218); 
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}

.text-custom {
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.noresults{
  padding-top: 50px;
  padding-left: 130px;
}
</style>
