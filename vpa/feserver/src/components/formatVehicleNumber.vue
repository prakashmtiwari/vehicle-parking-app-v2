<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue'])

const displayValue = ref('')

// Format vehicle number with hyphens
function formatVehicleNumber(value) {
  // Remove all non-alphanumeric characters
  const cleaned = value.replace(/[^A-Za-z0-9]/g, '').toUpperCase()
  
  // Apply formatting: XX-XX-XX-XXXX or XX-XX-XXXX
  let formatted = ''
  
  if (cleaned.length <= 2) {
    formatted = cleaned
  } else if (cleaned.length <= 4) {
    formatted = `${cleaned.slice(0, 2)}-${cleaned.slice(2)}`
  } else if (cleaned.length <= 6) {
    formatted = `${cleaned.slice(0, 2)}-${cleaned.slice(2, 4)}-${cleaned.slice(4)}`
  } else {
    formatted = `${cleaned.slice(0, 2)}-${cleaned.slice(2, 4)}-${cleaned.slice(4, 6)}-${cleaned.slice(6, 10)}`
  }
  
  return formatted
}

function handleInput(event) {
  const value = event.target.value
  const formatted = formatVehicleNumber(value)
  displayValue.value = formatted
  
  // Store without hyphens and emit to parent
  const cleanValue = formatted.replace(/-/g, '')
  emit('update:modelValue', cleanValue)
  
  // Update the input field
  event.target.value = formatted
}

function handlePaste(event) {
  event.preventDefault()
  const pastedText = event.clipboardData.getData('text')
  const formatted = formatVehicleNumber(pastedText)
  displayValue.value = formatted
  
  // Store without hyphens and emit to parent
  const cleanValue = formatted.replace(/-/g, '')
  emit('update:modelValue', cleanValue)
  
  event.target.value = formatted
}

// Watch for external changes to modelValue (like when modal opens)
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    displayValue.value = formatVehicleNumber(newValue)
  } else {
    displayValue.value = ''
  }
}, { immediate: true })
</script>

<template>
  <div class="form-group">
    <label class="form-label">Vehicle Number</label>
    <input
      type="text"
      :value="displayValue"
      @input="handleInput"
      @paste="handlePaste"
      class="form-input"
      placeholder="DL-01-AB-1234"
      maxlength="15"
      required
    />
    <small class="form-hint">Format: State-District-Series-Number (e.g., DL-01-AB-1234)</small>
  </div>
</template>

<style scoped>
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-family: 'Courier New', monospace;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.form-hint {
  display: block;
  margin-top: 0.5rem;
  color: #64748b;
  font-size: 0.85rem;
}
</style>