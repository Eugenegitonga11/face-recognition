import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancerealtime-30470-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Murtaza Kabir",
            "major": "robotics",
            "starting_year": "2020",
            "total_attendance":6,
            "standing": "G",
            "year":4,
            "last_attendance_time": "2024-01-09 16:58:00"
        },
    "852741":
        {
            "name": "Emily Blunt",
            "major": "statistics",
            "starting_year": "2021",
            "total_attendance": 4,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2024-01-09 16:58:00"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "engineering",
            "starting_year": "2020",
            "total_attendance": 10,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-09 16:58:00"
        },
    "987466":
        {
            "name": "Samuel Kiganjo",
            "major": "software",
            "starting_year": "2020",
            "total_attendance": 8,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-09 16:58:00"
        },
    "908070":
        {
            "name": "Eugene Mbogo",
            "major": "engineering",
            "starting_year": "2021",
            "total_attendance": 8,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2024-01-09 16:58:00"
        }

}

for key, value in data.items():
    ref.child(key).set(value)
