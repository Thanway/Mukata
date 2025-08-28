<template>
  <div class="min-h-screen bg-mookata text-stone-900">
    <!-- Hero -->
    <section class="bg-gradient-to-b from-red-500 via-orange-500 to-orange-600 text-white">
      <div class="mx-auto max-w-6xl px-4 py-16 lg:py-20 text-center">
        <h1 class="text-4xl lg:text-5xl font-extrabold drop-shadow-md">
          หมูกระทะต้นตำรับแบบไทยแท้
        </h1>
        <p class="mt-4 text-lg lg:text-xl opacity-95">
          สัมผัสความลงตัวของปิ้งย่างสไตล์เกาหลีและชาบูแบบไทยใจกลางกรุงเทพฯ
        </p>
        <NuxtLink
          to="/reservations"
          class="inline-block mt-8 bg-yellow-400 text-red-900 font-semibold px-8 py-3 rounded-xl
                 hover:bg-yellow-300 transition shadow"
        >
          จองโต๊ะ
        </NuxtLink>
      </div>
    </section>

    <!-- Today Status -->
    <section class="py-10 lg:py-12">
      <div class="mx-auto max-w-6xl px-4">
        <h2 class="text-2xl lg:text-3xl font-extrabold text-center text-red-800">
          สถานะวันนี้
        </h2>

        <div v-if="loading" class="text-center text-stone-600 mt-8">กำลังโหลด...</div>
        <div v-else class="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Total -->
          <div class="bg-white rounded-2xl shadow-lg p-6 text-center">
            <div class="mx-auto w-10 h-10 rounded-full bg-blue-100 grid place-items-center">
              <span class="text-blue-600">★</span>
            </div>
            <div class="mt-3 text-2xl font-extrabold">{{ stats.totalTables }}</div>
            <p class="text-stone-500 mt-1">จำนวนโต๊ะทั้งหมด</p>
          </div>

          <!-- Available -->
          <div class="bg-white rounded-2xl shadow-lg p-6 text-center">
            <div class="mx-auto w-10 h-10 rounded-full bg-green-100 grid place-items-center">
              <span class="text-green-600">✓</span>
            </div>
            <div class="mt-3 text-2xl font-extrabold text-green-700">{{ stats.available }}</div>
            <p class="text-stone-500 mt-1">พร้อมให้บริการ</p>
          </div>

          <!-- Occupied -->
          <div class="bg-white rounded-2xl shadow-lg p-6 text-center">
            <div class="mx-auto w-10 h-10 rounded-full bg-rose-100 grid place-items-center">
              <span class="text-rose-600">–</span>
            </div>
            <div class="mt-3 text-2xl font-extrabold text-rose-700">{{ stats.occupied }}</div>
            <p class="text-stone-500 mt-1">กำลังใช้งาน</p>
          </div>

          <!-- Reserved -->
          <div class="bg-white rounded-2xl shadow-lg p-6 text-center">
            <div class="mx-auto w-10 h-10 rounded-full bg-amber-100 grid place-items-center">
              <span class="text-amber-600">★</span>
            </div>
            <div class="mt-3 text-2xl font-extrabold text-amber-700">{{ stats.reserved }}</div>
            <p class="text-stone-500 mt-1">จองแล้ว</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-10">
      <div class="mx-auto max-w-6xl px-4">
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-white rounded-2xl shadow p-6">
            <h3 class="text-lg font-bold text-red-800">วัตถุดิบคัดพิเศษ</h3>
            <p class="mt-2 text-stone-600">
              หมู เนื้อ ไก่ และผักสดส่งตรงทุกวัน น้ำจิ้มสูตรลับสไตล์ไทยแท้
            </p>
          </div>
          <div class="bg-white rounded-2xl shadow p-6">
            <h3 class="text-lg font-bold text-red-800">บรรยากาศอบอุ่น</h3>
            <p class="mt-2 text-stone-600">
              ที่นั่งกว้าง โล่ง โปร่งสบาย เหมาะกับครอบครัวและกลุ่มเพื่อน
            </p>
          </div>
          <div class="bg-white rounded-2xl shadow p-6">
            <h3 class="text-lg font-bold text-red-800">จองโต๊ะออนไลน์</h3>
            <p class="mt-2 text-stone-600">
              จองง่าย รอไม่นาน เช็คสถานะโต๊ะได้แบบเรียลไทม์
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA strip -->
    <section class="py-10">
      <div class="mx-auto max-w-6xl px-4">
        <div class="bg-gradient-to-r from-amber-400 to-orange-500 text-white rounded-2xl p-8 text-center shadow">
          <h3 class="text-2xl font-extrabold">พร้อมอร่อยแล้วหรือยัง?</h3>
          <p class="mt-2 opacity-95">กดจองโต๊ะ แล้วมาฟินกับหมูกระทะร้อน ๆ กันเลย!</p>
          <NuxtLink
            to="/reservations"
            class="inline-block mt-5 bg-white text-red-700 font-semibold px-6 py-2 rounded-xl hover:bg-stone-100 transition"
          >
            จองโต๊ะตอนนี้
          </NuxtLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const API = 'http://localhost:5000/api'

const loading = ref(true)
const stats = ref({
  totalTables: 0,
  available: 0,
  occupied: 0,
  reserved: 0
})

// ✅ ดึง token มาใช้
const authHeaders = () => {
  const token = localStorage.getItem('token')
  return { Authorization: `Bearer ${token}` }
}

const fetchStats = async () => {
  loading.value = true
  try {
    const [tRes, rRes] = await Promise.all([
      axios.get(`${API}/tables`, { headers: authHeaders() }),
      axios.get(`${API}/reservations`, { headers: authHeaders() })
    ])

    const tables = tRes.data || []
    const reservations = rRes.data || []

    stats.value.totalTables = tables.length
    stats.value.available = tables.filter(t => t.isActive).length

    // นับสถานะจาก reservations
    const today = new Date().toISOString().slice(0, 10)
    const todayRes = reservations.filter(r => (r.reserveStart || '').slice(0, 10) === today)

    stats.value.reserved  = todayRes.filter(r => (r.status || '').toLowerCase() === 'reserved').length
    stats.value.occupied  = todayRes.filter(r => (r.status || '').toLowerCase() === 'seated').length
  } catch (e) {
    console.error('Fetch Home stats failed:', e)
  } finally {
    loading.value = false
  }
}


onMounted(fetchStats)
</script>
