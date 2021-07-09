# -*- coding: utf-8 -*-

db.define_table('nip_groups',
                Field('nip', required = True, unique = True),
                Field('groups', 'text', required = True)
                )                            
