from firebase import firebase
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1755237355<0 else 0
import time

def readFirebase():
    firebase1 = firebase.FirebaseApplication('https://augmentedreality-af310-default-rtdb.firebaseio.com/', None)
    waterLevel = firebase1.get('/AE232/waterLevel', None)
    fire = firebase1.get('/AE232/fire', None)
    vibration = firebase1.get('/AE232/vibration', None)
    return(waterLevel,fire,vibration)


def writeFirebase(otp_status):

    firebase1 = firebase.FirebaseApplication('https://augmentedreality-af310-default-rtdb.firebaseio.com/', None)
    result = firebase1.put('AE235/','otp',otp_status)
    print(result)


#print(readFirebase())
