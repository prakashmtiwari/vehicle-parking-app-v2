<template>
  <div class="p-6 max-w-2xl mx-auto">
    <h2 class="text-2xl font-semibold mb-6">🔍 Search</h2>

    <!-- Filter Selector -->
    <div class="flex gap-3 mb-4">
      <select v-model="filter" class="border p-2 rounded w-1/3">
        <option disabled value="">Select Filter</option>
        <option value="lots">Parking Lots</option>
        <option value="spots">Parking Spots</option>
        <option value="users">Users</option>
      </select>

      <!-- Status dropdown for parking spots -->
      <select v-if="filter === 'spots'" v-model="status" class="border p-2 rounded w-1/3">
        <option disabled value="">Select Status</option>
        <option value="available">Available</option>
        <option value="occupied">Occupied</option>
      </select>

      <!-- Query Input -->
      <input
        v-if="filter !== 'spots'"
        v-model="query"
        placeholder="Enter search query"
        class="border p-2 rounded flex-grow"
        @keyup.enter="triggerSearch"
      />
    </div>

    <button
      :disabled="!filter"
      @click="triggerSearch"
      class="bg-blue-600 text-black px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
    >
      Search
    </button>

    <!-- Results Section -->
    <div v-if="results.length" class="mt-6">
      <h3 class="text-lg font-semibold mb-3">Results:</h3>

      <div v-if="filter === 'lots'">
        <ul>
          <li v-for="lot in results" :key="lot.id" class="border-b py-2">
            <strong>{{ lot.name }}</strong> — {{ lot.pincode }} <br />
            <small>{{ lot.address }}</small>
          </li>
        </ul>
      </div>

      <div v-else-if="filter === 'spots'">
        <ul>
          <li v-for="spot in results" :key="spot.id" class="border-b py-2">
            Spot ID: {{ spot.id }} — Lot: {{ spot.lot_id }} — 
            <span :class="spot.is_occupied ? 'text-red-600' : 'text-green-600'">
              {{ spot.is_occupied ? 'Occupied' : 'Available' }}
            </span>
          </li>
        </ul>
      </div>

      <div v-else-if="filter === 'users'">
        <ul>
          <li v-for="user in results" :key="user.id" class="border-b py-2">
            {{ user.username }} — <small>{{ user.email }}</small>
          </li>
        </ul>
      </div>
    </div>

    <p v-else-if="searched" class="mt-6 text-gray-500 italic">No results found.</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
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
    const token = localStorage.getItem("access_token");
    let API_URL_BASE = `http://localhost:5000`
    let endpoint = `/api/search/${filter.value}`;
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
</script>

<style scoped>
select, input {
  min-width: 150px;
}
</style>
