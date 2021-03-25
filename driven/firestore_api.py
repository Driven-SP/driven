import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

#  we reference this db for each change in data that we do
#  cred_path = os.path.join(app.root_path, 'firestore-cred.json')
cred = credentials.Certificate('/Users/psapkota/source/driven-clean/driven/firestore-cred.json')
initialize_app(cred)

db = firestore.client()

#  all the actions are done for signed in users
#  to know which user is signed in, we will use Flask's session

# User API
def signUpUser(fname, lname, email, phone, username, password, primary_address):
    #  see if the username already exists
    users = db.collection(u'users').stream()
    for user in users:
        print(user.id)
        if user.id == username:
            print("username already taken")
            return False

    new_user_data = {
    u'fname': fname,
    u'lname': lname,
    u'email': email,
    u'phone': phone,
    u'password-hash': password,
    u'primary-address': primary_address,
    u'active-addresses' : [],
    u'inactive-addresses' : [],
    u'vendors-with-access' : []
    }

    db.collection(u'users').document(username).set(new_user_data)

    return True

#  takes in username and password
#  returns True if valid user credentials and False if invalid user credentials
def validateCredUser(username, password):
    user_ref = db.collection(u'users').document(username)
    data = user_ref.get()

    if data.exists:
        data_dict = data.to_dict()
        return data_dict['password-hash'] == password
    return False

def addAddress(username, address):
    pass

def deleteAddress(username, address):
    pass

def changePrimaryAddress(username, address):
    pass


# Vendor API
def getUserAddress(username):
    pass

def validateCredVendor(username, password):
    pass

#  dev testing
#  print(validateCredUser("prabinspkt", "prabin-password"))

#  print(signUpUser("Kaushik", "Mishra", "km@gmail.com", "111111111", "km", "kaushik-password", "Kaushik primary address"))
