from myproject.mongodb_conne import MongoConnection
from myapp.utils import generate_uuid_srt
db = MongoConnection().get_db()
Cliente = MongoConnection().get_collection('cliente')

def register_user(name, email, password):
    # with all validations and checks
    # insert the user in the database
    user = {
        '_id': generate_uuid_srt(),
        'name': name,
        'email': email,
        'password': password
    }

    return Cliente.insert_one(user)

def get_user(email):
    return Cliente.find_one({'email': email})

def login_user(email, password):
    user = get_user(email)
    if user and user['password'] == password:
        return user
    return None