<template>
  <div>
    <h2>Add a Movie</h2>

    <!-- Success Message -->
    <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

    <!-- Error Messages -->
    <div v-if="errorMessages.length" class="alert alert-danger">
      <ul>
        <li v-for="(error, index) in errorMessages" :key="index">{{ error }}</li>
      </ul>
    </div>

    <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" />
      </div>

      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea name="description" class="form-control"></textarea>
      </div>

      <div class="form-group mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input type="file" name="poster" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">Add Movie</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

let csrf_token = ref("")
let successMessage = ref("")
let errorMessages = ref([])

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token
    })
}

onMounted(() => {
  getCsrfToken()
})

function saveMovie() {
  let movieForm = document.getElementById('movieForm')
  let formData = new FormData(movieForm)

  fetch('/api/v1/movies', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        successMessage.value = data.message
        errorMessages.value = []
        movieForm.reset()
      } else if (data.errors) {
        errorMessages.value = data.errors
        successMessage.value = ""
      }
    })
    .catch(error => {
      console.error("Error submitting movie:", error)
    })
}
</script>
