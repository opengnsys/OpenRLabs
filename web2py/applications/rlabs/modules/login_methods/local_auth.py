

def local_auth(db):

    def local_auth_aux(username,
                        password,
                        db=db):
        
        user = db(db.auth_user.username==username).select().first()
        if (db.auth_user.password.validate(password) == (user.password, None)):
            return True
        else:
            return False
        
    return local_auth_aux
