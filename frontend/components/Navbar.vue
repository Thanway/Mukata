<template>
  <nav class="bg-red-600 text-white px-6 py-4 flex justify-between items-center shadow-lg">
    <!-- โลโก้ -->
    <div class="flex items-center space-x-3">
  <div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center">
    <svg class="w-7 h-7 text-pink-600" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <!-- หูหมู -->
      <circle cx="7" cy="7" r="2" fill="currentColor"/>
      <circle cx="17" cy="7" r="2" fill="currentColor"/>
      <!-- หัวหมู -->
      <circle cx="12" cy="12" r="7" fill="currentColor"/>
      <!-- ตา -->
      <circle cx="10" cy="11" r="1" fill="black"/>
      <circle cx="14" cy="11" r="1" fill="black"/>
      <!-- จมูก -->
      <ellipse cx="12" cy="14" rx="3" ry="2" fill="#ffb6c1"/>
      <circle cx="11" cy="14" r="0.5" fill="black"/>
      <circle cx="13" cy="14" r="0.5" fill="black"/>
    </svg>
  </div>

      <NuxtLink to="/" class="text-2xl font-bold">Mukata Jurassic</NuxtLink>
    </div>

    <!-- เมนู -->
    <div class="space-x-6 hidden md:flex">
<NuxtLink to="/Home">Home</NuxtLink>
<NuxtLink to="/login">Login</NuxtLink>
 <NuxtLink to="/register">Register</NuxtLink> 
 <NuxtLink to="/dashboard">Dashboard</NuxtLink>
  <NuxtLink to="/table">Table</NuxtLink> 
  <NuxtLink to="/reservations">reservations</NuxtLink>
   <NuxtLink to="/logout">logout</NuxtLink>
    </div>
  </nav>
</template>
