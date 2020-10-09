import firebase_admin
from firebase_admin import firestore
import pyrebase
from firebase_admin import auth


firebaseConfig = {
    'apiKey': "AIzaSyATnVoTGwXM0XpkPMrzsiBCEtpkchIHJ_8",
    'authDomain': "moviestreaming-582af.firebaseapp.com",
    'databaseURL': "https://moviestreaming-582af.firebaseio.com",
    'projectId': "moviestreaming-582af",
    'storageBucket': "moviestreaming-582af.appspot.com",
    'messagingSenderId': "211914614285",
    'appId': "1:211914614285:web:d89624ca6e8b5eac749744",
    'measurementId': "G-57G87TQ10G"
}
pyfirebase = pyrebase.initialize_app(firebaseConfig)

cred = firebase_admin.credentials.Certificate('firebaseconfig.json')
firebase_admin.initialize_app(cred)

storage= pyfirebase.storage()

db = firestore.client()
