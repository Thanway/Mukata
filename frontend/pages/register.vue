<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow w-80">
      <h1 class="text-xl font-bold mb-4 text-center">Register</h1>
      
      <input
        v-model="username"
        placeholder="Username"
        class="mb-3 p-2 border w-full rounded"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="mb-3 p-2 border w-full rounded"
      />
      
      <input
        v-model="confirmPassword"
        type="password"
        placeholder="Confirm Password"
        class="mb-4 p-2 border w-full rounded"
      />

      <button
        @click="handleRegister"
        class="bg-green-500 text-white p-2 w-full rounded hover:bg-green-600"
      >
        Register
      </button>

      <p v-if="errorMsg" class="text-red-500 text-sm mt-3 text-center">
        {{ errorMsg }}
      </p>

      <p class="text-center text-sm mt-4">
        Already have an account? 
        <router-link to="/login" class="text-blue-500 hover:underline">
          Login here
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  errorMsg.value = ''

  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match.'
    return
  }

  try {
    await axios.post('http://localhost:5000/api/register', {
      username: username.value,
      password: password.value
    })
    
    // Redirect to login page on successful registration
    router.push('/login?registered=true')
    
  } catch (err) {
    errorMsg.value =
      err.response?.data?.msg || 'Registration failed. Please try again.'
  }
}
</script>