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
        จัดการโต๊ะ
      </h1>

      <!-- ฟอร์มเพิ่มโต๊ะ -->
      <div class="bg-white/80 rounded-lg p-5 border border-cyan-600 shadow mb-8">
        <h2 class="text-xl font-bold mb-4">เพิ่มโต๊ะ</h2>
        <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
          <input
            v-model.trim="form.number"
            placeholder="เลขโต๊ะ (เช่น A1, 12, VIP-3)"
            class="bg-transparent border border-cyan-400 p-3 rounded-md md:col-span-3 placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500 shadow-sm text-black"
          />
          <input
            v-model.number="form.seats"
            type="number" min="1"
            placeholder="จำนวนที่นั่ง"
            class="bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500 shadow-sm text-black"
          />
          <button
            @click="createTable"
            class="bg-cyan-600 hover:bg-cyan-700 text-black font-semibold px-5 rounded-md shadow-md transition duration-300"
          >
            เพิ่มโต๊ะ
          </button>
        </div>
        <p class="text-sm mt-2 opacity-70">* ต้องกรอกเลขโต๊ะอย่างน้อย 1 ค่า</p>
      </div>

      <!-- แถบค้นหา + สรุป -->
      <div class="flex flex-col md:flex-row md:items-center gap-3 mb-5">
        <input
          v-model="q"
          placeholder="ค้นหาเลขโต๊ะ..."
          class="bg-transparent border border-cyan-300 p-3 rounded-md flex-1 placeholder-cyan-800 focus:outline-cyan-400 focus:ring-2 focus:ring-cyan-600 shadow-inner text-black"
        />
        <div class="text-sm opacity-80">
          โต๊ะทั้งหมด: <b>{{ tables.length }}</b> |
          ใช้งานได้: <b>{{ tables.filter(t => t.isActive).length }}</b>
        </div>
      </div>

      <!-- รายการโต๊ะ -->
      <div v-if="loading" class="text-center py-10 opacity-70">กำลังโหลด...</div>

      <div v-else class="rounded-lg overflow-hidden border border-cyan-600 bg-white/80 shadow">
        <table class="w-full text-left">
          <thead class="bg-cyan-50">
            <tr>
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
              class="border-t border-cyan-100 hover:bg-cyan-50/50 transition"
            >
              <td class="p-3">
                <template v-if="editId === t.id">
                  <input v-model.trim="edit.number" class="border p-1 rounded w-32" />
                </template>
                <template v-else>
                  <span class="font-semibold">{{ t.number }}</span>
                </template>
              </td>
              <td class="p-3">
                <template v-if="editId === t.id">
                  <input v-model.number="edit.seats" type="number" min="1" class="border p-1 rounded w-24" />
                </template>
                <template v-else>
                  {{ t.seats }}
                </template>
              </td>
              <td class="p-3">
                <span
                  class="px-2 py-1 text-xs rounded border"
                  :class="t.isActive ? 'bg-green-100 border-green-400' : 'bg-gray-100 border-gray-400'"
                >
                  {{ t.isActive ? 'ใช้งานได้' : 'ปิดใช้งาน' }}
                </span>
              </td>
              <td class="p-3">
                <div class="flex justify-end gap-2">
                  <button
                    v-if="editId !== t.id"
                    class="px-3 py-1 rounded bg-amber-500 hover:bg-amber-600 text-white"
                    @click="startEdit(t)"
                  >
                    แก้ไข
                  </button>
                  <button
                    v-else
                    class="px-3 py-1 rounded bg-blue-600 hover:bg-blue-700 text-white"
                    @click="saveEdit(t.id)"
                  >
                    บันทึก
                  </button>
                  <button
                    v-if="editId === t.id"
                    class="px-3 py-1 rounded bg-gray-500 hover:bg-gray-600 text-white"
                    @click="cancelEdit"
                  >
                    ยกเลิก
                  </button>
                  <button
                    class="px-3 py-1 rounded"
                    :class="t.isActive ? 'bg-yellow-500 hover:bg-yellow-600 text-white' : 'bg-green-600 hover:bg-green-700 text-white'"
                    @click="toggleActive(t)"
                  >
                    {{ t.isActive ? 'ปิดใช้งาน' : 'เปิดใช้งาน' }}
                  </button>
                  <button
                    class="px-3 py-1 rounded bg-red-600 hover:bg-red-700 text-white"
                    @click="removeTable(t.id)"
                  >
                    ลบ
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!filtered.length">
              <td colspan="4" class="p-5 text-center opacity-60">ไม่พบโต๊ะ</td>
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
    if (idx !== -1) {
      tables.value[idx] = { ...tables.value[idx], ...edit.value }
    }
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
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.font-ocean { font-family: 'Pacifico', cursive; }
.bg-ocean {
  background-image: url('https://images.unsplash.com/photo-1581322336686-c5a8f1b1d4be?auto=format&fit=crop&w=1500&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
