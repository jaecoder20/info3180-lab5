<script setup>
    let flashMessages = ref([]);
    let displayFlash = ref(false);
    let isSuccess = ref(false);
    const alertSuccessClass = 'alert-success';
    const alertErrorClass = 'alert-danger';
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
 function getFlashedErrors(errors){
    
    const errorStrings = [];
    errors.forEach(errorObject => {
    const key = Object.keys(errorObject)[0];
    const value = Object.values(errorObject)[0];
    errorStrings.push(`${key}: ${value}`);
    });
    for (let i=0;i<errorStrings.length;i++){

        flashMessages.value.push(errorStrings[i]);
    }
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
                if(data["errors"]==undefined){
                    displayFlash.value = true;
                    isSuccess.value = true;
                    flashMessages.value.push('Movie added successfully!');
                }else{
                    displayFlash.value = true;
                    isSuccess.value = false;
                    getFlashedErrors(data.errors)
                }
            })
            .catch(function (error) {
                console.log(error)
            });
    }
</script>
<template>
        <div v-for="(message, index) in flashMessages" :key="index" v-bind:class="[isSuccess ? alertSuccessClass : alertErrorClass]" class="alert">
            {{ message }}
        </div>
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
