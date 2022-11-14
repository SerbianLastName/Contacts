from bson.objectid import ObjectId
from config.config import DB, CONF
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging
import requests

from .models import ContactBase, ContactOnDB

contacts_router = APIRouter()

def validate_object_id(id_: str):
    try:
        _id = ObjectId(id_)
    except Exception:
        if CONF["fastapi"].get("debug", False):
            logging.warning("Invalid Object ID")
        raise HTTPException(status_code=400)
    return _id


async def _get_contact_or_404(id_: str):
    _id = validate_object_id(id_)
    contact = await DB.contact.find_one({"_id": _id})
    if contact:
        return contact
    else:
        raise HTTPException(status_code=404, detail="contact not found")


def fix_contact_id(contact):
    contact["id_"] = str(contact["_id"])
    return contact


@contacts_router.get("/", response_model=List[ContactOnDB])
async def get_all_contacts(limit: int = 1000, skip: int = 0):
    """[summary]
    Gets all contacts.
    [description]
    Endpoint to retrieve contacts.
    """    
    contacts_cursor = DB.contact.find().skip(skip).limit(limit)
    contacts = await contacts_cursor.to_list(length=limit)
    return list(map(fix_contact_id, contacts))


@contacts_router.post("/", response_model=ContactOnDB)
async def add_contact(contact: ContactBase):
    """[summary]
    Inserts a new contact on the DB.
    [description]
    Endpoint to add a new contact.
    """
    contact_op = await DB.contact.insert_one(contact.dict())
    if contact_op.inserted_id:
        contact = await _get_contact_or_404(contact_op.inserted_id)
        contact["id_"] = str(contact["_id"])
        return contact


@contacts_router.get(
    "/{id_}",
    response_model=ContactOnDB
)
async def get_contact_by_id(id_: ObjectId = Depends(validate_object_id)):
    """[summary]
    Get one contact by ID.
    [description]
    Endpoint to retrieve an specific contact.
    """
    
    contact = await DB.contact.find_one({"_id": id_})
    if contact:
        contact["id_"] = str(contact["_id"])
        return contact
    else:
        raise HTTPException(status_code=404, detail="Contact not found")
    

@contacts_router.delete(
    "/{id_}",
    dependencies=[Depends(_get_contact_or_404)],
    response_model=dict
)
async def delete_contact_by_id(id_: str):
    """[summary]
    Get one contact by ID.
    [description]
    Endpoint to retrieve an specific contact.
    """
    contact_op = await DB.contact.delete_one({"_id": ObjectId(id_)})
    if contact_op.deleted_count:
        return {"status": f"deleted count: {contact_op.deleted_count}"}


@contacts_router.put(
    "/{id_}",
    dependencies=[Depends(validate_object_id), Depends(_get_contact_or_404)],
    response_model=ContactOnDB
)
async def update_contact(id_: str, contact_data: ContactBase):
    """[summary]
    Update a contact by ID.
    [description]
    Endpoint to update an specific contact with some or all fields.
    """
    print(id_)
    contact_op = await DB.contact.update_one(
        {"_id": ObjectId(id_)}, {"$set": contact_data.dict()}
    )
    if contact_op.acknowledged:
        pass
    else:
        print("the bad stuff")
        raise HTTPException(status_code=304)