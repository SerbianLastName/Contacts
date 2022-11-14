import { ref, reactive } from "vue";

export const singletons = reactive({
    contactList: ref([]),
    listLength: 0,
    viewOpen: false,
    editContact: false,
    contact: {
        first_name: "",
        last_name: "",
    },
    async getList() {
        let requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        };
        let response = await fetch(
            "http://localhost:8000/contacts/",
            requestOptions
        );
        if (response.status == 200) {
            let rJson = await response.json();
            this.contactList = rJson;
            // Alphabetize
            this.contactList.sort(function(a, b) {
                return a.first_name.localeCompare(b.first_name);
            });
            // For some reason counting contactList.contactList in a component doesn't seem to work
            this.listLength = this.contactList.length;
            return;
        }
        console.error(response);
    },
    async getContact(id) {
        let requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        };
        let response = await fetch(
            `http://localhost:8000/contacts/${id}`,
            requestOptions
        );
        if (response.status == 200) {
            let rJson = await response.json();
            this.contact = rJson;
            return;
        }
        console.error(response);
    },
});