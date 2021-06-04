# -*- coding: utf-8 -*-
#################################################################################
# @file    import_users.py
# @brief   Module that manage info about client (remote PCs), from Opengnsys API Rest    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from ados import adoDB_users

def insert(file_stream, db):
    datos = {}
    error = False
    info_already_insert = ''
    count_insert = 0
    for line in file_stream.decode("utf-8").split('\n'):
        if ',' in line:
            separator_char = ','
        if ';' in line:
            separator_char = ';'
            
        if '@' in line:
            line = line.strip().strip('\n').strip('"')
            datos['first_name'] = line.split(separator_char)[0]
            datos['last_name'] = line.split(separator_char)[1]
            datos['email'] = line.split(separator_char)[2]            
            if '@' not in datos['email']:
                error = True
                info_insert = 'Error, usuario ' + datos['name'] + 'formato de email incorrecto'
                break
            
            datos['username'] = line.split(separator_char)[3]
            
            found = db(db.auth_user.username == datos['username']).count()
            #check user not exits
            if found == 0:
                adoDB_users.insert_user(db, datos['first_name'], datos['last_name'],
                                   datos['email'], datos['username'])
                count_insert = 1 + count_insert
            else:
                info_already_insert = '\n Algunos usuarios no se han importado porque ya existia su username.' 
    
    info_insert = " " + str(count_insert) + ' usuarios insertados' + info_already_insert                                          
                        
    if error:
        db.rollback()
        return info_insert
    else:
        db.commit()
        return 'Importación realizada con exito.' + info_insert