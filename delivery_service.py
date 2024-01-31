import firebase_admin
from firebase_admin import credentials, firestore
import package_model

#default_app = firebase_admin.initialize_app()

import os
current_dir = os.path.dirname(__file__)
cred = credentials.Certificate(os.path.join(current_dir, 'paczkomatex-c4617-firebase-adminsdk-itnid-cf22f73bb4.json'))
default_app = firebase_admin.initialize_app(cred)


def check_package_existence(document_id):
  db = firestore.client()
  doc_ref = db.collection('delivery').document(str(document_id))
  doc_snapshot = doc_ref.get()

  if doc_snapshot.exists:
      # Access the document data
      document_data = doc_snapshot.to_dict()
      package = package_model.Package(
            package_id=document_id,
            receiver_e=document_data.get('receiver_email'), 
            sender_e=document_data.get('sender_email'),
            target=document_data.get('target_parcel_locker')
        )
      return package
  else:
      print(f"Document with ID {document_id} does not exist.")
      return None


def remove_package_from_firestore(document_id):
    db = firestore.client()
    doc_ref = db.collection('delivery').document(str(document_id))

    # Try to delete the document
    try:
        doc_ref.delete()
        print(f"Document with ID {document_id} successfully deleted from Firestore.")
    except Exception as e:
        print(f"Error deleting document with ID {document_id}: {e}") 

import config

def add_package(package_data):
    # Dodaj dane paczki do pierwszego wolnego miejsca
    available_slot = next((idx for idx, package_info in enumerate(config.device_packages) if package_info is None), None)

    if available_slot is not None:
        config.device_packages[available_slot] = package_data
        return available_slot
    else:
        return None

def remove_package(package_id):
    # Find the index of the package with the specified package_id
    package_index = next((idx for idx, package in enumerate(config.device_packages) if package and package.package_uid == package_id), None)

    if package_index is not None:
        # Remove the package at the found index
        
        config.device_packages[package_index] = None
        print(f"Package with ID {package_id} removed.")
        return True
    else:
        print(f"Package with ID {package_id} not found.")
        return False
    
def is_package_at_device(package_id):
    # Check if the package with the specified package_id is present in config.device_packages
    return any(package and package.package_uid == package_id for package in config.device_packages)
