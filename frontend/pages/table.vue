<template>
  <div class="min-h-screen bg-mookata text-stone-900">
    <!-- Hero (แถบหัวอุ่นๆ) -->
    <div class="w-screen max-h-[320px] overflow-hidden border-b border-amber-300">
      <div class="h-[320px] bg-gradient-to-r from-amber-100 via-orange-100 to-rose-100 flex items-center justify-center">
        <h1 class="text-4xl font-extrabold tracking-wide drop-shadow-sm text-red-800">จัดการโต๊ะ</h1>
      </div>
    </div>

    <!-- Container -->
    <div class="p-6 max-w-5xl mx-auto">

      <!-- ฟอร์มเพิ่มโต๊ะ -->
      <div class="bg-white/90 rounded-xl p-5 border border-amber-300 shadow mb-8">
        <h2 class="text-xl font-bold mb-4 text-stone-800">เพิ่มโต๊ะ</h2>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
          <input
            v-model.trim="form.number"
            placeholder="เลขโต๊ะ (เช่น A1, 12, VIP-3)"
            class="bg-white/80 border border-amber-300 p-3 rounded-lg md:col-span-3 placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
          />
          <input
            v-model.number="form.seats"
            type="number" min="1"
            placeholder="จำนวนที่นั่ง"
            class="bg-white/80 border border-amber-300 p-3 rounded-lg placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
          />
          <button
            @click="createTable"
            class="bg-amber-600 hover:bg-amber-700 text-white font-semibold px-5 rounded-lg shadow-sm transition"
          >
            เพิ่มโต๊ะ
          </button>
        </div>
        <p class="text-sm mt-2 text-stone-500">* ต้องกรอกเลขโต๊ะอย่างน้อย 1 ค่า</p>
      </div>

      <!-- แถบค้นหา + สรุป -->
      <div class="flex flex-col md:flex-row md:items-center gap-3 mb-5">
        <input
          v-model="q"
          placeholder="ค้นหาเลขโต๊ะ..."
          class="bg-white/80 border border-amber-300 p-3 rounded-lg flex-1 placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500 shadow-sm"
        />
        <div class="text-sm text-stone-600">
          โต๊ะทั้งหมด: <b>{{ tables.length }}</b> |
          ใช้งานได้: <b>{{ tables.filter(t => t.isActive).length }}</b>
        </div>
      </div>

      <!-- รายการโต๊ะ -->
      <div v-if="loading" class="text-center py-10 text-stone-500">กำลังโหลด...</div>

      <div v-else class="rounded-xl overflow-hidden border border-amber-300 bg-white/90 shadow-sm">
        <table class="w-full text-left">
          <thead class="bg-amber-50">
            <tr class="text-stone-700">
              <th class="p-3">เลขโต๊ะ</th>
              <th class="p-3">ที่นั่ง</th>
              <th class="p-3">สถานะ</th>
              <th class="p-3 text-right">การจัดการ</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="t in filtered"
              :key="t.id"
              class="border-t border-amber-100 hover:bg-amber-50/60 transition"
            >
              <td class="p-3">
                <template v-if="editId === t.id">
                  <input v-model.trim="edit.number" class="border border-amber-300 p-1 rounded w-32 focus:outline-none focus:ring-2 focus:ring-amber-400" />
                </template>
                <template v-else>
                  <span class="font-semibold">{{ t.number }}</span>
                </template>
              </td>
              <td class="p-3">
                <template v-if="editId === t.id">
                  <input v-model.number="edit.seats" type="number" min="1" class="border border-amber-300 p-1 rounded w-24 focus:outline-none focus:ring-2 focus:ring-amber-400" />
                </template>
                <template v-else>
                  {{ t.seats }}
                </template>
              </td>
              <td class="p-3">
                <span
                  class="px-2 py-1 text-xs rounded-full border font-medium"
                  :class="t.isActive ? 'bg-green-100 text-green-700 border-green-300' : 'bg-stone-100 text-stone-700 border-stone-300'"
                >
                  {{ t.isActive ? 'ใช้งานได้' : 'ปิดใช้งาน' }}
                </span>
              </td>
              <td class="p-3">
                <div class="flex justify-end gap-2">
                  <button
                    v-if="editId !== t.id"
                    class="px-3 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 text-white"
                    @click="startEdit(t)"
                  >
                    แก้ไข
                  </button>
                  <button
                    v-else
                    class="px-3 py-1 rounded-lg bg-orange-600 hover:bg-orange-700 text-white"
                    @click="saveEdit(t.id)"
                  >
                    บันทึก
                  </button>
                  <button
                    v-if="editId === t.id"
                    class="px-3 py-1 rounded-lg bg-stone-500 hover:bg-stone-600 text-white"
                    @click="cancelEdit"
                  >
                    ยกเลิก
                  </button>
                  <button
                    class="px-3 py-1 rounded-lg text-white"
                    :class="t.isActive ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-green-600 hover:bg-green-700'"
                    @click="toggleActive(t)"
                  >
                    {{ t.isActive ? 'ปิดใช้งาน' : 'เปิดใช้งาน' }}
                  </button>
                  <button
                    class="px-3 py-1 rounded-lg bg-red-700 hover:bg-red-800 text-white"
                    @click="removeTable(t.id)"
                  >
                    ลบ
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!filtered.length">
              <td colspan="4" class="p-5 text-center text-stone-500">ไม่พบโต๊ะ</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'

const API = 'http://localhost:5000/api'

const form = ref({ number: '', seats: 4 })
const tables = ref([])
const q = ref('')
const loading = ref(false)

const editId = ref(null)
const edit = ref({ number: '', seats: 4 })

const authHeaders = () => {
  const token = localStorage.getItem('token')
  return { Authorization: `Bearer ${token}` }
}

const fetchTables = async () => {
  loading.value = true
  try {
    const { data } = await axios.get(`${API}/tables`, { headers: authHeaders() })
    tables.value = data || []
  } catch (e) {
    console.error(e)
    alert(e?.response?.data?.msg || 'โหลดรายการโต๊ะไม่สำเร็จ')
  } finally {
    loading.value = false
  }
}

const createTable = async () => {
  if (!form.value.number?.trim()) {
    return alert('กรุณากรอกเลขโต๊ะ')
  }
  try {
    const { data } = await axios.post(`${API}/tables`, form.value, { headers: authHeaders() })
    tables.value.unshift(data)
    form.value.number = ''
    form.value.seats = 4
  } catch (e) {
    alert(e?.response?.data?.msg || 'เพิ่มโต๊ะไม่สำเร็จ')
  }
}

const startEdit = (t) => {
  editId.value = t.id
  edit.value = { number: t.number, seats: t.seats }
}
const cancelEdit = () => {
  editId.value = null
  edit.value = { number: '', seats: 4 }
}
const saveEdit = async (id) => {
  try {
    await axios.patch(`${API}/tables/${id}`, edit.value, { headers: authHeaders() })
    const idx = tables.value.findIndex(x => x.id === id)
    if (idx !== -1) tables.value[idx] = { ...tables.value[idx], ...edit.value }
    cancelEdit()
  } catch (e) {
    alert(e?.response?.data?.msg || 'บันทึกไม่สำเร็จ')
  }
}

const toggleActive = async (t) => {
  try {
    const path = t.isActive ? 'deactivate' : 'activate'
    await axios.patch(`${API}/tables/${t.id}/${path}`, {}, { headers: authHeaders() })
    t.isActive = !t.isActive
  } catch (e) {
    alert(e?.response?.data?.msg || 'เปลี่ยนสถานะไม่สำเร็จ')
  }
}

const removeTable = async (id) => {
  if (!confirm('ยืนยันลบโต๊ะนี้?')) return
  const keep = [...tables.value]
  tables.value = tables.value.filter(x => x.id !== id)
  try {
    await axios.delete(`${API}/tables/${id}`, { headers: authHeaders() })
  } catch (e) {
    tables.value = keep
    alert(e?.response?.data?.msg || 'ลบไม่สำเร็จ')
  }
}

const filtered = computed(() => {
  const s = (q.value || '').toLowerCase().trim()
  if (!s) return tables.value
  return tables.value.filter(t => (t.number || '').toLowerCase().includes(s))
})

onMounted(fetchTables)
</script>

<style>
/* พื้นหลังครีม/เบจโทนร้านหมูกระทะ */
.bg-mookata {
  background-color: #fdf3e7; /* ลอง #fff7ec หรือ #fff4e6 ถ้าอยากสว่าง/นวลขึ้น */
}

/* (ตัวเลือก) ฟอนต์ไทยอ่านง่าย
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;600;800&display=swap');
:root { --thai: 'Noto Sans Thai', ui-sans-serif, system-ui; }
* { font-family: var(--thai); } */
</style>
