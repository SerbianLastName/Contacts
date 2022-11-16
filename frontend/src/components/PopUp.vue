<script setup>
import { global } from './Global.js'
</script>

<template>
  <w-dialog v-model="global.popUpOpen" :width="350" persistent title-class="primary-light1--bg white">
    <h2> {{ global.popUpMessage }}</h2>
  </w-dialog>
</template>