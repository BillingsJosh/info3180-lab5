<template>
    <div>
      <h1 class="text-2xl font-bold mb-4">All Movies</h1>
      <div v-if="movies.length === 0">No movies yet.</div>
  
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="movie in movies" :key="movie.id" class="border p-4 rounded shadow">
          <img :src="movie.poster" alt="Poster" class="w-full h-60 object-cover rounded mb-2" />
          <h2 class="text-lg font-semibold">{{ movie.title }}</h2>
          <p>{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  let movies = ref([]);
  
  function fetchMovies() {
    fetch('/api/v1/movies')
      .then(res => res.json())
      .then(data => {
        movies.value = data.movies;
      })
      .catch(err => console.error("Failed to fetch movies:", err));
  }
  
  onMounted(() => {
    fetchMovies();
  });
  </script>
  