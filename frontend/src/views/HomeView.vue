<script setup>
import TopBar from '/src/components/TopBar.vue'
import ContactList from '/src/components/ContactList.vue'
import ContactView from '/src/components/ContactView.vue'
import PopUp from '/src/components/PopUp.vue'
import { global } from '../components/Global.js'

global.getList()

</script>

<template>
  <div class="home">
    <w-card class="grow" content-class="pa5">
      <w-toolbar horizontal fixed top shadow>
        <w-flex column align-center>
          <TopBar />
        </w-flex>
      </w-toolbar>
    </w-card>
    <ContactView />
    <ContactList />
  </div>
  <PopUp />
</template>