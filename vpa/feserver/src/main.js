import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import 'bootstrap/dist/css/bootstrap.min.css'


import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())


// ✅ On reload, restore this tab's active user
const auth = useAuthStore()

const activeUser = sessionStorage.getItem('active_user')
if (activeUser) {
  auth.restoreSession(activeUser)
}

// logout from all tabs if a user logs out of one tab
window.addEventListener('storage', (event) => {
  if (event.key?.startsWith('token_') && !event.newValue) {
    const username = event.key.replace('token_', '')
    const activeUser = sessionStorage.getItem('active_user')

    if (activeUser === username) {
      const auth = useAuthStore()
      auth.logout()
    }
  }
})




app.use(router)
app.use(Toast)

app.mount('#app')
