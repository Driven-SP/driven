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
def signUpUser(fname, lname, email, phone, username, password):
    #  see if the username and email already exists
    users = db.collection(u'users').stream()
    for user in users:
        print(user.id)
        user_data = user.to_dict()
        if user.id == username:
            print("username already taken")
            return False
        elif user_data["email"] == email:
            print("email already taken")
            return False

    new_user_data = {
    u'fname': fname,
    u'lname': lname,
    u'email': email,
    u'phone': phone,
    u'password-hash': password,
    u'primary-address': "",
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


#  limitation: this could fail if unregistered username is provided, but since this is an internal
#  api, we should  call this only on registerd username
def addAddress(username, address):
    # register address in firebase first
    new_address_ref = db.collection(u'addresses').document()
    new_address_ref.set({
        u'address': address
    })

    #  todo: add check for dupliacy here, currently duplicate address cann live for a user
    #  this new address document_id is always unique, so it is not possible to tell if there
    #  is duplicaty of address based on this
    user_ref = db.collection(u'users').document(username)
    user_info = user_ref.get().to_dict()
    user_active_addresses = user_info["active-addresses"]
    user_active_addresses.append(new_address_ref.get().id)

    #  now, finally replace with new array containing the new address document id
    user_ref.set({
        u'active-addresses': user_active_addresses
    }, merge=True)


#  move address to inactive list
#  this is in part to provide user with the list of addresses he/she has ever used
#  limitation: we need to make sure both username and address_id that we give are valid
#  address_id should be in active-addresses list of username provided
def deleteAddress(username, address_id):
    user_ref = db.collection(u'users').document(username)
    user_info = user_ref.get().to_dict()

    user_active_addresses = user_info["active-addresses"]
    user_inactive_addresses = user_info["inactive-addresses"]

    user_active_addresses.remove(address_id)
    user_inactive_addresses.append(address_id)

    #  now, finally replace with new arrays
    user_ref.set({
        u'active-addresses': user_active_addresses,
        u'inactive-addresses': user_inactive_addresses
    }, merge=True)


#  this is the reverse of delete address, it moves address from inactive list to active list
#  like above, we need to make sure username exists and address_id is in inactive list
def reviveAddress(username, address_id):
    user_ref = db.collection(u'users').document(username)
    user_info = user_ref.get().to_dict()

    user_active_addresses = user_info["active-addresses"]
    user_inactive_addresses = user_info["inactive-addresses"]

    user_inactive_addresses.remove(address_id)
    user_active_addresses.append(address_id)

    #  now, finally replace with new arrays
    user_ref.set({
        u'active-addresses': user_active_addresses,
        u'inactive-addresses': user_inactive_addresses
    }, merge=True)


#  we need to make sure that username exists and that given address_id is in active address list
#  primary address also exists in active addresses list, so there is duplicacy
#  current primary address could be empty string set during user signup
def changePrimaryAddress(username, address_id):
    user_ref = db.collection(u'users').document(username)
    user_info = user_ref.get().to_dict()

    primary_address = user_info["primary-address"]
    user_active_addresses = user_info["active-addresses"]

    #  if current primary address id is non-empty string, move it back to active address list
    if primary_address:
        user_active_addresses.append(primary_address)

    #  remove new candidate from active address list
    user_active_addresses.remove(address_id)

    #  now, finally replace with new values
    user_ref.set({
        u'active-addresses': user_active_addresses,
        u'primary-address': address_id
    }, merge=True)


# Packages API


# Vendor API
def getUserAddress(username):
    pass

def validateCredVendor(username, password):
    pass


#  utility functions
#  supply a valid username
#  todo: use utilitity functions in above APIs, we can even optimize further by giving info that
#  we have already fetched from firebase so that we don't have to fetch it again
def getUserInfo(username):
    user_ref = db.collection(u'users').document(username)
    user_info = user_ref.get().to_dict()
    return user_info

#  supply a valid username
def getActiveAddressIds(username):
    user_info = getUserInfo(username)
    return user_info["active-addresses"]

#  supply a valid username
def getInactiveAddressIds(username):
    user_info = getUserInfo(username)
    return user_info["inactive-addresses"]

#  supply a valid username
def getPrimaryAddressId(username):
    user_info = getUserInfo(username)
    return user_info["primary-address"]

def getAddressFromId(address_id):
    address_ref = db.collection(u'addresses').document(address_id)
    address_info = address_ref.get().to_dict()
    return address_info["address"]





#  dev testing

#  same email
#  print(signUpUser("Kaushik", "Mishra", "kmishra@gmail.com", "111111111", "kaushik-new-username", "kaushik-password"))
#  same username
#  print(signUpUser("Kaushik", "Mishra", "km-new-email@gmail.com", "111111111", "kmishra", "kaushik-password"))
#  new user
#  print(signUpUser("Swarnim", "Bhandari", "swarnim@gmail.com", "111111111", "swarnim", "swarnim-password"))
#  login credentials validation
#  print(validateCredUser("kmishra", "kaushik-password"))
#  add address
#  addAddress("kmishra", "new address for kmishra")
#  if this fails, it means that the username is wrong
#  addAddress("kaushik-new-username", "new address for kaushik new username")
#  if this fails, it means that either username is wrong or address-id is not in the user's info
#  deleteAddress("kaushik-new-username", "q8XDWNBfLq2Xw8CgG0jU")

#  addAddress("kaushik-new-username", "1 test for change primary address")
#  addAddress("kaushik-new-username", "2 test for change primary address")
#  addAddress("kaushik-new-username", "3 test for change primary address")
#  changePrimaryAddress("kaushik-new-username", "6v92RACp4syi3Zg6Xx8t")
#  changePrimaryAddress("kaushik-new-username", "9ZNKA2IiU6BRmP6ttR6K")

#  deleteAddress("kaushik-new-username", "DDp2bhYziYp4aNIKHAUo")
#  reviveAddress("kaushik-new-username", "DDp2bhYziYp4aNIKHAUo")

#  print(getActiveAddressIds("kaushik-new-username"))
#  print(getInactiveAddressIds("kaushik-new-username"))
#  test_prim_address = getPrimaryAddressId("kaushik-new-username")
#  print(test_prim_address)
#  print(getAddressFromId(test_prim_address))
