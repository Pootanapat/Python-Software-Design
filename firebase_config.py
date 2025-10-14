import pyrebase

config = {
    "apiKey": "AIzaSyAQF0yAG3O3KmZUAhVsBF5xdIQ1R8oPyEc",
    "authDomain": "minifarm-911a8.firebaseapp.com",
    "databaseURL": "https://minifarm-911a8-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "minifarm-911a8",
    "storageBucket": "minifarm-911a8.firebasestorage.app",
    "messagingSenderId": "526557336577",
    "appId": "1:526557336577:web:b0f95d8ad5fcdbb1e5dc00"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()