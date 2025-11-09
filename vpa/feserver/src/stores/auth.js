// src/stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.roles?.includes('admin'),
    isUser: (state) => state.user?.roles?.includes('user'),
  },

  actions: {
    /**
     * Login the user and persist to localStorage
     */
    login(token, user) {
      const tokenKey = `token_${user.username}`
      const userKey = `user_${user.username}`

      this.token = token
      this.user = user

      localStorage.setItem(tokenKey, token)
      localStorage.setItem(userKey, JSON.stringify(user))

  // 👇 This is per-tab (cleared when tab closes)
      sessionStorage.setItem('active_user', user.username)    },

    /**
     * Logout the current user (only clear their token/data)
     */
    logout() {
      if (this.user?.username) {
        const tokenKey = `token_${this.user.username}`
        const userKey = `user_${this.user.username}`

        localStorage.removeItem(tokenKey)
        localStorage.removeItem(userKey)
      }

      // 👇 Also clear this tab's active user session
      const activeUser = sessionStorage.getItem('active_user')
      if (activeUser === this.user.username) {
        sessionStorage.removeItem('active_user')
      }

      this.token = null
      this.user = null
    },

    /**
     * Restore a user session (e.g. on app reload)
     * @param {string} username - The username to restore
     */
    restoreSession(username) {
      const tokenKey = `token_${username}`
      const userKey = `user_${username}`

      const storedToken = localStorage.getItem(tokenKey)
      const storedUser = localStorage.getItem(userKey)

      if (storedToken && storedUser) {
        this.token = storedToken
        this.user = JSON.parse(storedUser)
      } else {
        this.token = null
        this.user = null
      }
    }

  },
})
