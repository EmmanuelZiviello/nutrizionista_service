import bcrypt


def check_pwd(not_hashed_password, hashed_password):
    return bcrypt.checkpw(not_hashed_password.encode('utf_8'), hashed_password)


def hash_pwd(password) -> bytes:
    # diminuire gensalt se l'app rallenta
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

    return hashed