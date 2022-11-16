// Let's save some lines of
// C
// O
// D
// E
import { global } from "./Global.js";

export const databaseGet = async (URI) => {
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
    let r = await fetch(`${URI}`, requestOptions);
    if (r.status == 200) {
      let rJson = await r.json();
      return rJson;
    }
    return { message: r };
  } catch (err) {
    return { message: err };
  }
};

export const databaseMutate = async (URI, body, method) => {
  let requestOptions = {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Credentials": true,
      "Access-Control-Allow-Methods": "*",
    },
    body: body,
  };
  if (method == "DELETE") {
    requestOptions = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
    };
  }
  try {
    let r = await fetch(`${URI}`, requestOptions);
    if (r.status == 200) {
      let rJson = await r.json();
      return rJson;
    }
    return { message: r };
  } catch (err) {
    return { message: err };
  }
};

export const getCityState = async (zipCode) => {
  let rJson = await databaseGet(`http://localhost:8000/usps/${zipCode}`);
  return rJson;
};

export const checkNames = (firstName, lastName) => {
  for (let i = 0; i < global.listLength; i++) {
    if (
      firstName.toLowerCase().trim() ==
        global.contactList[i].first_name.toLowerCase().trim() &&
      lastName.toLowerCase().trim() ==
        global.contactList[i].last_name.toLowerCase().trim()
    ) {
      return true;
    }
  }
  return false;
};
