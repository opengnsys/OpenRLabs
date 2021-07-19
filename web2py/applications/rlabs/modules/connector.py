# -*- coding: utf-8 -*-
#################################################################################
# @file    cnection_stage.py
# @brief   Module that manage connection stages with remotePC    
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################
from gluon import current

from gluon.storage import Storage

import json
from datetime import datetime, timedelta
import time

from client_lab import Client
from ados import adoDB_reserves, adoDB_openRlabs_setup
import errors


class Connection:            
        
    def __init__(self, my_context):

        self.my_context = Storage()

        # Rellenamos context
        for k,v in my_context.items():
            self.my_context[k] = v
        
        
        self.client = Client(self.my_context)
        
        self.WAIT_CHECK_LOOP = 10
        self.MAX_RETRIES = int((adoDB_openRlabs_setup.getSetup_OpenRLabs(my_context['db'])['seconds_to_wait'] / self.WAIT_CHECK_LOOP) - 1)
        
     
    def do_assign_reserve(self):        
        reserve = adoDB_reserves.get_available_hosts(self.my_context.db,self.my_context['lab_id'], 
                                                self.my_context['image_id']).first()
        if reserve:
            reserve.update_record(user_id=self.my_context['user_id'],
                                is_assigned = True,
                                assigned_init_time = datetime.now())

            self.my_context.db.commit()                 

            equipo_reservado = {}
            equipo_reservado['id'] = reserve['pc_id']
            equipo_reservado['name'] = reserve['pc_name']
            equipo_reservado['ip'] = reserve['ip']
            equipo_reservado['mac'] = reserve['mac']
            equipo_reservado['protocol'] = reserve['protocol']
            equipo_reservado['port'] = reserve['port']
            equipo_reservado['ou_id'] = reserve['ou_id']
            equipo_reservado['lab_id'] = reserve['lab_id']
                    
            #Por compatibilidad con el resto de la app
            #Que usa pc_id por claridad.
            equipo_reservado['pc_id'] = equipo_reservado['id']
                        

            return equipo_reservado
        else:
            return None
            


    def do_reserve(self):
        print('reserve remote PC')
        equipo_reservado= None
        # Al hacer reserva se manda arrancar el equipo y se crea entrada en cola acciones para levantar el equipo
        # deseado.
        equipo_reservado = self.client.reserve_remote_pc()        
        print("equipo_reservado en opengnsys")
        ####
        ## COMPROBAR FORMATO RESPUESTA VALIDA Y CHEQUEAR QUE CONTIENE TODOS LOS CAMPOS NECESARIOS
        ###
        if 'id' not in equipo_reservado:        
            return {'error': '\n ' + errors.ERROR_RESERVA}        
        else:
            if equipo_reservado:                
                for k,v in equipo_reservado.items():
                    self.my_context[k] = v

                expiration_time = datetime.now() + timedelta(hours=int(self.my_context.maxtime))
                #expiration_time = expiration_time.strftime('%d/%m/%Y %H:%M:%S')
                            
                self.my_context.expiration_time = expiration_time

                self.my_context.reserved_init_time = datetime.now()
                self.my_context.assigned_init_time = datetime.now()
                self.my_context.is_assigned = True

                print('insert reserva')
                try:           
                    adoDB_reserves.insert(self.my_context)
                except:                    
                    return {'error': '\n Error de reserva. No es posible registrar reserva en openrlabs'}
                
                self.client.update_context(self.my_context)
                
                print('eventos redirigidos')
                self.client.redirect_events()
                    
                print('register timeout')            
                self.client.register_session_timeout()
                
        
                '''
                print('setup_task')
                gestor_de_reservas.setup_task(opengnsys.__OPENGNSYS_SERVER__, opengnsys.__APIKEY__, 
                                                        ou_id, lab_id, pc_id, ip, int(maxtime))
                '''            
                # Devolvemos todos los datos necesarios para poder hacer conexion a 
                # escritorio remoto.
                
                              
                equipo_reservado['client_type'] = self.my_context.client_type
                equipo_reservado['protocol'] = self.my_context.protocol
                equipo_reservado['port'] = self.my_context.port
                equipo_reservado.update({'ou_id' : self.my_context.ou_id, 'ou' : None,
                                         'lab_id': self.my_context.lab_id, 'lab' : None,
                                         'num_retries' : self.my_context.num_retries})
                
                #Por compatibilidad con el resto de la app
                #Que usa pc_id por claridad.
                equipo_reservado['pc_id'] = equipo_reservado['id']
        
                return {'status': '\n Reserva realizada. Equipo concedido: ' + equipo_reservado['name'] + 
                        '\n Arrancando equipo: ../',
                        'equipo_reservado': equipo_reservado}
            else:        
                return {'error': '\n Error de reserva.'}

    def check_pc_status(self):
        print('cheking..')
        ou_id = str(self.my_context.ou_id)
        lab_id = str(self.my_context.lab_id)
        pc_id = str(self.my_context.id)
        pc_name = str(self.my_context.name)
        ip = str(self.my_context.ip)
        protocol = str(self.my_context.protocol)
        port = str(self.my_context.port)
        client_type = str(self.my_context.client_type)
        
        num_retries = int(self.my_context.num_retries)
                
        if num_retries < self.MAX_RETRIES:

            #time.sleep( self.WAIT_CHECK_LOOP )

            self.my_context.num_retries = str(num_retries + 1)

            pc_status = self.client.get_status_client()            

            if 'status' not in pc_status: 
                pc_status['status'] = 'error'
                
            if pc_status['status'] == 'off' or pc_status['status'] == 'oglive' \
               or pc_status['status'] == 'busy' or pc_status['status'] == 'error':
                                
                return {'status' : '.../',
                        'equipo_reservado' : self.my_context,
                        'wait_to_check' : self.WAIT_CHECK_LOOP}
            else:

                adoDB_reserves.set_is_running_true(self.my_context.db, pc_id)

                return {'ip': ip, 'protocol': protocol, 'port': port, 
                       'pc_id': pc_id,'pc_name' : pc_name, 
                       'ou_id': ou_id, 'lab_id': lab_id,
                       'finalizado': True,
                       'client_type': client_type,
                       'status' : '\n Conexión realizada con éxito.'}
        else:        
                
            self.client.unreserve_remote_pc()
                         
            return {'error': 'Fallo al encender el equipo de forma remota.\n Intentelo con otro equipo.'}
          
       
            