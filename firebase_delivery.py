import pyrebase

# Konfiguracja dostępu do Firebase
firebase_config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "databaseURL": "YOUR_DATABASE_URL",  # Opcjonalne, jeśli korzystasz z Realtime Database
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Funkcja do dodawania dostawy do kolekcji "delivery"
def add_delivery(uid, sender_name, sender_surname, sender_email, receiver_name, receiver_surname, receiver_email, target_parcel_locker):
    delivery_data = {
        "UID": uid,
        "SenderName": sender_name,
        "SenderSurname": sender_surname,
        "SenderEmail": sender_email,
        "ReceiverName": receiver_name,
        "ReceiverSurname": receiver_surname,
        "ReceiverEmail": receiver_email,
        "TargetParcelLocker": target_parcel_locker,
    }

    db.child("delivery").child(uid).set(delivery_data)

# Przykładowe dane dostawy
sample_delivery = {
    "uid": "1234",
    "sender_name": "John",
    "sender_surname": "Doe",
    "sender_email": "john.doe@example.com",
    "receiver_name": "Jane",
    "receiver_surname": "Doe",
    "receiver_email": "jane.doe@example.com",
    "target_parcel_locker": 1,
}

# Dodanie przykładowej dostawy do kolekcji "delivery"
add_delivery(
    sample_delivery["uid"],
    sample_delivery["sender_name"],
    sample_delivery["sender_surname"],
    sample_delivery["sender_email"],
    sample_delivery["receiver_name"],
    sample_delivery["receiver_surname"],
    sample_delivery["receiver_email"],
    sample_delivery["target_parcel_locker"]
)
