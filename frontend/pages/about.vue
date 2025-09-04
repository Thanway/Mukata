<template>
  <section class="w-full min-h-screen py-16 px-4 bg-gradient-to-b from-red-50 to-orange-100">
    <h2 class="text-4xl font-extrabold text-center mb-12 text-red-700 drop-shadow">
      ทีมผู้พัฒนา
    </h2>

    <!-- Flex ให้จัดกลาง -->
    <div class="flex flex-wrap justify-center gap-10">
      <div
        v-for="(member, index) in members"
        :key="index"
        class="flex flex-col items-center bg-white p-6 rounded-2xl shadow-lg hover:scale-105 hover:shadow-xl transition w-60"
      >
        <!-- วงกลม -->
        <div class="w-40 h-40 rounded-full overflow-hidden mb-4 border-4 border-red-500 shadow-md">
          <img
            :src="member.image"
            :alt="member.name"
            class="w-full h-full object-cover"
          />
        </div>

        <!-- ชื่อ -->
        <p class="text-2xl font-extrabold text-red-700 tracking-wide text-center">
          {{ member.name }}
        </p>
      </div>
    </div>
  </section>
</template>


<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const API = 'https://api-mukata.loeitech.org/api'

const members = [
  { name: "โชกุน", image: "/co.jpg" },
  { name: "โชค", image: "/chok.jpg" },
  { name: "โด",   image: "/do.jpg" },
  { name: "โอ๊ต", image: "/oat.jpg" },
  { name: "เก้า", image: "/kao.jpg" }
];

</script>
