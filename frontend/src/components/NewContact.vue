<!-- New Contact, Composition API -->

<script setup>
import { ref } from 'vue'
import { singletons } from './singletons/singletons.js'
// import { getCity } from './usps/GetCity';

const addOpen = ref(false);
const messageOpen = ref(false);
const message = ref("");
const matchFound = ref(false);
const ignoreMatch = ref(false);
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
  zip: value => (String(value).length == 5 || String(value).length == 0) || 'Zip code should be 5 digits long',
});

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

const makeForm = () => {
  let body = JSON.stringify({
    first_name: firstName.value,
    last_name: lastName.value,
    cell_number: cellNum.value,
    office_number: officeNum.value,
    home_number: homeNum.value,
    email: email.value,
    zip_code: zipCode.value,
    city: city.value,
    state: state.value,
    favorite: favorite.value
  })
  let requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: body,
  };
  sendForm(requestOptions)
}

const sendForm = async (request) => {
  let r = await fetch("http://localhost:8000/contacts/", request);
  if (r.status == 200) {
    message.value = "New Contact Saved.";
    messageOpen.value = true;
    ignoreMatch.value = false;
    addOpen.value = false;
    clearForm();
    singletons.getList()
    setTimeout(() => {
      messageOpen.value = false;
    }, 1000);
    return;
  }
  console.error(r);
  message.value = "Oops, looks like something went wrong.";
  messageOpen.value = true;
  setTimeout(() => {
    messageOpen.value = false;
  }, 1000);
};

const checkName = () => {
  firstName.value = firstName.value.trim();
  lastName.value = lastName.value.trim();
  if (singletons.contactList.map(a => a.first_name) == (firstName.value)) {
    for (let i = 0; i < singletons.contactList.length; i++) {
      if (singletons.contactList[i].last_name == lastName.value) {
        matchFound.value = true;
        return
      }
    }
  }
  matchFound.value = false;
}

const close = () => {
  matchFound.value = false;
  addOpen.value = false;
  clearForm()
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
  <w-flex wrap column align-center justify-center class="text-center">
    <w-button type="submit" @click="addOpen = true"> <b>ADD NEW CONTACT</b>
    </w-button>
    <w-dialog v-model="addOpen" :width="350" persistent persistent-no-animation title-class="primary-light1--bg white">
      <w-card>
        <h2> {{ firstName + " " + lastName }}</h2>
        <w-form>
          <w-grid gap="2">
            <w-input type="text" v-model="firstName" label="First Name" :validators="[validators.required]"
              @blur="checkName()" @keyup="checkName()" />
            <w-input type="text" v-model="lastName" label="Last Name" @blur="checkName()" @keyup="checkName()" />
            <w-input type="tel" v-model="cellNum" label="Cellphone Number" @blur="cellNum = cellNum.trim()" />
            <w-input type="tel" v-model="officeNum" label="Office Number" @blur="officeNum = officeNum.trim()" />
            <w-input type="tel" v-model="homeNum" label="Home Number" @blur="homeNum = homeNum.trim()" />
            <w-input type="email" v-model="email" label="E-mail Address" @blur="email = email.trim()" />
            <div v-if="String(zipCode).length == 5">
              <w-input type="text" readonly v-model="city" label="City" />
              <w-input type="text" readonly v-model="state" label="State" />
            </div>
            <w-input type="number" v-model="zipCode" label="Zip Code" :validators="[validators.zip]" @blur="checkZip()"
              @keyup="checkZip()" />
            <w-checkbox class="align-center" v-model="favorite">Favorite</w-checkbox>
            <w-divider class="my3 mx-1" />
            <div>
              <w-button
                :disabled="firstName.trim() === '' || firstName == null || String(zipCode).length != 5 && String(zipCode).length != 0 || matchFound"
                type="submit" @click="makeForm()"> <b>SAVE</b>
              </w-button>
              <div v-if="matchFound">
                <h5>{{ firstName + " " + lastName }} already in your contacts. </h5>
              </div>
              <w-divider class="my3 mx-1" />
              <w-button type="submit" @click="close()" bg-color="light-blue" color="white"> <b>CLOSE</b>
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
  </w-flex>
</template>