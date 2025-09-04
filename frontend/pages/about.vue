<template>
  <section class="w-full min-h-screen py-12 px-4 bg-gradient-to-b from-red-50 to-orange-100">
    <h2 class="text-4xl font-extrabold text-center mb-8 text-red-700 drop-shadow">
      ทีมผู้พัฒนา
    </h2>

    <!-- โซนโชว์คนที่เลือก -->
    <div class="max-w-5xl mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-8 bg-white/70 rounded-3xl p-6 md:p-10 shadow-xl">

        <!-- ภาพใหญ่ + อนิเมชันตอนเปลี่ยน -->
        <Transition
          mode="out-in"
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4 scale-95 rotate-1"
          enter-to-class="opacity-100 translate-y-0 scale-100 rotate-0"
          leave-active-class="transition duration-300 ease-in"
          leave-from-class="opacity-100 translate-y-0 scale-100"
          leave-to-class="opacity-0 -translate-y-4 scale-95"
        >
          <div :key="selectedMember.name" class="flex justify-center">
            <div class="relative w-72 h-72 md:w-80 md:h-80 rounded-3xl overflow-hidden shadow-2xl ring-4 ring-red-500/70">
              <img :src="selectedMember.image" :alt="selectedMember.name" class="w-full h-full object-cover" />
              <!-- ป้ายชื่อมุมล่าง -->
              <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
                <p class="text-3xl font-black text-white tracking-wide drop-shadow">{{ selectedMember.name }}</p>
                <p class="text-white/90 text-sm">{{ selectedMember.role }}</p>
              </div>
            </div>
          </div>
        </Transition>

        <!-- ข้อมูล/ปุ่ม Activate เท่ๆ -->
        <div class="space-y-5">
          <div>
            <p class="uppercase text-sm tracking-widest text-red-600 font-bold">ตำแหน่ง</p>
            <p class="text-2xl font-extrabold text-slate-800">{{ selectedMember.role }}</p>
          </div>

          <p class="text-slate-700 leading-relaxed">
            {{ selectedMember.bio }}
          </p>

          <div class="flex items-center gap-3">
            <button
              class="px-6 py-3 rounded-xl bg-red-600 text-white font-semibold shadow hover:shadow-lg
                     active:scale-95 transition"
            >
              ACTIVATE
            </button>
              <NuxtLink
                :to="`/view/${selectedMember.name}`"
                class="px-6 py-3 rounded-xl border border-slate-300 bg-white text-slate-700 font-semibold hover:shadow"
              >
                VIEW PROFILE
              </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- แถบตัวเลือกด้านล่าง (thumbnail selector) -->
    <div class="max-w-5xl mx-auto mt-10">
      <div
        class="flex items-center justify-center gap-4 md:gap-6 flex-wrap
               bg-white/70 rounded-2xl p-4 shadow"
      >
        <button
          v-for="(m, i) in members"
          :key="m.name"
          @click="select(i)"
          @mouseenter="hovered = i"
          @mouseleave="hovered = null"
          class="group flex flex-col items-center"
        >
          <div
            class="w-16 h-16 rounded-2xl overflow-hidden ring-2 transition
                   shadow-md select-none
                   group-active:scale-95"
            :class="[
              selectedIndex === i ? 'ring-red-600 scale-105 shadow-lg' : 'ring-transparent hover:ring-red-300',
              hovered === i && selectedIndex !== i ? 'translate-y-[-2px]' : ''
            ]"
          >
            <img :src="m.image" :alt="m.name" class="w-full h-full object-cover"
                 :class="selectedIndex === i ? '' : 'grayscale hover:grayscale-0'" />
          </div>
          <span
            class="mt-2 text-sm font-semibold"
            :class="selectedIndex === i ? 'text-red-700' : 'text-slate-600 group-hover:text-red-600'"
          >
            {{ m.name }}
          </span>
        </button>
      </div>

      <!-- hint: ใช้คีย์บอร์ดซ้าย/ขวาได้ -->
      <p class="text-center text-slate-500 text-sm mt-3">กด ← → เพื่อเลือกคนได้</p>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

/** วางรูปไว้ในโฟลเดอร์ /public ของ Nuxt:
 *  public/co.jpg, public/chok.jpg, public/do.jpg, public/oat.jpg, public/kao.jpg
 */
const members = [
  {
    name: 'โชกุน',
    image: '/co.jpg',
    role: 'Frontend',
    bio: 'ดูแลหน้าเว็บ Nuxt 3, Tailwind, ทำระบบสั่งอาหารผ่าน QR และปรับ UI ให้สมูท'
  },
  {
    name: 'โชค',
    image: '/chok.jpg',
    role: 'Backend',
    bio: 'ดูแล API ด้วย FastAPI/Flask, เชื่อม MongoDB, ทำระบบ Auth และ Order'
  },
  {
    name: 'โด',
    image: '/do.jpg',
    role: 'DevOps',
    bio: 'ตั้งค่า Deploy/CI, Docker, Nginx, ติดตามสถานะเซิร์ฟเวอร์และ Log'
  },
  {
    name: 'โอ๊ต',
    image: '/oat.jpg',
    role: 'Data/AI',
    bio: 'ทำ Dashboard ยอดขาย และโมเดลช่วยคาดการณ์วัตถุดิบ'
  },
  {
    name: 'เก้า',
    image: '/kao.jpg',
    role: 'Designer',
    bio: 'ออกแบบ Branding สีแดง-ส้ม และส่วนติดต่อผู้ใช้ทั้งหมด'
  }
]

// state
const selectedIndex = ref(0)
const hovered = ref(null)
const selectedMember = computed(() => members[selectedIndex.value])

function select(i) {
  if (i < 0) i = members.length - 1
  if (i >= members.length) i = 0
  selectedIndex.value = i
}

// keyboard left/right
function onKey(e) {
  if (e.key === 'ArrowRight') select(selectedIndex.value + 1)
  if (e.key === 'ArrowLeft')  select(selectedIndex.value - 1)
}

onMounted(() => {
  window.addEventListener('keydown', onKey)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
})
</script>
