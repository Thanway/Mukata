<template>
  <div class="min-h-screen bg-mookata text-stone-900">
    <!-- Container -->
    <div class="p-6 max-w-3xl mx-auto">
      <h1 class="text-4xl font-extrabold mb-8 text-center tracking-wide drop-shadow-sm text-red-800">
        ฟอร์มจองโต๊ะ
      </h1>

      <!-- Error banner -->
      <div v-if="error" class="mb-6 bg-rose-50 border border-rose-300 text-rose-800 rounded-lg p-4">
        <p class="font-bold">เกิดข้อผิดพลาด</p>
        <p class="text-sm whitespace-pre-wrap">{{ error }}</p>
      </div>

      <!-- Form -->
      <div class="bg-white/95 rounded-xl p-6 shadow border border-amber-300">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Name -->
          <div>
            <label class="block text-sm mb-1">ชื่อลูกค้า *</label>
            <input
              v-model.trim="form.customerName"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500"
              placeholder="เช่น สมชาย ใจดี"
            />
          </div>

          <!-- Phone -->
          <div>
            <label class="block text-sm mb-1">เบอร์โทร</label>
            <input
              v-model.trim="form.phone"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500"
              placeholder="เช่น 0812345678"
            />
          </div>

          <!-- Party size -->
          <div>
            <label class="block text-sm mb-1">จำนวนคน *</label>
            <input
              v-model.number="form.partySize"
              type="number" min="1"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-amber-500"
              placeholder="เช่น 4"
            />
          </div>

          <!-- Table -->
          <div>
            <label class="block text-sm mb-1">โต๊ะ *</label>
            <select
              v-model="form.tableId"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
              <option value="" disabled>-- เลือกโต๊ะ --</option>
              <option
                v-for="t in tables"
                :key="t.id"
                :value="t.id"
                :disabled="!t.isActive"
              >
                {{ t.number }} (ที่นั่ง {{ t.seats }}) {{ !t.isActive ? ' - ปิดใช้งาน' : '' }}
              </option>
            </select>
          </div>

          <!-- Reserve start -->
          <div>
            <label class="block text-sm mb-1">เวลาเริ่ม *</label>
            <input
              v-model="form.reserveStart"
              type="datetime-local"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>

          <!-- Reserve end -->
          <div>
            <label class="block text-sm mb-1">เวลาสิ้นสุด *</label>
            <input
              v-model="form.reserveEnd"
              type="datetime-local"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
            <p class="text-xs mt-1 text-stone-500">
              * ไม่กรอกได้ ถ้าจะให้ระบบกำหนดอัตโนมัติ +120 นาที
            </p>
          </div>

          <!-- Status -->
          <div class="md:col-span-2">
            <label class="block text-sm mb-1">สถานะ</label>
            <select
              v-model="form.status"
              class="w-full bg-transparent border border-amber-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            >
              <option value="reserved">reserved</option>
              <option value="seated">seated</option>
              <option value="completed">completed</option>
              <option value="cancelled">cancelled</option>
            </select>
          </div>
        </div>

        <!-- Buttons -->
        <div class="mt-6 flex gap-3">
          <button
            @click="submit"
            class="bg-amber-600 hover:bg-amber-700 text-white font-semibold px-6 py-3 rounded-lg shadow-sm transition"
            :disabled="submitting"
          >
            {{ submitting ? 'กำลังบันทึก...' : 'บันทึกการจอง' }}
          </button>
          <button
            @click="resetForm"
            class="bg-stone-200 hover:bg-stone-300 text-stone-800 font-semibold px-6 py-3 rounded-lg shadow-sm transition"
            :disabled="submitting"
          >
            ล้างฟอร์ม
          </button>
        </div>
      </div>

      <!-- Success mini banner -->
      <div v-if="successMsg" class="mt-6 bg-green-50 border border-green-300 text-green-800 rounded-lg p-4">
        {{ successMsg }}
      </div>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const API = 'http://localhost:5000/api'

const tables = ref([])
const error = ref('')
const successMsg = ref('')
const submitting = ref(false)

const form = ref({
  customerName: '',
  phone: '',
  partySize: 1,
  tableId: '',
  reserveStart: '',
  reserveEnd: '',
  status: 'reserved'
})

const headers = () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const fetchTables = async () => {
  error.value = ''
  try {
    const { data } = await axios.get(`${API}/tables`, { headers: headers() })
    tables.value = data || []
  } catch (e) {
    console.error(e)
    error.value = e?.response?.data?.msg || 'โหลดรายการโต๊ะไม่สำเร็จ'
  }
}

const validate = () => {
  if (!form.value.customerName.trim()) return 'กรุณากรอกชื่อลูกค้า'
  if (!form.value.partySize || form.value.partySize < 1) return 'จำนวนคนต้องมากกว่าหรือเท่ากับ 1'
  if (!form.value.tableId) return 'กรุณาเลือกโต๊ะ'
  if (!form.value.reserveStart) return 'กรุณาเลือกเวลาเริ่ม'
  // reserveEnd ไม่บังคับ — ถ้าไม่กรอก backend จะ +120 นาทีให้
  return ''
}

const normalizeDatetimeLocal = (s) => {
  // input type="datetime-local" คืน "YYYY-MM-DDTHH:MM"
  // ส่งไป backend ได้เลย หรือจะแปลงเป็น ISO ก็ได้ (backend ของคุณรองรับทั้งสอง)
  return s || null
}

const submit = async () => {
  error.value = ''
  successMsg.value = ''
  const v = validate()
  if (v) { error.value = v; return }

  submitting.value = true
  try {
    const payload = {
      customerName: form.value.customerName,
      phone: form.value.phone || '',
      partySize: Number(form.value.partySize),
      tableId: form.value.tableId,
      reserveStart: normalizeDatetimeLocal(form.value.reserveStart),
      // ถ้าไม่กรอก reserveEnd จะให้ backend คำนวนเอง (+120 นาที)
      ...(form.value.reserveEnd ? { reserveEnd: normalizeDatetimeLocal(form.value.reserveEnd) } : {}),
      status: form.value.status
    }
    const { data } = await axios.post(`${API}/reservations`, payload, { headers: headers() })
    successMsg.value = `บันทึกสำเร็จ (โต๊ะ ${data?.table?.number ?? '-'}, เวลาเริ่ม ${data?.reserveStart ?? '-'})`
    resetForm()
  } catch (e) {
    console.error(e)
    error.value = e?.response?.data?.msg || 'บันทึกการจองไม่สำเร็จ'
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  form.value = {
    customerName: '',
    phone: '',
    partySize: 1,
    tableId: '',
    reserveStart: '',
    reserveEnd: '',
    status: 'reserved'
  }
}

onMounted(fetchTables)
</script>

<style>
/* พื้นหลังครีมโทนร้านหมูกระทะ */
.bg-mookata {
  background-color: #fdf3e7;
}
</style>
