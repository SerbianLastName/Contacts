<script setup>
// import { ref } from 'vue'
import '@mdi/font/css/materialdesignicons.min.css'
import { global } from './Global.js'

const viewContact = async (id) => {
  global.viewOpen = true
  global.viewContact = true
  global.editContact = false
  global.newContact = false
  await global.getContact(id)
}
</script>

<template>
  <w-list :items="global.contactList" hover>
    <template #item="{ item }">
      <w-flex align-center justify-center @click="viewContact(item.id_)">
        <h4>{{
            item.first_name + " " + item.last_name
        }} </h4>
        <div v-if="item.favorite">
          <w-icon class="mr1" xs color="primary">
            mdi mdi-star
          </w-icon>
        </div>
      </w-flex>
    </template>
  </w-list>
</template>