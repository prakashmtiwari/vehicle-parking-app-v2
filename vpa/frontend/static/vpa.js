const { createApp } = Vue

const app = createApp({
  data() {
    return {
      appName: "Vehicle Parking App - V2",
      users: [],
      loading: false,
    }
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const res = await axios.get("/api/v1/users") // backend API call
        this.users = res.data
      } catch (err) {
        console.error("Error fetching users:", err)
      } finally {
        this.loading = false
      }
    }
  },
  template: `
    <div class="container">
      <h1 class="mb-4">{{ appName }}</h1>

      <button class="btn btn-primary mb-3" @click="fetchUsers" :disabled="loading">
        {{ loading ? "Loading..." : "Load Users" }}
      </button>

      <ul class="list-group">
        <li v-for="u in users" :key="u.id" class="list-group-item">
          {{ u.username }} — {{ u.email }}
        </li>
      </ul>
    </div>
  `
})

app.mount('#app')
