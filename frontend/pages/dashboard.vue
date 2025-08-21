<template>
  <div class="min-h-screen bg-ocean text-black font-ocean">
    <!-- Hero -->
    <div class="w-screen max-h-[320px] overflow-hidden border-b border-cyan-500">
      <img
        src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80"
        alt="Underwater"
        class="w-full h-full object-cover"
        style="height: 320px;"
      />
    </div>

    <!-- Container -->
    <div class="p-6 max-w-5xl mx-auto">
      <h1 class="text-4xl font-extrabold mb-8 text-center tracking-wide drop-shadow-lg">
        แดชบอร์ดการจองโต๊ะ
      </h1>

      <!-- สรุปสถิติ -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div class="rounded-lg p-5 bg-gradient-to-br from-cyan-100 to-teal-100 border border-cyan-600 shadow">
          <p class="text-sm opacity-70">โต๊ะทั้งหมด</p>
          <p class="text-3xl font-extrabold">{{ stats.totalTables }}</p>
        </div>
        <div class="rounded-lg p-5 bg-gradient-to-br from-cyan-100 to-teal-100 border border-cyan-600 shadow">
          <p class="text-sm opacity-70">โต๊ะใช้งานได้</p>
          <p class="text-3xl font-extrabold">{{ stats.activeTables }}</p>
        </div>
        <div class="rounded-lg p-5 bg-gradient-to-br from-cyan-100 to-teal-100 border border-cyan-600 shadow">
          <p class="text-sm opacity-70">การจองทั้งหมด</p>
          <p class="text-3xl font-extrabold">{{ stats.totalReservations }}</p>
        </div>
        <div class="rounded-lg p-5 bg-gradient-to-br from-cyan-100 to-teal-100 border border-cyan-600 shadow">
          <p class="text-sm opacity-70">จองวันนี้</p>
          <p class="text-3xl font-extrabold">{{ stats.todayReservations }}</p>
        </div>
      </div>

      <!-- ค้นหารายการจอง -->
      <div class="flex gap-3 mb-6">
        <input
          v-model="searchText"
          placeholder="ค้นหา: ชื่อลูกค้า / เบอร์ / โต๊ะ / สถานะ"
          class="bg-transparent border border-cyan-300 p-3 rounded-md flex-1 placeholder-cyan-800 focus:outline-cyan-400 focus:ring-2 focus:ring-cyan-600 shadow-inner text-black"
        />
        <button
          @click="clearSearch"
          class="bg-cyan-300 hover:bg-cyan-400 text-black font-semibold px-5 rounded-md shadow transition duration-300"
        >
          ล้าง
        </button>
      </div>

      <!-- รายการจองล่าสุด -->
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-2xl font-bold">การจองล่าสุด</h2>
        <NuxtLink to="/reservations" class="text-cyan-700 underline">ดูทั้งหมด →</NuxtLink>
      </div>

      <div v-if="loading" class="text-center py-10 opacity-70">กำลังโหลด...</div>

      <div v-else class="space-y-4">
        <div
          v-for="r in filteredReservations.slice(0, 10)"
          :key="r.id"
          class="bg-gradient-to-r from-cyan-100 via-blue-200 to-teal-100 rounded-lg p-5 shadow border border-cyan-600"
        >
          <div class="flex justify-between items-start">
            <div>
              <p class="font-bold text-lg">
                โต๊ะ {{ r.table?.number ?? '-' }} • {{ r.customerName ?? '-' }}
              </p>
              <p class="text-sm">เบอร์: {{ r.phone || '-' }} • จำนวนคน: {{ r.partySize || '-' }}</p>
              <p class="text-sm">
                เวลา: {{ fmt(r.reserveStart) }} — {{ fmt(r.reserveEnd) }}
              </p>
              <p class="text-sm">สถานะ: <span class="font-semibold">{{ r.status }}</span></p>
            </div>
            <div class="flex gap-2">
              <button
                class="px-3 py-1 rounded bg-yellow-500 hover:bg-yellow-600 text-white"
                @click="cancelReservation(r.id)"
                :disabled="r.status === 'cancelled' || r.status === 'completed'"
              >
                ยกเลิก
              </button>
              <button
                class="px-3 py-1 rounded bg-red-600 hover:bg-red-700 text-white"
                @click="deleteReservation(r.id)"
              >
                ลบ
              </button>
            </div>
          </div>
        </div>

        <div v-if="!filteredReservations.length" class="opacity-60 italic py-10 text-center">
          ไม่พบรายการที่ตรงกับการค้นหา
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const API = 'http://localhost:5000/api'

const stats = ref({
  totalTables: 0,
  activeTables: 0,
  totalReservations: 0,
  todayReservations: 0
})

const reservations = ref([])
const searchText = ref('')
const loading = ref(false)

const authHeaders = () => {
  const token = localStorage.getItem('token')
  return { Authorization: `Bearer ${token}` }
}

const fetchData = async () => {
  loading.value = true
  try {
    const [tRes, rRes] = await Promise.all([
      axios.get(`${API}/tables`, { headers: authHeaders() }),
      axios.get(`${API}/reservations`, { headers: authHeaders() })
    ])
    const tables = tRes.data || []
    const resvs = rRes.data || []

    reservations.value = resvs

    stats.value.totalTables = tables.length
    stats.value.activeTables = tables.filter(t => t.isActive).length
    stats.value.totalReservations = resvs.length

    const today = new Date().toISOString().slice(0, 10)
    stats.value.todayReservations = resvs.filter(x =>
      (x.reserveStart || '').slice(0, 10) === today
    ).length
  } catch (e) {
    console.error('Fetch dashboard failed:', e)
  } finally {
    loading.value = false
  }
}

const fmt = (iso) => {
  if (!iso) return '-'
  try {
    const d = new Date(iso)
    const pad = (n) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
  } catch { return iso }
}

const clearSearch = () => { searchText.value = '' }

const filteredReservations = computed(() => {
  const q = (searchText.value || '').trim().toLowerCase()
  if (!q) return reservations.value
  return reservations.value.filter(r => {
    const name = (r.customerName || '').toLowerCase()
    const ph = (r.phone || '').toLowerCase()
    const tableNo = String(r.table?.number || '').toLowerCase()
    const st = (r.status || '').toLowerCase()
    return name.includes(q) || ph.includes(q) || tableNo.includes(q) || st.includes(q)
  })
})

const cancelReservation = async (id) => {
  try {
    await axios.patch(`${API}/reservations/${id}/cancel`, {}, { headers: authHeaders() })
    const target = reservations.value.find(x => x.id === id)
    if (target) target.status = 'cancelled'
  } catch (e) {
    alert(e?.response?.data?.msg || 'ยกเลิกไม่สำเร็จ')
  }
}

const deleteReservation = async (id) => {
  const keep = [...reservations.value]
  reservations.value = reservations.value.filter(x => x.id !== id)
  try {
    await axios.delete(`${API}/reservations/${id}`, { headers: authHeaders() })
  } catch (e) {
    reservations.value = keep
    alert(e?.response?.data?.msg || 'ลบไม่สำเร็จ')
  }
}

onMounted(fetchData)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.font-ocean { font-family: 'Pacifico', cursive; }
.bg-ocean {
  background-image: url('https://images.unsplash.com/photo-1581322336686-c5a8f1b1d4be?auto=format&fit=crop&w=1500&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
