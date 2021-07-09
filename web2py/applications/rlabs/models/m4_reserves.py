# -*- coding: utf-8 -*-
from datetime import datetime

db.define_table('pre_reserves',
                Field('lab_id', 'integer', required = True, readable = False),                
                Field('ou_id', required=True, readable = False),
                Field('lab_name', required = True),
                Field('image_id', required=True, readable = False),
                Field('image_name', required=True),
                Field('protocol', 'reference services', required=True,
                                requires = IS_IN_DB(db, db.services.id, '%(name)s', zero=None),          
                                represent=lambda id, result: db.services[id].name
                                                   ),
                Field('init_time', 'datetime', required=True, widget=SQLFORM.widgets.string.widget),
                Field('finish_time', 'datetime', required=True, widget=SQLFORM.widgets.string.widget),
                Field('last_decreased_time', 'datetime', readable=False, writable=False),
                Field('attempted_boots', 'integer', required=True, default=0, readable=False, writable=False),
                Field('num_reserves', 'integer', required=True, label="Hosts en espera")
            )


def set_last_decreased(row, id):
    db(db.pre_reserves.id == id).update(last_decreased_time=datetime.now())

db.pre_reserves._after_insert.append(lambda row, id: set_last_decreased(row, id))

db.define_table('reserves',
                Field('user_id', 'reference auth_user', required=True,
                      requires = IS_IN_DB(db, db.auth_user.id, '%(first_name)s'),
                      represent=lambda id, result: db.auth_user[id].first_name + " " +
                                                   db.auth_user[id].last_name
                                                   ),
                Field('ou_id', required=True),
                Field('lab_id', required=True),
                Field('pc_id', required=True),
                Field('pc_name', required=True),
                Field('image_id', required=True),                
                Field('expiration_time', 'datetime', required=True),
                Field('ip', required=True, unique=True),
                Field('mac', required=True, unique=True),
                Field('protocol', required=True),
                Field('port', required=True),
                Field('is_running', 'boolean', default=False),
                Field('is_assigned', 'boolean', default=True),
                Field('prereserve_id', 'reference pre_reserves', default=None),
                Field('assigned_init_time', 'datetime'),
                Field('reserved_init_time', 'datetime', required=True),
                )

# Remove all expired reserves
#db(db.reserves.expiration_time < datetime.now()).delete()

rs = db(db.reserves.expiration_time < datetime.now()).select()
for r in rs:
    if r['prereserve_id'] == None:
        r.delete_record()
