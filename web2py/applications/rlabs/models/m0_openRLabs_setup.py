# -*- coding: utf-8 -*-

db.define_table('active_directory',
                Field('admin_ad', required=True),
                Field('password', type='password', required=True, requires=CRYPT()),
                Field('server_ad', required=True),
                Field('base_db', required=True),
                )

db.define_table('pop3_server',
                Field('url', required=True),
                Field('port', 'integer', required=True),
                Field('use_tls', type='boolean', required=True, default=True),
                )

db.define_table('openRLabs_setup',
                Field('URL_Apache_Guacamole_WebSocket', required=True),
                Field('URL_openGnsys_server', required=True),
                Field('URL_openRLabs_server', required=True),
                Field('auth_mode', requires = IS_IN_SET(['active_directory', 'pop3_server'], 
                                                        zero=None)),
                Field('maxtime_reserve', required=True, default='2'),
                Field('seconds_to_wait', required=True, default=200)
                )

if db(db.openRLabs_setup).isempty():
    import load_init_setup
    
    load_init_setup.load_setup(db)
#Ensure only one record
def only_one_record(table):
    first = db(db[table].id > 1).select().first()
    
    if first:
        db(db[table].id != first['id']).delete()
        
    db[table].id.readable = False
    

only_one_record('active_directory')
only_one_record('pop3_server')
only_one_record('openRLabs_setup')    
