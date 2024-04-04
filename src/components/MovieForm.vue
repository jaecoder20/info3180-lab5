<script setup>
    import { ref, onMounted } from "vue";
    onMounted(() => {
    getCsrfToken();
    }); 
    let csrf_token = ref("");
    function getCsrfToken() {
    fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
    console.log(data);
    csrf_token.value = data.csrf_token;
    })
 } 
    function saveMovie(){
        let movieForm = document.getElementById('movieForm');
        let form_data = new FormData(movieForm);
        fetch("/api/v1/movies", {
            method: 'POST',
            body: form_data,
            headers: {
            'X-CSRFToken': csrf_token.value
            } 
            })
            .then(function (response) {
            return response.json();
            })
            .then(function (data) {
            // display a success message
            console.log(data);
            })
            .catch(function (error) {
            console.log(error);
            });
    }
</script>
<template>
  <form class="col-sm-6 justify-items-center" id="movieForm" @submit.prevent="saveMovie">
    <div class="form-group mb-3">
        <label class="form-label" for="title">Title</label><br>
        <input class="form-control" type="text" name="title" id="title">
    </div>
    <div class="form-group">
        <label class="form-label" for="description">Description</label><br>
        <textarea class="form-control" name="description" id="description" cols="30" rows="10"></textarea>
    </div>
    <div class="form-group">
        <label class="form-label" for="upload">Upload Movie Poster</label><br>
        <input class="form-control-file" type="file" name="poster" id="upload">
    </div>
    <button type="submit" class="btn btn-primary mb-2">Add Movie</button>
  </form>
</template>
