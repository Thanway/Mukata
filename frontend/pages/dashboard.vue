<template>
  <div class="min-h-screen bg-ocean text-black font-ocean">
    
    <!-- รูปภาพใต้น้ำเต็มจอ -->
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
        บันทึกใต้น้ำ
      </h1>

      <!-- เพิ่มโน้ต -->
      <div class="flex gap-3 mb-8">
        <input
          v-model="title"
          placeholder="หัวข้อ"
          class="bg-transparent border border-cyan-400 p-3 rounded-md w-1/3 placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500 shadow-sm text-black"
        />
        <input
          v-model="content"
          placeholder="เนื้อหา"
          class="bg-transparent border border-cyan-400 p-3 rounded-md flex-1 placeholder-cyan-800 focus:outline-cyan-300 focus:ring-2 focus:ring-cyan-500 shadow-sm text-black"
        />
        <button
          @click="createNote"
          class="bg-cyan-600 hover:bg-cyan-700 text-black font-semibold px-5 rounded-md shadow-md transition duration-300"
        >
          บันทึก
        </button>
      </div>

      <!-- ค้นหาโน้ต -->
      <div class="flex gap-3 mb-10">
        <input
          v-model="searchText"
          @keyup.enter="searchNotes"
          placeholder="ค้นหาโน้ต..."
          class="bg-transparent border border-cyan-300 p-3 rounded-md flex-1 placeholder-cyan-800 focus:outline-cyan-400 focus:ring-2 focus:ring-cyan-600 shadow-inner text-black"
        />
        <button
          @click="searchNotes"
          class="bg-cyan-500 hover:bg-cyan-600 text-black font-semibold px-5 rounded-md shadow transition duration-300"
        >
          ค้นหา
        </button>
        <button
          @click="clearSearch"
          class="bg-cyan-300 hover:bg-cyan-400 text-black font-semibold px-5 rounded-md shadow transition duration-300"
        >
          ล้าง
        </button>
      </div>

      <!-- แสดง Notes -->
      <div class="space-y-5">
        <NoteCard
          v-for="note in filteredNotes"
          :key="note.id"
          :note="note"
          @delete="deleteNote"
          class="bg-gradient-to-r from-cyan-100 via-blue-200 to-teal-100 rounded-lg p-6 shadow-lg border border-cyan-600 hover:shadow-2xl transition text-black"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const title = ref('')
const content = ref('')
const searchText = ref('')
const notes = ref([])

const fetchNotes = async () => {
  const token = localStorage.getItem('token')
  const res = await axios.get('http://localhost:5000/api/notes', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  notes.value = res.data
}

const createNote = async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.post('http://localhost:5000/api/notes', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    notes.value.unshift(res.data)
    title.value = ''
    content.value = ''
  } catch (e) {
    console.error('Create note failed:', e)
  }
}

const deleteNote = async (id) => {
  const token = localStorage.getItem('token')
  await axios.delete(`http://localhost:5000/api/notes/${id}`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  fetchNotes()
}

const searchNotes = () => {}

const clearSearch = () => {
  searchText.value = ''
}

const filteredNotes = computed(() => {
  if (!searchText.value) return notes.value
  return notes.value.filter(note =>
    note.title.toLowerCase().includes(searchText.value.toLowerCase()) ||
    note.content.toLowerCase().includes(searchText.value.toLowerCase())
  )
})

onMounted(fetchNotes)
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

.font-ocean {
  font-family: 'Pacifico', cursive;
}

.bg-ocean {
  background-image: url('https://images.unsplash.com/photo-1581322336686-c5a8f1b1d4be?auto=format&fit=crop&w=1500&q=80');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
