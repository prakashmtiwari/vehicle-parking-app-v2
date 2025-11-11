<template>
  <AdminNavbar />

  <div class="form-container">
    <div class="form-wrapper">
      <!-- Header Section -->
      <div class="form-header">
        <h2 class="form-title">
          {{ isEdit ? "Edit Parking Lot" : "Add New Parking Lot" }}
        </h2>
        <p class="form-subtitle">
          {{ isEdit ? "Update parking lot information" : "Create a new parking lot in the system" }}
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading && isEdit" class="loading-state">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="loading-text">Loading parking lot details...</p>
      </div>

      <!-- Form Card -->
      <div v-else class="form-card">
        <form @submit.prevent="handleSubmit">
          <div class="form-grid">
            <!-- Prime Location -->
            <div class="form-group">
              <label for="primeLocation" class="form-label">
                <span class="label-icon">📍</span>
                Prime Location
                <span class="required">*</span>
              </label>
              <input
                type="text"
                class="form-input"
                id="primeLocation"
                v-model="form.prime_location_name"
                placeholder="e.g., Downtown Plaza"
                required
              />
            </div>

            <!-- Price -->
            <div class="form-group">
              <label for="price" class="form-label">
                <span class="label-icon">💰</span>
                Price per Hour
                <span class="required">*</span>
              </label>
              <div class="input-with-prefix">
                <span class="input-prefix">₹</span>
                <input
                  type="number"
                  class="form-input with-prefix"
                  id="price"
                  v-model.number="form.price"
                  placeholder="50"
                  min="0"
                  step="0.01"
                  required
                />
              </div>
            </div>

            <!-- Address -->
            <div class="form-group full-width">
              <label for="address" class="form-label">
                <span class="label-icon">🏠</span>
                Address
                <span class="required">*</span>
              </label>
              <input
                type="text"
                class="form-input"
                id="address"
                v-model="form.address"
                placeholder="Enter complete address"
                required
              />
            </div>

            <!-- Pin Code -->
            <div class="form-group">
              <label for="pinCode" class="form-label">
                <span class="label-icon">📮</span>
                Pin Code
              </label>
              <input
                type="text"
                class="form-input"
                id="pinCode"
                v-model="form.pin_code"
                placeholder="110001"
                maxlength="6"
                pattern="[0-9]{6}"
              />
            </div>

            <!-- Max Spots -->
            <div class="form-group">
              <label for="maxSpots" class="form-label">
                <span class="label-icon">🅿️</span>
                Maximum Spots
                <span class="required">*</span>
              </label>
              <input
                type="number"
                class="form-input"
                id="maxSpots"
                v-model.number="form.maximum_number_of_spots"
                placeholder="100"
                min="1"
                required
              />
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="error-message">
            <span class="error-icon">⚠️</span>
            {{ error }}
          </div>

          <!-- Actions -->
          <div class="form-actions">
            <button 
              type="button" 
              class="btn btn-cancel" 
              @click="cancelForm"
              :disabled="loading"
            >
              Cancel
            </button>
            <button 
              type="submit" 
              class="btn btn-submit"
              :disabled="loading"
            >
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Saving...' : (isEdit ? 'Update Parking Lot' : 'Create Parking Lot') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <AdminFooter />
</template>

<script setup>
import { reactive, ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import parkingLotService from "@/services/parkingLotService"
import AdminNavbar from "@/components/AdminNavbar.vue"
import AdminFooter from "@/components/AdminFooter.vue"
import { useToast } from "vue-toastification"

const toast = useToast()

// Router hooks
const route = useRoute()
const router = useRouter()
const lotId = route.params.id

// Determine if we're in Edit mode
const isEdit = computed(() => !!route.params.id)

// Form state
const form = reactive({
  prime_location_name: "",
  price: null,
  address: "",
  pin_code: "",
  maximum_number_of_spots: null
})

// Loading state
const loading = ref(false)
const error = ref("")

// Fetch existing lot if editing
onMounted(async () => {
  if (lotId) {
    loading.value = true
    try {
      const res = await parkingLotService.getLot(lotId)
      Object.assign(form, {
        prime_location_name: res.data.prime_location_name,
        price: res.data.price,
        address: res.data.address,
        pin_code: res.data.pin_code,
        maximum_number_of_spots: res.data.maximum_number_of_spots
      })
    } catch (err) {
      console.error(err)
      error.value = err.response?.data?.message || err.message || "Failed to load parking lot"
      toast.error(error.value)
    } finally {
      loading.value = false
    }
  }
})

// Submit handler
async function handleSubmit() {
  error.value = ""
  
  // Validation
  if (!form.prime_location_name || !form.price || !form.address || !form.maximum_number_of_spots) {
    toast.error("Please fill all required fields")
    return
  }

  loading.value = true
  try {
    if (isEdit.value) {
      await parkingLotService.updateLot(route.params.id, form)
      toast.success("Parking lot updated successfully!")
    } else {
      await parkingLotService.createLot(form)
      toast.success("Parking lot created successfully!")
    }
    router.push("/parking-lots")
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to save parking lot"
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

// Cancel handler
function cancelForm() {
  router.push("/parking-lots")
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Container */
.form-container {
  font-family: 'Poppins', sans-serif;
  min-height: calc(100vh - 120px);
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
}

.form-wrapper {
  padding-top: 100px;
  max-width: 900px;
  margin: 0 auto;
}

/* Header Section */
.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.form-title::before {
  content: '';
  width: 4px;
  height: 1.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.form-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.3rem;
  border-color: #667eea;
  border-right-color: transparent;
}

/* Form Card */
.form-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

/* Form Labels */
.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label-icon {
  font-size: 1.1rem;
}

.required {
  color: #ef4444;
  font-weight: 700;
}

/* Form Inputs */
.form-input {
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
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

/* Input with Prefix */
.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 1rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  pointer-events: none;
}

.form-input.with-prefix {
  padding-left: 2.5rem;
}

/* Error Message */
.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #dc2626;
  font-size: 0.9rem;
}

.error-icon {
  font-size: 1.25rem;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f1f5f9;
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background: #f1f5f9;
  color: #64748b;
}

.btn-cancel:hover:not(:disabled) {
  background: #e2e8f0;
  color: #475569;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  min-width: 180px;
}

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: 0.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .form-container {
    padding: 1.5rem 1rem;
  }

  .form-title {
    font-size: 1.5rem;
  }

  .form-subtitle {
    font-size: 0.85rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }

  .form-group.full-width {
    grid-column: 1;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .form-container {
    padding: 1rem 0.5rem;
  }

  .form-card {
    padding: 1.25rem;
    border-radius: 0.75rem;
  }

  .form-title {
    font-size: 1.25rem;
  }

  .label-icon {
    font-size: 1rem;
  }

  .form-input {
    padding: 0.65rem 0.85rem;
    font-size: 0.9rem;
  }
}
</style>