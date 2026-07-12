from tinydb import TinyDB, Query

db = TinyDB("database.json")
students = db.table("students")
User = Query()


students.insert({
    "username": 'Alex',
    "password": 'Alex',
    "contact": 123456789,
    "address": 'Hyderabad',
    "role": "user"
})


students.get(User.username == "Alex")

students.search(User.role == "student")

students.all()


students.update({'Username' : 'Sam'}, User.address == 'Hyderabad' ) 

students.remove(User.username== 'Sam')
