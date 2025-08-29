<template>
  <div class="min-h-screen bg-mookata flex items-center justify-center p-4">
    <div class="w-full max-w-sm bg-white/95 border border-amber-300 rounded-2xl shadow-lg p-6">
      <h1 class="text-2xl font-extrabold text-center mb-6 text-red-800">สมัครสมาชิก</h1>

      <!-- Error -->
      <p v-if="errorMsg" class="mb-4 bg-rose-50 border border-rose-300 text-rose-800 rounded-md p-3 text-sm">
        {{ errorMsg }}
      </p>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm mb-1 text-stone-700">ชื่อผู้ใช้</label>
          <input
            v-model.trim="username"
            placeholder="ตั้งชื่อผู้ใช้"
            class="w-full p-3 rounded-lg border border-amber-300 bg-white/90 placeholder-stone-400
                   focus:outline-none focus:ring-2 focus:ring-amber-500"
            autocomplete="username"
            @keyup.enter="handleRegister"
          />
        </div>

        <div>
          <label class="block text-sm mb-1 text-stone-700">รหัสผ่าน</label>
          <div class="relative">
            <input
              :type="showPw ? 'text' : 'password'"
              v-model="password"
              placeholder="อย่างน้อย 6 ตัวอักษร"
              class="w-full p-3 pr-12 rounded-lg border border-amber-300 bg-white/90 placeholder-stone-400
                     focus:outline-none focus:ring-2 focus:ring-amber-500"
              autocomplete="new-password"
              @keyup.enter="handleRegister"
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

        <div>
          <label class="block text-sm mb-1 text-stone-700">ยืนยันรหัสผ่าน</label>
          <div class="relative">
            <input
              :type="showPw2 ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="พิมพ์ซ้ำรหัสผ่าน"
              class="w-full p-3 pr-12 rounded-lg border border-amber-300 bg-white/90 placeholder-stone-400
                     focus:outline-none focus:ring-2 focus:ring-amber-500"
              autocomplete="new-password"
              @keyup.enter="handleRegister"
            />
            <button
              type="button"
              class="absolute inset-y-0 right-0 px-3 text-stone-500 hover:text-stone-700"
              @click="showPw2 = !showPw2"
              aria-label="toggle password visibility"
            >
              {{ showPw2 ? 'ซ่อน' : 'แสดง' }}
            </button>
          </div>
          <p v-if="password && confirmPassword && password !== confirmPassword"
             class="text-xs mt-1 text-rose-600">
            รหัสผ่านไม่ตรงกัน
          </p>
        </div>

        <button
          type="submit"
          class="w-full py-3 rounded-lg font-semibold text-white bg-amber-600 hover:bg-amber-700
                 disabled:opacity-60 disabled:cursor-not-allowed transition shadow"
          :disabled="loading"
        >
          <span v-if="!loading">สมัครสมาชิก</span>
          <span v-else>กำลังสมัครสมาชิก...</span>
        </button>
      </form>

      <div class="mt-4 text-center text-sm text-stone-600">
        มีบัญชีแล้ว?
        <RouterLink to="/login" class="text-red-700 hover:text-red-800 underline underline-offset-4">
          เข้าสู่ระบบ
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API = 'https://api-mukata.loeitech.org/api' // ปรับตามจริงได้

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const loading = ref(false)
const showPw = ref(false)
const showPw2 = ref(false)
const router = useRouter()

const handleRegister = async () => {
  if (loading.value) return
  errorMsg.value = ''

  // ตรวจสอบพื้นฐานฝั่ง client
  if (!username.value.trim()) {
    errorMsg.value = 'กรุณากรอกชื่อผู้ใช้'
    return
  }
  if (!password.value || password.value.length < 6) {
    errorMsg.value = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'รหัสผ่านไม่ตรงกัน'
    return
  }

  loading.value = true
  try {
    await axios.post(`${API}/register`, {
      username: username.value,
      password: password.value
    })
    // สมัครสำเร็จ -> ไปหน้า login พร้อมพารามิเตอร์แจ้งเตือน
    router.push('/login?registered=true')
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'สมัครสมาชิกไม่สำเร็จ กรุณาลองใหม่'
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
