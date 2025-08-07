<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow w-96 text-center">
      <h1 class="text-2xl font-bold mb-4">good buy</h1>
      <p class="mb-4">You are logged in as <strong>{{ username }}</strong></p>

      <button
        @click="handleLogout"
        class="bg-red-500 text-white p-2 w-full rounded hover:bg-red-600"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')

// ตรวจสอบว่า token มีหรือไม่ และดึงชื่อผู้ใช้ (จาก localStorage หรือ API)
onMounted(() => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login') // ถ้าไม่มี token ให้ redirect
  }

  // ตัวอย่าง: ถ้ามี username เก็บใน localStorage ด้วย
  const storedUser = localStorage.getItem('username')
  if (storedUser) {
    username.value = storedUser
  }
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  router.push('/login')
}
</script>