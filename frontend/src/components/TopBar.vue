<script setup>
import { global } from './Global.js'

const onClick = () => {
  global.newContact = true;
  global.viewOpen = true;
}
</script>

<template>
  <w-flex wrap column align-center justify-center class="text-center">
    <w-button type="submit" @click="onClick()"> <b>ADD NEW CONTACT</b>
    </w-button>
  </w-flex>
</template>