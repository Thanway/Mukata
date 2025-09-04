<template>
  <nav class="bg-red-600 text-white px-6 py-3 shadow-lg sticky top-0 z-50">
    <div class="flex items-center justify-between">
      <!-- โลโก้ + ชื่อ -->
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-yellow-400 rounded-full grid place-items-center">
          <span class="text-pink-600 text-xl">🐷</span>
        </div>
        <NuxtLink to="/" class="text-xl font-bold">Mukata Jurassic</NuxtLink>
      </div>

      <!-- เมนูหลัก -->
      <div class="flex items-center gap-6 relative">
        <NuxtLink to="/Home" class="hover:underline">Home</NuxtLink>
        <NuxtLink to="/login" class="hover:underline">Login</NuxtLink>

        <!-- ปุ่ม Menu + Dropdown -->
        <div class="relative">
          <button
            @click="isOpen = !isOpen"
            :aria-expanded="isOpen"
            class="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition"
          >
            <span>Menu</span>
            <svg :class="isOpen ? 'rotate-180' : ''" class="w-4 h-4 transition-transform" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.08 1.04l-4.25 4.25a.75.75 0 01-1.06 0L5.21 8.27a.75.75 0 01.02-1.06z" clip-rule="evenodd"/>
            </svg>
          </button>

          <!-- อนิเมชัน dropdown -->
          <Transition
            enter-active-class="transition ease-out duration-200"
            enter-from-class="opacity-0 -translate-y-2 scale-95"
            enter-to-class="opacity-100 translate-y-0 scale-100"
            leave-active-class="transition ease-in duration-150"
            leave-from-class="opacity-100 translate-y-0 scale-100"
            leave-to-class="opacity-0 -translate-y-2 scale-95"
          >
            <div
              v-if="isOpen"
              class="absolute right-0 mt-2 w-48 bg-red-700 rounded-lg shadow-lg py-2 flex flex-col space-y-1 z-50"
            >
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/register" @click="isOpen=false">Register</NuxtLink>
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/dashboard" @click="isOpen=false">Dashboard</NuxtLink>
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/table" @click="isOpen=false">Table</NuxtLink>
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/reservations" @click="isOpen=false">Reservations</NuxtLink>
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/logout" @click="isOpen=false">Logout</NuxtLink>
              <NuxtLink class="block px-4 py-2 hover:bg-white/10 rounded" to="/about" @click="isOpen=false">About</NuxtLink>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
const isOpen = ref(false)

// ปิดเมนูเมื่อกด ESC (เล็ก ๆ น้อย ๆ เพื่อ UX)
const onKey = (e) => { if (e.key === 'Escape') isOpen.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>
