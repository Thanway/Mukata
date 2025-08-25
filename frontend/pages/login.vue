<template>
  <div class="min-h-screen bg-mookata flex items-center justify-center p-4">
    <div class="w-full max-w-sm bg-white/95 border border-amber-300 rounded-2xl shadow-lg p-6">
      <h1 class="text-2xl font-extrabold text-center mb-6 text-red-800">เข้าสู่ระบบ</h1>

      <!-- Error -->
      <p v-if="errorMsg" class="mb-4 bg-rose-50 border border-rose-300 text-rose-800 rounded-md p-3 text-sm">
        {{ errorMsg }}
      </p>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm mb-1 text-stone-700">ชื่อผู้ใช้</label>
          <input
            v-model.trim="username"
            placeholder="Username"
            class="w-full p-3 rounded-lg border border-amber-300 bg-white/90 placeholder-stone-400
                   focus:outline-none focus:ring-2 focus:ring-amber-500"
            autocomplete="username"
          />
        </div>

        <div>
          <label class="block text-sm mb-1 text-stone-700">รหัสผ่าน</label>
          <div class="relative">
            <input
              :type="showPw ? 'text' : 'password'"
              v-model="password"
              placeholder="Password"
              class="w-full p-3 pr-12 rounded-lg border border-amber-300 bg-white/90 placeholder-stone-400
                     focus:outline-none focus:ring-2 focus:ring-amber-500"
              autocomplete="current-password"
              @keyup.enter="handleLogin"
            />
            <button
              type="button"
              class="absolute inset-y-0 right-0 px-3 text-stone-500 hover:text-stone-700"
              @click="showPw = !showPw"
              aria-label="toggle password visibility"
            >
              {{ showPw ? 'ซ่อน' : 'แสดง' }}
            </button>
          </div>
        </div>

        <button
          type="submit"
          class="w-full py-3 rounded-lg font-semibold text-white bg-amber-600 hover:bg-amber-700
                 disabled:opacity-60 disabled:cursor-not-allowed transition shadow"
          :disabled="loading"
        >
          <span v-if="!loading">เข้าสู่ระบบ</span>
          <span v-else>กำลังเข้าสู่ระบบ...</span>
        </button>
      </form>

      <div class="mt-4 text-center text-sm text-stone-600">
        ยังไม่มีบัญชี?
        <RouterLink to="/register" class="text-red-700 hover:text-red-800 underline underline-offset-4">
          สมัครสมาชิก
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API = 'http://localhost:5000/api' // ปรับตามจริงถ้าจำเป็น

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)
const showPw = ref(false)
const router = useRouter()

const handleLogin = async () => {
  if (loading.value) return
  errorMsg.value = ''
  loading.value = true
  try {
    const res = await axios.post(`${API}/login`, {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.access_token)
    router.push('/dashboard')
  } catch (err) {
    errorMsg.value = err?.response?.data?.msg || 'เข้าสู่ระบบไม่สำเร็จ กรุณาลองใหม่'
  } finally {
    loading.value = false
  }
}
</script>

<style>
/* พื้นหลังครีมโทนร้านหมูกระทะ */
.bg-mookata { background-color: #fdf3e7; }
/* ถ้าอยากนวลขึ้น: #fff7ec หรือ #fff4e6 */
</style>
