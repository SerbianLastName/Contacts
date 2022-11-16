<script setup>
import { ref, watch } from 'vue'
import '@mdi/font/css/materialdesignicons.min.css'
import { global } from './Global.js'
import { databaseMutate, getCityState, checkNames } from './tools';

const matchFound = ref(false);
const firstName = ref("");
const lastName = ref("");
const cellNum = ref("");
const officeNum = ref("");
const homeNum = ref("");
const email = ref("");
const zipCode = ref("");
const city = ref("");
const state = ref("");
const favorite = ref(false);
const validators = ref({
  required: value => !!value || 'A first name is required',
  zip: value => (String(value).length == 5 || String(value).length == 0) || 'Zip code should be 5 digits long'
});

const close = () => {
  clearForm()
  global.newContact = false
  global.editContact = false
  global.viewContact = false
  global.viewOpen = false
}

watch(global, () => {
  if (global.viewContact) setForm();
})

const edit = () => {
  global.editContact = true
  global.viewContact = false
}

const cancelEdit = () => {
  global.editContact = false
  global.viewContact = true
  setForm()
}

const setForm = () => {
  firstName.value = global.contact.first_name;
  lastName.value = global.contact.last_name;
  cellNum.value = global.contact.cell_number;
  officeNum.value = global.contact.office_number;
  homeNum.value = global.contact.office_number;
  email.value = global.contact.email;
  city.value = global.contact.city;
  state.value = global.contact.state;
  zipCode.value = global.contact.zip_code;
  favorite.value = global.contact.favorite;
}

const clearForm = () => {
  firstName.value = "";
  lastName.value = "";
  cellNum.value = "";
  officeNum.value = "";
  homeNum.value = "";
  email.value = "";
  zipCode.value = "";
  city.value = "";
  state.value = "";
  favorite.value = false;
}

const makeForm = (method) => {
  let body = JSON.stringify({
    first_name: firstName.value,
    last_name: lastName.value,
    cell_number: cellNum.value,
    office_number: officeNum.value,
    home_number: homeNum.value,
    email: email.value,
    city: city.value,
    state: state.value,
    zip_code: zipCode.value,
    favorite: favorite.value,
  })
  sendContactForm(body, method)
}

const sendContactForm = async (body, method) => {
  let id_ = ""
  global.popUpMessage = "New Contact Saved."
  if (method == "PUT") {
    id_ = global.contact.id_
    global.popUpMessage = "Contact Updated."
  }
  if (method == "DELETE") {
    id_ = global.contact.id_
    global.popUpMessage = "Contact Deleted."
  }
  let rJson = await databaseMutate(`http://localhost:8000/contacts/${id_}`, body, method);
  if (rJson.success) {
    global.popUpOpen = true
    global.editContact = false
    global.newContact = false
    global.getList()
    if (method == "DELETE" || method == "POST") {
      global.viewContact = false
      global.viewOpen = false
      global.deleteOpen = false
      clearForm()
    }
    setTimeout(() => {
      global.popUpOpen = false;
    }, 1500);
    return;
  }
  console.error(rJson.message);
  global.popUpMessage = "Oops, looks like something went wrong."
  global.popUpOpen = true
  setTimeout(() => {
    global.popUpOpen = false;
  }, 1500);
};

const checkName = () => {
  matchFound.value = checkNames(firstName.value.trim(), lastName.value.trim())
}

const checkZip = async () => {
  let rJson = await getCityState(zipCode.value)
  city.value = rJson.city;
  state.value = rJson.state;
}
</script>

<template>
  <w-flex wrap column align-center justify-center class="text-center">
    <w-dialog v-model="global.viewOpen" :width="350" persistent title-class="primary-light1--bg white">
      <w-card>
        <h2> {{ firstName + " " + lastName }}</h2>
        <w-divider class="my3 mx-1" />
        <w-form>
          <w-grid gap="2">
            <w-flex wrap column>
              <w-input type="text" :readonly="global.viewContact" v-model="firstName" label="First Name"
                :validators="[validators.required]" @blur="checkName()" @keyup="checkName()" />
              <w-input type="text" :readonly="global.viewContact" v-model="lastName" label="Last Name"
                @blur="checkName()" @keyup="checkName()" />
              <w-input type="tel" :readonly="global.viewContact" v-model="cellNum" label="Cellphone Number"
                @blur="cellNum = cellNum.trim()" />
              <w-input type="tel" :readonly="global.viewContact" v-model="officeNum" label="Office Number"
                @blur="officeNum = officeNum.trim()" />
              <w-input type="tel" :readonly="global.viewContact" v-model="homeNum" label="Home Number"
                @blur="homeNum = homeNum.trim()" />
              <w-input type="email" :readonly="global.viewContact" v-model="email" label="E-mail Address"
                @blur="email = email.trim()" />
              <div v-if="String(zipCode).length == 5">
                <w-input type="text" readonly v-model="city" label="City" />
                <w-input type="text" readonly v-model="state" label="State" />
              </div>
              <w-input type="number" :readonly="global.viewContact" v-model="zipCode" label="Zip Code"
                :validators="[validators.zip]" @blur="checkZip()" @keyup="checkZip()" />
              <w-divider class="my1 mx-1" color="white" />
              <w-checkbox class="align-center" :disabled="global.viewContact" v-model="favorite">Favorite
              </w-checkbox>
              <w-divider class="my2 mx-1" />
              <div>
                <div v-if="global.newContact">
                  <w-button
                    :disabled="firstName.trim() === '' || firstName == null || String(zipCode).length != 5 && String(zipCode).length != 0 || matchFound"
                    type="submit" @click="makeForm('POST')"> <b>SAVE</b>
                  </w-button>
                </div>
                <div v-if="global.viewContact">
                  <div v-if="!global.editContact">
                    <w-button type="submit" @click="edit()"> <b>EDIT</b>
                    </w-button>
                  </div>
                </div>
                <div v-if="global.editContact">
                  <w-button type="submit" @click="cancelEdit()" bg-color="light-blue" color="white">
                    <b>CANCEL</b>
                  </w-button>
                  <w-divider class="my1 mx-1" color="white" />
                  <w-button
                    :disabled="firstName.trim() === '' || firstName == null || String(zipCode).length != 5 && String(zipCode).length != 0 || matchFound"
                    type="submit" @click="makeForm('PUT')"> <b>SAVE</b>
                  </w-button>
                  <w-divider class="my1 mx-1" color="white" />
                  <w-button type="submit" @click="global.deleteOpen = true" bg-color="error">
                    <b>DELETE</b>
                  </w-button>
                </div>
                <div v-if="matchFound">
                  <h5>{{ firstName + " " + lastName }} is already in your contacts. </h5>
                </div>
                <w-divider class="my1 mx-1" color="white" />
                <div v-if="!global.editContact">
                  <w-divider class="my1 mx-1" color="white" />
                  <w-button type="submit" @click="close()" bg-color="light-blue" color="white">
                    <b>CLOSE</b>
                  </w-button>
                </div>
              </div>
            </w-flex>
          </w-grid>
        </w-form>
      </w-card>
    </w-dialog>
    <w-dialog v-model="global.deleteOpen" :width="350" persistent title-class="primary-light1--bg white">
      <h3> Are you sure you want to delete {{ firstName + " " + lastName }}?</h3>
      <h5> This action can't be undone.</h5>
      <w-divider class="my3 mx-1" />
      <w-button type="submit" @click="makeForm('DELETE')" bg-color="error">
        <b>DELETE</b>
      </w-button>
      <w-divider class="my3 mx-1" />
      <w-button type="submit" @click="global.deleteOpen = false" bg-color="light-blue" color="white">
        <b>CANCEL</b>
      </w-button>
    </w-dialog>
  </w-flex>
</template>