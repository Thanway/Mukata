<template>
  <nav class="bg-red-600 text-white px-6 py-4 flex justify-between items-center shadow-lg">
    <!-- โลโก้ -->
    <div class="flex items-center space-x-3">
      <div class="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center">
        <svg class="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 24 24">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10
               10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5
               1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
          />
        </svg>
      </div>
      <NuxtLink to="/" class="text-2xl font-bold">Siam Moo Kata</NuxtLink>
    </div>

    <!-- เมนู -->
    <div class="space-x-6 hidden md:flex">
<NuxtLink to="/login">Login</NuxtLink>
 <NuxtLink to="/register">Register</NuxtLink> 
 <NuxtLink to="/dashboard">Dashboard</NuxtLink>
  <NuxtLink to="/table">Table</NuxtLink> 
  <NuxtLink to="/reservations">reservations</NuxtLink>
   <NuxtLink to="/logout">logout</NuxtLink>
    </div>
  </nav>
</template>
