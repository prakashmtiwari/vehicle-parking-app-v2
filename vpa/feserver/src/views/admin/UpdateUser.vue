<template>
  <div class="edit-user-page">
    <AdminNavbar />

    <main class="content-wrapper">
      <div class="admin-container">
        <div class="admin-card">
          <!-- Header Section -->
          <div class="card-header">
            <div class="header-content">
              <button class="btn-back" @click="cancelEdit" title="Back to Users">
                ← Back
              </button>
              <div class="header-text">
                <h2 class="card-title">Edit User</h2>
                <p class="card-subtitle">Update user information and credentials.</p>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="alert-error">
            <span class="alert-icon">⚠️</span>
            <span>{{ error }}</span>
          </div>

          <!-- Loading State -->
          <div v-if="loading && !form.username" class="loading-state">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="loading-text">Loading user data...</p>
          </div>

          <!-- Form Section -->
          <div v-else class="form-container">
            <form @submit.prevent="handleSubmit">
              <!-- Username Field -->
              <div class="form-group">
                <label for="username" class="form-label">
                  <span class="label-icon">👤</span>
                  Username
                  <span class="required">*</span>
                </label>
                <input
                  type="text"
                  id="username"
                  class="form-input"
                  v-model="form.username"
                  placeholder="Enter username"
                  required
                />
              </div>

              <!-- Name Fields Row -->
              <div class="form-row">
                <!-- First Name -->
                <div class="form-group">
                  <label for="firstName" class="form-label">
                    <span class="label-icon">📝</span>
                    First Name
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    class="form-input"
                    v-model="form.first_name"
                    placeholder="Enter first name"
                  />
                </div>

                <!-- Last Name -->
                <div class="form-group">
                  <label for="lastName" class="form-label">
                    <span class="label-icon">📝</span>
                    Last Name
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    class="form-input"
                    v-model="form.last_name"
                    placeholder="Enter last name"
                  />
                </div>
              </div>

              <!-- Email Field -->
              <div class="form-group">
                <label for="email" class="form-label">
                  <span class="label-icon">✉️</span>
                  Email Address
                  <span class="required">*</span>
                </label>
                <input
                  type="email"
                  id="email"
                  class="form-input"
                  v-model="form.email"
                  placeholder="Enter email address"
                  required
                />
              </div>

              <!-- Password Field -->
              <div class="form-group">
                <label for="password" class="form-label">
                  <span class="label-icon">🔒</span>
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  class="form-input"
                  v-model="form.password"
                  placeholder="Enter new password"
                />
                <p class="field-hint">Leave blank to keep the current password</p>
              </div>

              <!-- Action Buttons -->
              <div class="form-actions">
                <button 
                  type="button" 
                  class="btn-action btn-cancel" 
                  @click="cancelEdit"
                  :disabled="loading"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  class="btn-action btn-submit" 
                  :disabled="loading"
                >
                  <span v-if="loading" class="btn-spinner">
                    <span class="spinner-small"></span>
                    Updating...
                  </span>
                  <span v-else>
                    <span class="btn-icon">✓</span>
                    Update User
                  </span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>

    <AdminFooter />
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import userService from "@/services/userManagementService"
import AdminNavbar from "@/components/AdminNavbar.vue"
import AdminFooter from "@/components/AdminFooter.vue"
import { useToast } from "vue-toastification";

const toast = useToast()

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
    // Don't populate password field for security
    form.password = ""
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
  error.value = ""
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
    toast.success("User details updated successfully")
    router.push("/users") // go back to user list
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to update user"
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

// Cancel button
function cancelEdit() {
  router.push("/users")
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
.edit-user-page {
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
  max-width: 700px;
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

/* Header Section */
.card-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1.5rem;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn-back {
  align-self: flex-start;
  background: none;
  border: none;
  color: #667eea;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: all 0.2s ease;
}

.btn-back:hover {
  color: #764ba2;
  transform: translateX(-2px);
}

.header-text {
  text-align: left;
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

/* Alert Error */
.alert-error {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #991b1b;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.alert-icon {
  font-size: 1.25rem;
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

/* Form Container */
.form-container {
  margin-top: 1rem;
}

/* Form Groups */
.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #334155;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.label-icon {
  font-size: 1rem;
}

.required {
  color: #ef4444;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-family: 'Poppins', sans-serif;
  color: #1e293b;
  transition: all 0.2s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

.field-hint {
  margin: 0.5rem 0 0 0;
  font-size: 0.85rem;
  color: #64748b;
  font-style: italic;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f1f5f9;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #f1f5f9;
  color: #475569;
}

.btn-cancel:hover:not(:disabled) {
  background: #e2e8f0;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  font-size: 1.1rem;
}

.btn-spinner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner-small {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Bootstrap spinner override */
.spinner-border {
  width: 2.5rem;
  height: 2.5rem;
  border-width: 0.25rem;
  color: #667eea;
}

/* Responsive Design */
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

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn-action {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .admin-card {
    padding: 1.25rem;
  }

  .card-title {
    font-size: 1.25rem;
  }

  .form-input {
    padding: 0.65rem 0.85rem;
    font-size: 0.9rem;
  }

  .form-label {
    font-size: 0.85rem;
  }
}
</style>