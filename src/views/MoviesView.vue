<script setup>
import { ref, onMounted } from "vue";
let movies = ref([]);

onMounted(() => {
    fetchMovies();
});
function fetchMovies(){
    fetch("/api/v1/movies", {
        method: 'GET'
        })
        .then(function (response) {
        return response.json();
        })
        .then(function (data) {
          movies.value = data.movies;
          movies.value.forEach(movie => fetchPoster(movie));
        })
        .catch(function (error) {
            console.log(error)
        });
    
}
function fetchPoster(movie) {
    fetch(`/api/v1/posters/${movie.poster}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        movie.poster = data.posterURL;
    })
    .catch(error => console.error(error));
}
</script> 
<template>
  <div class="container">
      <h1 class="my-4">Movies</h1>
      <div class="row">
          <div v-for="movie in movies" :key="movie.id" class="col-lg-6 col-md-8 mb-4">
              <div class="card h-100">
                  <div class="row g-0 h-100">
                      <div class="col-md-4">
                          <img :src="movie.poster" alt="Movie Poster" class="card-img h-100">
                      </div>
                      <div class="col-md-8">
                          <div class="card-body">
                              <h2 class="card-title">{{ movie.title }}</h2>
                              <p class="card-text">{{ movie.description }}</p>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>