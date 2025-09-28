<template>
  <AdminNavbar />

  <div class="container my-5 d-flex flex-column align-items-center">
    <!-- Heading -->
    <h2 class="mb-4 text-center">Edit User</h2>

    <div v-if="error" class="text-danger mb-3 text-center">{{ error }}</div>

    <!-- Card/Form -->
    <div class="card p-4" style="max-width: 600px; width: 100%;">
      <form @submit.prevent="handleSubmit">
        <!-- Username -->
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            id="username"
            class="form-control"
            v-model="form.username"
            placeholder="Enter username"
            required
          />
        </div>

        <!-- First Name -->
        <div class="mb-3">
          <label for="firstName" class="form-label">First Name</label>
          <input
            type="text"
            id="firstName"
            class="form-control"
            v-model="form.first_name"
            placeholder="Enter first name"
          />
        </div>

        <!-- Last Name -->
        <div class="mb-3">
          <label for="lastName" class="form-label">Last Name</label>
          <input
            type="text"
            id="lastName"
            class="form-control"
            v-model="form.last_name"
            placeholder="Enter last name"
          />
        </div>

        <!-- Email -->
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            class="form-control"
            v-model="form.email"
            placeholder="Enter email"
            required
          />
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label">Password (leave blank to keep current)</label>
          <input
            type="password"
            id="password"
            class="form-control"
            v-model="form.password"
            placeholder="Enter new password"
          />
        </div>

        <!-- Actions -->
        <div class="text-end mt-4">
          <button type="button" class="btn btn-light me-2" @click="cancelEdit">Cancel</button>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? "Updating..." : "Update User" }}
          </button>
        </div>
      </form>
    </div>
  </div>

  <AdminFooter />
</template>


<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import userService from "@/services/userManagementService"
import AdminNavbar from "@/components/AdminNavbar.vue"
import AdminFooter from "@/components/AdminFooter.vue"

const route = useRoute()
const router = useRouter()
const userId = route.params.id

const form = reactive({
  username: "",
  first_name: "",
  last_name: "",
  email: "",
  password: ""
})

const loading = ref(false)
const error = ref("")

// Fetch user data on mount
onMounted(async () => {
  loading.value = true
  try {
    const res = await userService.getUser(userId)
    form.username = res.data.username
    form.first_name = res.data.first_name
    form.last_name = res.data.last_name
    form.email = res.data.email
    form.password = res.data.password || ""
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load user"
  } finally {
    loading.value = false
  }
})

// Handle form submission
async function handleSubmit() {
  loading.value = true
  try {
    const payload = {
      username: form.username,
      first_name: form.first_name,
      last_name: form.last_name,
      email: form.email
    }
    // Only include password if entered
    if (form.password) payload.password = form.password

    await userService.updateUser(userId, payload)
    router.push("/users") // go back to user list
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to update user"
    alert(error.value)
  } finally {
    loading.value = false
  }
}

// Cancel button
function cancelEdit() {
  router.push("/users")
}
</script>
