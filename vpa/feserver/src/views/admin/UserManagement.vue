<template>
  <AdminNavbar />

  <div class="container my-5">
    <h2 class="mb-4 custom-text">User Management</h2>


    <div class="card custom-outline p-3">
      <h3 style="text-align: center;">Registered Users</h3>

      <div v-if="loading" class="py-4 text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <table class="table table-hover align-middle table-responsive table-sm mt-3">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Name</th>
              <th>Update User</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.fullname }}</td>
              <td>
                <button
                  class="btn btn-sm btn-warning me-2"
                  @click="goToEditUser(user.id)"
                >
                  Edit
                </button>
                <!-- <button
                  class="btn btn-sm btn-danger"
                  @click="deleteUser(user.id)"
                >
                  Delete
                </button> -->
              </td>
            </tr>
            <tr v-if="users.length === 0">
              <td colspan="5" class="text-center">No users found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <AdminFooter />
</template>

<style scoped>
.custom-text {
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 1px solid rgb(218, 47, 218); 
  margin-bottom: 20px;
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}

</style>


<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import userService from "@/services/userManagementService"
import AdminNavbar from "@/components/AdminNavbar.vue"
import AdminFooter from "@/components/AdminFooter.vue"
import { useToast } from "vue-toastification";



const toast = useToast();
const users = ref([])
const loading = ref(false)
const error = ref("")

const router = useRouter()

// Load all users
async function loadUsers() {
  loading.value = true
  error.value = ""
  try {
    const res = await userService.getUsers()
    users.value = res.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load users"
  } finally {
    loading.value = false
  }
}

// Delete user
async function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return
  try {
    await userService.deleteUser(id)
    await loadUsers()
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to delete user"
    toast.error(error.value)
  }
}


// Navigate to Edit User page
function goToEditUser(id) {
  router.push(`/users/${id}/edit`)
}

// Fetch users on mount
onMounted(loadUsers)
</script>
