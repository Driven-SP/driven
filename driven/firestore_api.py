import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

#  we reference this db for each change in data that we do
#  cred_path = os.path.join(app.root_path, 'firestore-cred.json')
cred = credentials.Certificate('/Users/psapkota/source/driven-clean/driven/firestore-cred.json')
initialize_app(cred)

db = firestore.client()

# User API
def signUpUser(fname, lname, email, phone, username, password):
    #  see if the username and email already exists
    users = db.collection(u'users').stream()
    for user in users:
        user_data = user.to_dict()
        print(user_data["username"])
        if user_data["username"] == username:
            print("username already taken")
            return False
        elif user_data["email"] == email:
            print("email already taken")
            return False

    new_user_data = {
    u'fname': fname,
    u'lname': lname,
    u'username': username,
    u'email': email,
    u'phone': phone,
    u'password-hash': password,
    u'primary-address': "",
    u'active-addresses' : [],
    u'inactive-addresses' : [],
    u'vendors-with-access' : []
    }

    #  let firebase create document_id automatically autotmatically
    new_user_ref = db.collection(u'users').document()
    new_user_ref.set(new_user_data)

    return True

#  takes in username and password
#  returns True if valid user credentials and False if invalid user credentials
def validateCredUser(user_document_id, password):
    user_ref = db.collection(u'users').document(user_document_id)
    data = user_ref.get()

    if data.exists:
        data_dict = data.to_dict()
        return data_dict['password-hash'] == password
    return False


#  Profile API

def changeLnameUser(user_document_id, new_lname):
    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'lname': new_lname
    }, merge=True)


def changeFnameUser(user_document_id, new_fname):
    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'fname': new_fname
    }, merge=True)


#  updated username should also be unique
def changeUsernameUser(user_document_id, new_username):
    users = db.collection(u'users').stream()
    for user in users:
        user_data = user.to_dict()
        if user_data["username"] == new_username:
            print("username already taken")
            return False

    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'username': new_username
    }, merge=True)
    return True


#  updated email should also be unique
def changeEmailUser(user_document_id, new_email):
    users = db.collection(u'users').stream()
    for user in users:
        user_data = user.to_dict()
        if user_data["email"] == new_email:
            print("email already taken")
            return False

    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'email': new_email
    }, merge=True)
    return True


def changePhoneUser(user_document_id, new_phone):
    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'phone': new_phone
    }, merge=True)


def changePasswordUser(user_document_id, new_password):
    user_ref = db.collection(u'users').document(user_document_id)
    user_ref.set({
        u'password-hash': new_password
    }, merge=True)


#  Address API

#  limitation: this could fail if unregistered username is provided, but since this is an internal
#  api, we should  call this only on registerd username
def addAddressUser(user_document_id, address):
    # register address in firebase first
    new_address_ref = db.collection(u'addresses').document()
    new_address_ref.set({
        u'address': address
    })

    #  todo: add check for dupliacy here, currently duplicate address cann live for a user
    #  this new address document_id is always unique, so it is not possible to tell if there
    #  is duplicaty of address based on this
    user_ref = db.collection(u'users').document(user_document_id)
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
def deleteAddressUser(user_document_id, address_id):
    user_ref = db.collection(u'users').document(user_document_id)
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
def reviveAddressUser(user_document_id, address_id):
    user_ref = db.collection(u'users').document(user_document_id)
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
def changePrimaryAddressUser(user_document_id, address_id):
    user_ref = db.collection(u'users').document(user_document_id)
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
def getUserAddressVendor(user_document_id):
    pass

def validateCredVendor(user_document_id, password):
    pass


#  utility functions
#  supply a valid user_document_id
#  todo: use utilitity functions in above APIs, we can even optimize further by giving info that
#  we have already fetched from firebase so that we don't have to fetch it again

def getDocumentIdOfUser(username):
    users = db.collection(u'users').stream()
    for user in users:
        user_data = user.to_dict()
        if user_data["username"] == username:
            return user.id
    return ""

def getUserInfo(user_document_id):
    user_ref = db.collection(u'users').document(user_document_id)
    user_info = user_ref.get().to_dict()
    return user_info

#  supply a valid user_document_id
def getActiveAddressIds(user_document_id):
    user_info = getUserInfo(user_document_id)
    return user_info["active-addresses"]

#  supply a valid user_document_id
def getInactiveAddressIds(user_document_id):
    user_info = getUserInfo(user_document_id)
    return user_info["inactive-addresses"]

#  supply a valid user_document_id
def getPrimaryAddressId(user_document_id):
    user_info = getUserInfo(user_document_id)
    return user_info["primary-address"]

def getAddressFromId(address_id):
    address_ref = db.collection(u'addresses').document(address_id)
    address_info = address_ref.get().to_dict()
    return address_info["address"]

def getActiveAddresses(user_document_id):
    active_address_ids = getActiveAddressIds(user_document_id)
    active_addresses = []
    for address_id in active_address_ids:
        active_addresses.append(getAddressFromId(address_id))
    return active_addresses

def getInactiveAddresses(user_document_id):
    inactive_address_ids = getInactiveAddressIds(user_document_id)
    inactive_addresses = []
    for address_id in inactive_address_ids:
        inactive_addresses.append(getAddressFromId(address_id))
    return inactive_addresses

def getPrimaryAddress(user_document_id):
    primary_address_id = getPrimaryAddressId(user_document_id)
    if primary_address_id:
        return getAddressFromId(primary_address_id)
    return ""

def getIdAddressMap(user_document_id, address_type):
    if address_type == "ACTIVE":
        map_id_active_address = {}
        active_address_ids = getActiveAddressIds(user_document_id)
        for address_id in active_address_ids:
            map_id_active_address[address_id] = getAddressFromId(address_id)
        return map_id_active_address
    elif address_type == "INACTIVE":
        map_id_inactive_address = {}
        inactive_address_ids = getInactiveAddressIds(user_document_id)
        for address_id in inactive_address_ids:
            map_id_inactive_address[address_id] = getAddressFromId(address_id)
        return map_id_inactive_address
    else:
        raise Exception("address_type should be either ACTIVE or INACTIVE")



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

#  print(validateCredUser("kaushik-new-username", "kaushik-password"))

#  print(getActiveAddresses("kaushik-new-username"))
#  print(getInactiveAddresses("kaushik-new-username"))
#  print(getPrimaryAddress("kaushik-new-username"))

#  print(getIdAddressMap("kaushik-new-username", "INACTIVE"))
#  print(getIdAddressMap("kaushik-new-username", "ACTIVE"))

#  signUpUser("Prabin", "Sapkota", "ps@gmail.com", "2028484998", "prabinspkt", "prabin-password")
#  signUpUser("Prabin", "Sapkota", "ps@gmail.com", "2028484998", "ps", "prabin-password")
#  signUpUser("Prabin", "Sapkota", "random@gmail.com", "2028484998", "prabinspkt", "prabin-password")

#  note the argument is user_document_id, not username
#  changeUsernameUser("iiGbVTaYWHsv4p26OPam", "ps")
#  changeEmailUser("iiGbVTaYWHsv4p26OPam", "changed-prabin-email@gmail.com")

#  changeUsernameUser("iiGbVTaYWHsv4p26OPam", "seth")
#  changeEmailUser("iiGbVTaYWHsv4p26OPam", "kmishra@gmail.com")
