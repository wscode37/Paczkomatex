import firebase_admin
from firebase_admin import credentials, firestore

#default_app = firebase_admin.initialize_app()

cred = credentials.Certificate('paczkomatex-c4617-firebase-adminsdk-itnid-cf22f73bb4.json')
default_app = firebase_admin.initialize_app(cred)


def check_package_existence(document_id):
  db = firestore.client()
  doc_ref = db.collection('delivery').document(document_id)
  doc_snapshot = doc_ref.get()

  if doc_snapshot.exists:
      # Access the document data
      document_data = doc_snapshot.to_dict()
      print("Document data:", document_data)
      return document_data
  else:
      print(f"Document with ID {document_id} does not exist.")
      return None
  
