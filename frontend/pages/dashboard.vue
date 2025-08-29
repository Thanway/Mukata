<template>
  <div class="min-h-screen bg-mookata text-stone-900">
    <!-- Container -->
    <div class="p-6 max-w-5xl mx-auto">
      <h1 class="text-4xl font-extrabold mb-8 text-center tracking-wide drop-shadow-sm text-red-800">
        Table Status
      </h1>

      <!-- สรุปสถิติ -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <!-- โต๊ะทั้งหมด -->
        <div class="rounded-2xl p-5 bg-orange-100/80 border border-orange-300 shadow-sm">
          <p class="text-sm text-stone-600">โต๊ะทั้งหมด</p>
          <p class="text-3xl font-extrabold text-orange-800">{{ stats.totalTables }}</p>
        </div>

        <!-- โต๊ะใช้งานได้ -->
        <div class="rounded-2xl p-5 bg-green-100/80 border border-green-300 shadow-sm">
          <p class="text-sm text-stone-600">โต๊ะใช้งานได้</p>
          <p class="text-3xl font-extrabold text-green-700">{{ stats.activeTables }}</p>
        </div>

        <!-- การจองทั้งหมด -->
        <div class="rounded-2xl p-5 bg-rose-100/80 border border-rose-300 shadow-sm">
          <p class="text-sm text-stone-600">การจองทั้งหมด</p>
          <p class="text-3xl font-extrabold text-rose-700">{{ stats.totalReservations }}</p>
        </div>

        <!-- จองวันนี้ -->
        <div class="rounded-2xl p-5 bg-amber-100/80 border border-amber-300 shadow-sm">
          <p class="text-sm text-stone-600">จองวันนี้</p>
          <p class="text-3xl font-extrabold text-amber-700">{{ stats.todayReservations }}</p>
        </div>
      </div>

      <!-- ค้นหารายการจอง -->
      <div class="flex gap-3 mb-6">
        <input
          v-model="searchText"
          placeholder="ค้นหา: ชื่อลูกค้า / เบอร์ / โต๊ะ / สถานะ"
          class="bg-white/70 border border-amber-300 p-3 rounded-xl flex-1 placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
        />
        <button
          @click="clearSearch"
          class="bg-amber-500 hover:bg-amber-600 text-white font-semibold px-5 py-2 rounded-xl shadow-sm transition"
        >
          ล้าง
        </button>
      </div>

      <!-- รายการจองล่าสุด -->
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-2xl font-bold text-stone-800">การจองล่าสุด</h2>
        <NuxtLink to="/reservations" class="text-red-700 hover:text-red-800 underline underline-offset-4">ดูทั้งหมด →</NuxtLink>
      </div>

      <div v-if="loading" class="text-center py-10 text-stone-500">กำลังโหลด...</div>

      <div v-else class="space-y-4">
        <div
          v-for="r in filteredReservations.slice(0, 10)"
          :key="r.id"
          class="bg-gradient-to-r from-amber-50 via-orange-50 to-rose-50 rounded-2xl p-5 shadow-sm border border-amber-200"
        >
          <div class="flex justify-between items-start">
            <div>
              <p class="font-bold text-lg text-stone-900">
                โต๊ะ {{ r.table?.number ?? '-' }} • {{ r.customerName ?? '-' }}
              </p>
              <p class="text-sm text-stone-600">เบอร์: {{ r.phone || '-' }} • จำนวนคน: {{ r.partySize || '-' }}</p>
              <p class="text-sm text-stone-600">
                เวลา: {{ fmt(r.reserveStart) }} — {{ fmt(r.reserveEnd) }}
              </p>
              <p class="text-sm text-stone-700">
                สถานะ:
                <span
                  class="font-semibold px-2 py-0.5 rounded-full"
                  :class="{
                    'bg-green-100 text-green-700': r.status === 'available',
                    'bg-rose-100 text-rose-700': r.status === 'occupied',
                    'bg-amber-100 text-amber-700': r.status === 'reserved',
                    'bg-stone-100 text-stone-700': r.status === 'cleaning',
                    'bg-stone-200 text-stone-700': !['available','occupied','reserved','cleaning'].includes((r.status||'').toLowerCase())
                  }"
                >
                  {{ r.status }}
                </span>
              </p>
            </div>
            <div class="flex gap-2">
              <button
                class="px-3 py-1 rounded-lg bg-yellow-600 hover:bg-yellow-700 text-white disabled:opacity-50"
                @click="cancelReservation(r.id)"
                :disabled="r.status === 'cancelled' || r.status === 'completed'"
              >
                ยกเลิก
              </button>
              <button
                class="px-3 py-1 rounded-lg bg-red-700 hover:bg-red-800 text-white"
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

const API = 'https://api-mukata.loeitech.org/api'

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
/* พื้นหลังครีม/เบจแบบภาพตัวอย่าง */
.bg-mookata {
  background-color: #fdf3e7; /* ครีมอุ่น */
  /* ถ้าอยากให้นวลขึ้นอีก ลอง #fff7ec หรือ #fff4e6 */
}

/* (ตัวเลือก) ฟอนต์อบอุ่นนิดๆ
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;600;800&display=swap');
:root { --thai: 'Noto Sans Thai', ui-sans-serif, system-ui; }
* { font-family: var(--thai); } */
</style>
