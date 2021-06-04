# -*- coding: utf-8 -*-

db.auth_user.id.readable = False
db.auth_user.password.readable = False
db.auth_user.password.writable = False

db.auth_user.email.unique = True # Only works on forms


db.auth_membership.id.readable = False




def enable_user(row, id):
    enabled_id = db(db.auth_group.role == 'enabled').select().first()['id']
    db.auth_membership.insert(user_id = id,
                              group_id = enabled_id)



db.auth_user._after_insert.append(lambda row, id: enable_user(row, id))



def reset_passwd(row):
    user_id = row.select().first()["user_id"]    
    db(db.auth_user.id == user_id).update(password = None)


db.auth_membership._before_delete.append(lambda row: reset_passwd(row))