<template>
    <div>
      <div v-if="statusMessage" class="status-message">{{ statusMessage }}</div>
      <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      statusMessage: String,
      uploadError: String,
    },
  };
  </script>
  