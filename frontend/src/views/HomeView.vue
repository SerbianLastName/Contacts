<script setup>
import NewContact from '/src/components/NewContact.vue'
import ContactList from '/src/components/ContactList.vue'
import { singletons } from '../components/singletons/singletons.js'

//  Retrieve contact list from singleton
singletons.getList()

</script>

<template>
  <div class="home">
    <w-card class="grow" content-class="pa7">
      <w-toolbar horizontal fixed top shadow>
        <w-flex column align-center>
          <NewContact />
        </w-flex>
      </w-toolbar>
    </w-card>
    <ContactList />
  </div>
</template>