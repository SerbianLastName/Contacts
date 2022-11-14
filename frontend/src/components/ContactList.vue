<script setup>
import { ref } from 'vue'
import '@mdi/font/css/materialdesignicons.min.css'
import { singletons } from './singletons/singletons.js'

const messageOpen = ref(false)
const deleteOpen = ref(false)
const matchFound = ref(false);
const message = ref("")
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

const onClick = async (id) => {
  singletons.viewOpen = true
  await singletons.getContact(id)
  setForm()
}

const cancel = () => {
  singletons.editContact = false
  setForm()
}

const setForm = () => {
  firstName.value = singletons.contact.first_name;
  lastName.value = singletons.contact.last_name;
  cellNum.value = singletons.contact.cell_number;
  officeNum.value = singletons.contact.office_number;
  homeNum.value = singletons.contact.office_number;
  email.value = singletons.contact.email;
  city.value = singletons.contact.city;
  state.value = singletons.contact.state;
  zipCode.value = singletons.contact.zip_code;
  favorite.value = singletons.contact.favorite;
}

const closeEdit = () => {
  singletons.viewOpen = false;
  singletons.editContact = false;
}

const makeForm = () => {
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
  let requestOptions = {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  };
  sendForm(requestOptions)
}

const sendForm = async (request) => {
  let response = await fetch(`http://localhost:8000/contacts/${singletons.contact.id_}`, request);
  if (response.status == 200) {
    message.value = "Contact Updated."
    messageOpen.value = true
    singletons.editContact = false
    singletons.getList()
    setTimeout(() => {
      messageOpen.value = false;
    }, 1000);
    return;
  }
  console.error(response);
  message.value = "Oops, looks like something went wrong."
  messageOpen.value = true
  setTimeout(() => {
    messageOpen.value = false;
  }, 1000);
};

const deleteContact = async () => {
  let requestOptions = {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  };
  let response = await fetch(`http://localhost:8000/contacts/${singletons.contact.id_}`, requestOptions);
  if (response.status == 200) {
    message.value = "Contact Deleted."
    messageOpen.value = true
    deleteOpen.value = false
    singletons.editContact = false
    singletons.viewOpen = false
    singletons.getList()
    setTimeout(() => {
      messageOpen.value = false;
    }, 1000);
    return;
  }
  console.error(response);
  message.value = "Oops, looks like something went wrong."
  messageOpen.value = true
  setTimeout(() => {
    messageOpen.value = false;
  }, 1000);
}

const checkName = () => {
  console.log("Checking name")
  firstName.value = firstName.value.trim();
  lastName.value = lastName.value.trim();
  if (firstName.value.toLowerCase() == singletons.contact.first_name.toLowerCase() && lastName.value.toLowerCase() == singletons.contact.last_name.toLowerCase()) return;
  console.log("no edit check passed");
  for (var i = 0; i < singletons.contactList.length; i++) {
    if (singletons.contactList[i].first_name.toLowerCase() == firstName.value.toLowerCase() && singletons.contactList[i].last_name.toLowerCase() == lastName.value.toLowerCase()) {
      matchFound.value = true;
      return
    }
  }
  matchFound.value = false;
}

const checkZip = async () => {
  if (String(zipCode.value).length == 5) {
    let requestOptions = {
      headers: {
        "Content-Type": "text/xml",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": true,
        "Access-Control-Allow-Methods": "*",
      },
      method: "get",
    };
    try {
      let r = await fetch(
        `http://localhost:8000/check/${zipCode.value}`,
        requestOptions
      );
      let rJson = await r.json()
      city.value = rJson.city
      state.value = rJson.state
      return
    } catch (err) {
      console.error(err);
    }
  }
  city.value = "";
  state.value = "";
}

</script>

<template>
  <w-list :items="singletons.contactList" hover>
    <template #item="{ item }">
      <w-flex align-center justify-center @click="onClick(item.id_)">
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
  <w-flex wrap column align-center justify-center class="text-center">
    <w-dialog v-model="singletons.viewOpen" :width="350" persistent persistent-no-animation
      title-class="primary-light1--bg white">
      <w-card>
        <h2> {{ firstName + " " + lastName }}</h2>
        <w-divider class="my3 mx-1" />
        <w-form>
          <w-grid gap="2">
            <w-input type="text" :readonly="!singletons.editContact" v-model="firstName" label="First Name"
              :validators="[validators.required]" @blur="checkName()" @keyup="checkName()" />
            <w-input type="text" :readonly="!singletons.editContact" v-model="lastName" label="Last Name"
              @blur="checkName()" @keyup="checkName()" />
            <w-input type="tel" :readonly="!singletons.editContact" v-model="cellNum" label="Cellphone Number"
              @blur="cellNum = cellNum.trim()" />
            <w-input type="tel" :readonly="!singletons.editContact" v-model="officeNum" label="Office Number"
              @blur="officeNum = officeNum.trim()" />
            <w-input type="tel" :readonly="!singletons.editContact" v-model="homeNum" label="Home Number"
              @blur="homeNum = homeNum.trim()" />
            <w-input type="email" :readonly="!singletons.editContact" v-model="email" label="E-mail Address"
              @blur="email = email.trim()" />
            <div v-if="String(zipCode).length == 5">
              <w-input type="text" readonly v-model="city" label="City" />
              <w-input type="text" readonly v-model="state" label="State" />
            </div>
            <w-input type="number" :readonly="!singletons.editContact" v-model="zipCode" label="Zip Code"
              :validators="[validators.zip]" @blur="checkZip()" @keyup="checkZip()" />
            <w-checkbox class="align-center" :disabled="!singletons.editContact" v-model="favorite">Favorite
            </w-checkbox>
            <w-divider class="my3 mx-1" />
            <div>
              <div v-if="!singletons.editContact">
                <w-button type="submit" @click="singletons.editContact = true"> <b>EDIT</b>
                </w-button>
              </div>
              <div v-if="singletons.editContact">
                <w-button type="submit" @click="cancel()" bg-color="light-blue" color="white"> <b>CANCEL</b>
                </w-button>
                <w-button
                  :disabled="firstName.trim() === '' || firstName == null || String(zipCode).length != 5 && String(zipCode).length != 0 || matchFound"
                  type="submit" @click="makeForm()"> <b>SAVE</b>
                </w-button>
                <div v-if="matchFound">
                  <h5>{{ firstName + " " + lastName }} is already in your contacts. </h5>
                </div>
                <w-divider class="my3 mx-1" />
                <w-button type="submit" @click="deleteOpen = true" bg-color="error">
                  <b>DELETE</b>
                </w-button>

              </div>
              <w-divider class="my3 mx-1" />
              <w-button type="submit" @click="closeEdit()" bg-color="light-blue" color="white"> <b>CLOSE</b>
              </w-button>
            </div>
          </w-grid>
        </w-form>
      </w-card>
    </w-dialog>
    <w-dialog v-model="messageOpen" :width="350" persistent persistent-no-animation
      title-class="primary-light1--bg white">
      <h2> {{ message }}</h2>
    </w-dialog>
    <w-dialog v-model="deleteOpen" :width="350" persistent persistent-no-animation
      title-class="primary-light1--bg white">
      <h3> Are you sure you want to delete {{ firstName + " " + lastName }}?</h3>
      <h5> This action can't be undone.</h5>
      <w-divider class="my3 mx-1" />
      <w-button type="submit" @click="deleteContact()" bg-color="error">
        <b>DELETE</b>
      </w-button>
      <w-divider class="my3 mx-1" />
      <w-button type="submit" @click="deleteOpen = false" bg-color="light-blue" color="white">
        <b>CANCEL</b>
      </w-button>
    </w-dialog>
  </w-flex>
</template>