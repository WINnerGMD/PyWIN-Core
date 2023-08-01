import bcrypt

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), b'$2b$12$VWAACqVFSNt8bIiWVXdsyO').decode()




