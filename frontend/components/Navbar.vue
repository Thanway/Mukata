<template>
  <nav class="bg-blue-600 text-white px-6 py-4 flex justify-between items-center">
    <NuxtLink to="/" class="font-bold text-xl">DailyNotes</NuxtLink>
    <div class="space-x-4">
      <NuxtLink to="/login">Login</NuxtLink>
      <NuxtLink to="/register">Register</NuxtLink>
      <NuxtLink to="/dashboard">Dashboard</NuxtLink>
      <NuxtLink to="/table">Table</NuxtLink>
      <NuxtLink to="/reservations">reservations</NuxtLink>
      <NuxtLink to="/logout">logout</NuxtLink>
    </div>
  </nav>
</template>
