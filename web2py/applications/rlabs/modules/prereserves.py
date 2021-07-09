# -*- coding: utf-8 -*-
#################################################################################
# @file    prereserves.py
# @brief   
# @warning None
# @note Use: None     
# @license GNU GPLv3+
# @author  David Fuertes, EUPT, University of Zaragoza.
#          Opengnsys Api Rest support provided by Juan Carlos García, EUPT, University of Zaragoza.
# @version 1.1.0 - First version
# @date    2019-15-11
#################################################################################

from gluon.storage import Storage

from datetime import datetime, timedelta

from ognsys import Ognsys
from client_lab import Client
from ados import adoDB_reserves, adoDB_users, adoDB_openRlabs_setup, adoDB_services, adoDB_prereserves

class Reserve:
    def __init__(self, db, reserve_db, context_pre) -> None:         
        self.TIME_TO_BOOT =  timedelta(seconds=adoDB_openRlabs_setup.get_seconds_to_wait_reserve(db))
        

        self.db = db     

        self.context = Storage()
        
        # Rellenamos context
        for k,v in context_pre.items():
            self.context[k] = v        
        

        self.opengnsys = Ognsys(db)
        self.opengnsys.set_apikey(self.context['ou_id'])        
                        
        self.__set_context()

        if reserve_db:
            self.__set_context_from_reserve_db(reserve_db)

        self.client = Client(self.context)
    
    def __set_context_from_reserve_db(self, reserve_db):        
        self.context['id'] = reserve_db['id']
        self.context['pc_id'] = reserve_db['pc_id']
        self.context['image_id'] = reserve_db['image_id']
        self.context['ip'] = reserve_db['ip']        
        self.context['reserved_init_time'] = reserve_db['reserved_init_time']        

    def __set_context(self):
        service = adoDB_services.get_service_by_id(self.db, self.context['protocol_id'])

        self.context['maxtime'] = self.__get_maxtime()
        self.context['is_assigned'] = False
        self.context['is_running'] = False
        self.context['reserved_init_time'] = datetime.now()        
        self.context['protocol'] = service['name']
        self.context['port'] = service['port']        
        self.context['expiration_time'] = self.context['finish_time']        
        

    def __get_maxtime(self):
        time_to_finish = self.context['finish_time'] - datetime.now()
        time_to_finish_hours = round(time_to_finish.total_seconds() / 3600)
        if time_to_finish_hours == 0:
            time_to_finish_hours = 1
        return time_to_finish_hours

    def set_host_is_running(self):
        adoDB_reserves.set_is_running_true(self.db, self.context['pc_id'])

    def host_is_not_booting(self):        
        if (datetime.now() - self.context['reserved_init_time']) > self.TIME_TO_BOOT:
            return True
        else:
            return False

    def remove(self):
        self.client.unreserve_remote_pc()        


    def hosts_reserve_estropeado(self):
        hosts_status = self.client.get_status_client() 
        if hosts_status == "off" or 'error' in hosts_status:
            return True
        else:
            self.set_host_is_running()
            return False

    def do_host_reserve(self):
        print("reservo hosts")
            
        host = self.client.reserve_remote_pc()        

        if 'id' in host:
            # Rellenamos context pues
            # no existe reserva previa.
            for k,v in host.items():
                self.context[k] = v        
            
            print('insert reserva')                    
            adoDB_reserves.insert(self.context)
                            

            self.client.update_context(self.context)
            
            print('eventos redirigidos')            
            self.client.redirect_events()            
            print('register timeout')            
            self.client.register_session_timeout()

            

class PreReserve:

    def __init__(self, db ,prereserve_in_db) -> None:
        self.TIME_TO_DECREASE = timedelta(minutes=20)
        self.MAX_ATTENPTED_BOOTS = 1

        self.db = db

        self.prereserve_in_db = prereserve_in_db

        self.context = Storage()
        
        self.__set_context(prereserve_in_db)

        self.reserves = []
        self.__populate_reserves()

    def __set_context(self, prereserve_in_db):
        self.context['db'] = self.db
        self.context['user_id'] = adoDB_users.get_admin_id(self.db)
        self.context['ou_id'] = prereserve_in_db['ou_id']
        self.context['lab_id'] = prereserve_in_db['lab_id']
        self.context['prereserve_id'] = prereserve_in_db['id']  
        self.context['image_id'] = prereserve_in_db['image_id']
        self.context['num_reserves'] = prereserve_in_db['num_reserves']        
        self.context['init_time'] = prereserve_in_db['init_time']
        self.context['finish_time'] = prereserve_in_db['finish_time']
        self.context['last_decreased_time'] = prereserve_in_db['last_decreased_time']
        self.context['attempted_boots'] = prereserve_in_db['attempted_boots']
        self.context['protocol_id'] = prereserve_in_db['protocol']
        

    def __increase_num_attempted(self):        
        self.prereserve_in_db.update_record(attempted_boots=self.prereserve_in_db['attempted_boots'] + 1)
        self.db.commit()
        
        self.context['attempted_boots'] = self.prereserve_in_db['attempted_boots']

    def __decrease_num_hosts(self):
        if datetime.now() - self.context['last_decreased_time'] > self.TIME_TO_DECREASE:
            print('decremento yes')
            self.prereserve_in_db.update_record(num_reserves=self.prereserve_in_db['num_reserves'] - 1,
                            last_decreased_time=datetime.now(),
                            attempted_boots=0)

            self.db.commit()
            self.context['last_decreased_time'] = self.prereserve_in_db['last_decreased_time']


        return self.prereserve_in_db['num_reserves']

    ## 
    #  NOTA: Podriamos obtener reservas NO ASIGNADAS, en cuyo caso 
    #        la app SIEMPRE ofrecería n hosts disponibles. Es decir,
    #        al ocuparse un hosts, se levantaría otro.
    ##
    def __populate_reserves(self):
        reserves_by_lab_db = adoDB_reserves.get_by_lab_PreR(self.db, self.context['prereserve_id'], self.context['lab_id'])
        
        for reserve_db in reserves_by_lab_db:            
            reserve = Reserve(self.db, reserve_db, self.context)
            self.reserves.append(reserve)


    def get_reserves(self):
        return self.reserves

    def expired(self):
        if self.context['finish_time'] < datetime.now():
            return True
        else:
            return False
    def is_in_time(self):
        if self.context['init_time'] < datetime.now() < self.context['finish_time']:
            return True
        else:
            return False
    
    def remove(self):        
        for reserve in self.reserves:          
            reserve.remove()
        adoDB_prereserves.remove_by_id(self.db, self.context['prereserve_id'])

    def __remove_n_reserves(self, n):                
        for reserve in self.reserves:
            if reserve.context['is_assigned'] == False and n < 0:                
                reserve.remove()
                n = n + 1


    def do_reserves(self):        
        num_hosts_desired = self.context['num_reserves']
        num_hosts_up = 0
        for reserve in self.reserves:
            if reserve.host_is_not_booting():                
                if reserve.hosts_reserve_estropeado(): 
                    print('estropeado')          
                    reserve.remove()
                    if ( datetime.now()  - self.context['last_decreased_time']) > self.TIME_TO_DECREASE:
                        print('timepo decremento pasado')
                        if self.context['attempted_boots'] > self.MAX_ATTENPTED_BOOTS:
                            print('decremento host')
                            num_hosts_desired = self.__decrease_num_hosts()
                        else:
                            print('incrmento num intentos')
                            self.__increase_num_attempted()

                else:
                    reserve.set_host_is_running()                    
                    num_hosts_up = num_hosts_up + 1
            else:
                num_hosts_up = num_hosts_up + 1
                
        if num_hosts_desired - num_hosts_up > 0:
            for i in range(num_hosts_desired - num_hosts_up):
                reserve = Reserve(self.db, None, self.context)
                self.reserves.append(reserve)
                reserve.do_host_reserve()
        
        if num_hosts_desired - num_hosts_up < 0:
            self.__remove_n_reserves(num_hosts_desired - num_hosts_up)
