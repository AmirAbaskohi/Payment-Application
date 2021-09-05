import hashlib, binascii, os

def hash(string):
    # Salt is a randomly generated string that is joined with the password before hashing
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # Compute their hash and then convert it into a string with 
    pwdhash = hashlib.pbkdf2_hmac('sha512', string.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    # Restoring salt and hash
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    # Making the hash of new password
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    # Check if they work correctly
    return pwdhash == stored_password