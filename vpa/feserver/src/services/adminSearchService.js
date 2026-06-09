import axios from "axios"
import { useAuthStore } from "@/stores/auth"
import { API_HOST } from "./apiConfig"

const API_BASE_URL = `${API_HOST}`

export function authHeader() {
  const auth = useAuthStore()

  let token = auth.token
  if (!token && auth.user?.username) {
    token = localStorage.getItem(`token_${auth.user.username}`)
  }

  return token ? { Authorization: `Bearer ${token}` } : {}
}

export default {
  async search(filter, query, status) {
    if (!filter) throw new Error("Filter type is required")

    const endpoint = `/search/${filter}`
    const params = {}

    if (filter === "spots") {
      if (!status) throw new Error("Please select a spot status.")
      params.status = status
    } else {
      if (!query?.trim()) throw new Error("Please enter a search term.")
      params.query = query.trim()
    }

    const response = await axios.get(`${API_BASE_URL}${endpoint}`, {
      params,
      headers: authHeader(),
    })

    return response.data
  },
}
