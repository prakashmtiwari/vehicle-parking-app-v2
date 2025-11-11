<template>
  <div class="user-management-page">
    <AdminNavbar />

    <main class="content-wrapper">
      <div class="admin-container">
        <div class="admin-card">
          <!-- Header Section -->
          <div class="card-header">
            <h2 class="card-title">User Management</h2>
            <p class="card-subtitle">View and manage all registered users in your system.</p>
          </div>

          <!-- Table Section -->
          <div class="table-container">
            <div v-if="loading" class="loading-state">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="loading-text">Loading users...</p>
            </div>

            <div v-else>
              <div class="table-wrapper">
                <table class="custom-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Full Name</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="user in users" :key="user.id">
                      <td>
                        <span class="id-badge">{{ user.id }}</span>
                      </td>
                      <td>
                        <div class="username-cell">
                          <span class="username-icon">👤</span>
                          <span class="username-text">{{ user.username }}</span>
                        </div>
                      </td>
                      <td>
                        <div class="email-cell">
                          <span class="email-icon">✉️</span>
                          <span class="email-text">{{ user.email }}</span>
                        </div>
                      </td>
                      <td class="name-cell">{{ user.fullname }}</td>
                      <td>
                        <div class="action-buttons">
                          <button
                            class="btn-action btn-edit"
                            @click="goToEditUser(user.id)"
                            title="Edit User"
                          >
                            <span class="btn-icon">✏️</span>
                            Edit
                          </button>
                          <!-- Uncomment if delete functionality is needed -->
                          <!-- <button
                            class="btn-action btn-delete"
                            @click="deleteUser(user.id)"
                            title="Delete User"
                          >
                            <span class="btn-icon">🗑️</span>
                            Delete
                          </button> -->
                        </div>
                      </td>
                    </tr>
                    <tr v-if="users.length === 0">
                      <td colspan="5" class="empty-state">
                        <div class="empty-content">
                          <span class="empty-icon">👥</span>
                          <p class="empty-text">No users found.</p>
                          <p class="empty-subtext">Users will appear here once they register.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- User Count Summary -->
              <div v-if="users.length > 0" class="table-footer">
                <p class="user-count">
                  Total Users: <span class="count-badge">{{ users.length }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <AdminFooter />
  </div>
</template>

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
    toast.success("User deleted successfully.")
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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
.user-management-page {
  padding-top: 100px;
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  background-color: #f8fafc;
}

.content-wrapper {
  padding: 2rem;
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px));
  padding-bottom: 3rem;
}

.admin-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* Card Styling */
.admin-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.card-header {
  text-align: left;
  margin-bottom: 2rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.card-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
}

/* Table Styles */
.table-container {
  margin-top: 1.5rem;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  font-size: 0.9rem;
}

.custom-table thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.custom-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.custom-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.custom-table tbody tr:hover {
  background-color: #f8fafc;
}

.custom-table td {
  padding: 1rem;
  color: #334155;
  vertical-align: middle;
}

/* Table Cell Styling */
.id-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f1f5f9;
  color: #475569;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.85rem;
}

.username-cell,
.email-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.username-icon,
.email-icon {
  font-size: 1rem;
  opacity: 0.7;
}

.username-text {
  font-weight: 600;
  color: #1e293b;
}

.email-text {
  color: #64748b;
}

.name-cell {
  font-weight: 500;
  color: #334155;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-icon {
  font-size: 0.9rem;
}

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-edit:hover {
  background: #fde68a;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(146, 64, 14, 0.2);
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(153, 27, 27, 0.2);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem !important;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.empty-text {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

.empty-subtext {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

/* Table Footer */
.table-footer {
  padding: 1rem 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-top: none;
  border-radius: 0 0 0.5rem 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-count {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.count-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .username-cell,
  .email-cell {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .admin-card {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .card-subtitle {
    font-size: 0.9rem;
  }

  .custom-table {
    font-size: 0.8rem;
  }

  .custom-table th,
  .custom-table td {
    padding: 0.75rem 0.5rem;
  }

  .username-cell,
  .email-cell {
    flex-direction: row;
    gap: 0.4rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-action {
    width: 100%;
    justify-content: center;
  }

  .empty-icon {
    font-size: 2rem;
  }

  .empty-text {
    font-size: 1rem;
  }

  .table-footer {
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
}

@media (max-width: 640px) {
  /* Make table scrollable on very small screens */
  .table-wrapper {
    overflow-x: scroll;
  }

  .custom-table {
    min-width: 600px;
  }
}

/* Bootstrap spinner override */
.spinner-border {
  width: 2.5rem;
  height: 2.5rem;
  border-width: 0.25rem;
  color: #667eea;
}
</style>