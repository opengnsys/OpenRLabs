# -*- coding: utf-8 -*-

def get_day(num_day):
    if num_day == 0:
        return 'Lunes'
    if num_day == 1:
        return 'Martes'
    if num_day == 2:
        return 'Miércoles'
    if num_day == 3:
        return 'Jueves'
    if num_day == 4:
        return 'Viernes'
    if num_day == 5:
        return 'Sábado'
    if num_day == 6:
        return 'Domingo'
    
    return 'Error'

db.define_table('labs_timetable',                                
                Field('lab_id', 'integer', required = True, readable = False),                              
                Field('lab_name', required = True),
                Field('Init_Day', 'integer', required = True, requires = IS_IN_SET({0 : 'Lunes', 1 : 'Martes', 2: 'Miércoles', 3: 'Jueves', 
                                                                         4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}, zero=None),
                                                    represent = lambda result, row: get_day(row.Init_Day)),                                                    
                Field('End_Day', 'integer', required = True, requires = IS_IN_SET({0 : 'Lunes', 1 : 'Martes', 2: 'Miércoles', 3: 'Jueves', 
                                                                         4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}, zero=None),
                                                    represent = lambda result, row: get_day(row.End_Day)),                                                
                Field('Init_time', 'time', required=True, default='08:00', requires = IS_TIME(error_message='must be HH:MM:SS!')),
                Field('End_time', 'time', required=True, default='22:00', requires = IS_TIME(error_message='must be HH:MM:SS!')),
                Field('cod_asign', default=None),
                )
                



