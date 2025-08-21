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
    <div class="p-6 max-w-3xl mx-auto">
      <h1 class="text-4xl font-extrabold mb-8 text-center tracking-wide drop-shadow-lg">
        ฟอร์มจองโต๊ะ
      </h1>

      <!-- Error banner -->
      <div v-if="error" class="mb-6 bg-red-50 border border-red-300 text-red-800 rounded p-4">
        <p class="font-bold">เกิดข้อผิดพลาด</p>
        <p class="text-sm whitespace-pre-wrap">{{ error }}</p>
      </div>

      <!-- Form -->
      <div class="bg-white/85 rounded-lg p-6 shadow border border-cyan-600">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm mb-1">ชื่อลูกค้า *</label>
            <input
              v-model.trim="form.customerName"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
              placeholder="เช่น สมชาย ใจดี"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">เบอร์โทร</label>
            <input
              v-model.trim="form.phone"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
              placeholder="เช่น 0812345678"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">จำนวนคน *</label>
            <input
              v-model.number="form.partySize"
              type="number" min="1"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
              placeholder="เช่น 4"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">โต๊ะ *</label>
            <select
              v-model="form.tableId"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
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

          <div>
            <label class="block text-sm mb-1">เวลาเริ่ม *</label>
            <input
              v-model="form.reserveStart"
              type="datetime-local"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
            />
          </div>

          <div>
            <label class="block text-sm mb-1">เวลาสิ้นสุด *</label>
            <input
              v-model="form.reserveEnd"
              type="datetime-local"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
            />
            <p class="text-xs mt-1 opacity-70">* ไม่กรอกได้ ถ้าจะให้ระบบกำหนดอัตโนมัติ +120 นาที (ตั้งไว้ใน backend แล้ว)</p>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm mb-1">สถานะ</label>
            <select
              v-model="form.status"
              class="w-full bg-transparent border border-cyan-400 p-3 rounded-md focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500"
            >
              <option value="reserved">reserved</option>
              <option value="seated">seated</option>
              <option value="completed">completed</option>
              <option value="cancelled">cancelled</option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button
            @click="submit"
            class="bg-cyan-600 hover:bg-cyan-700 text-black font-semibold px-6 py-3 rounded-md shadow-md transition"
            :disabled="submitting"
          >
            {{ submitting ? 'กำลังบันทึก...' : 'บันทึกการจอง' }}
          </button>
          <button
            @click="resetForm"
            class="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold px-6 py-3 rounded-md shadow-md transition"
            :disabled="submitting"
          >
            ล้างฟอร์ม
          </button>
        </div>
      </div>

      <!-- Success mini banner -->
      <div v-if="successMsg" class="mt-6 bg-green-50 border border-green-300 text-green-800 rounded p-4">
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
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.font-ocean { font-family: 'Pacifico', cursive; }
.bg-ocean {
  background-image: url('https://images.unsplash.com/photo-1581322336686-c5a8f1b1d4be?auto=format&fit=crop&w=1500&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
