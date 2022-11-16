import { ref, reactive } from "vue";
import { databaseGet } from "./tools";

export const global = reactive({
  contactList: ref([]),
  listLength: ref(0),
  contact: {
    first_name: "",
    last_name: "",
  },
  viewOpen: ref(false),
  deleteOpen: false,
  popUpOpen: false,
  popUpMessage: "",
  viewContact: false,
  editContact: false,
  newContact: false,

  async getList() {
    let rJson = await databaseGet("http://localhost:8000/contacts/");
    try {
      this.contactList = rJson;
      this.contactList.sort(function (a, b) {
        return a.first_name.localeCompare(b.first_name);
      });
      this.listLength = this.contactList.length;
      return;
    } catch (err) {
      console.error(err);
    }
  },

  async getContact(id) {
    let rJson = await databaseGet(`http://localhost:8000/contacts/${id}`);
    try {
      this.contact = rJson;
      return;
    } catch (err) {
      console.error(err);
    }
  },
});
