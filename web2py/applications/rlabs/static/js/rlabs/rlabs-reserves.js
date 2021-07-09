class TrReserves {
    constructor(reserve, table) {        
        this.table = table;
        this.tr = '	<tr class="active_reserves_tr"></tr>';

        this.reserve = reserve;   

    }

    td1_html(){
        let html = '<img id="img_connect_reserve_' + this.reserve['id'] + '" ' +
                        'class="status_equipo active_reserve_status" data-status="' + this.reserve['status'] + '" ' +
                        'data-loggedin="' + this.reserve['loggedin'] + '" ' +
                        'src="../static/images/odernador_WIN.png"></img>';
        return html
    }

    td2_html(){
        let html = '<span>' + this.reserve['pc_name'] + '</span>';
        return html
    }

    td3_html(){
        let html = '<span><img class="image_user" src="../static/images/user.png"></span>';
        return html
    }

    td4_html(){
        let html = '<span>' + this.reserve['user_id'] + '</span>';
        return html
    }

    td5_html(){
        let html = '<span><button id="btn_connect_reserve_' + this.reserve['id'] + '" ' +
                                'type="button" class="btn btn-secondary btn-client-connect" ' +
                                'onclick="connect_remotePC(event)" ' +
                                'data-reserve_id="' + this.reserve['id'] + '" ' +
                                'data-sound="on" ' +
                                'data-pc_id="' + this.reserve['pc_id'] + '" ' +
                                'data-lab_id="' + this.reserve['lab_id'] + '" ' +
                                'data-ou_id="' + this.reserve['ou_id'] + '" ' +
                                'data-pc_name="' + this.reserve['pc_name'] + '" ' +
                                'data-port="' + this.reserve['port'] + '" ' +
                                'data-protocol="' + this.reserve['protocol'] + '" ' +
                                'data-ip="' + this.reserve['ip'] +'">Conectar</button></span>' +                                                                                        
                    '<span><button type="button" class="btn btn-primary" ' +
                                'onclick="unreserve(event)" ' +
                                'data-reserve_id="' + this.reserve['id'] + '" ' +
                                'data-pc_id="' + this.reserve['pc_id'] + '" ' +
                                'data-lab_id="' + this.reserve['lab_id'] + '" ' +
                                'data-ou_id="' + this.reserve['ou_id'] + '">Cancelar</button></span>'

                        

        
        //console.log(html)

        return html
    }


    insert_tr(){
        //console.log(this.reserve)        
        let tbody = this.table.getElementsByTagName('tbody')[0]
        let row = tbody.insertRow();
        row.setAttribute("class", "active_reserves_tr");
        let td1 = row.insertCell();
        let td2 = row.insertCell();
        let td3 = row.insertCell();
        let td4 = row.insertCell();
        let td5 = row.insertCell();
        td1.innerHTML = this.td1_html();
        td2.innerHTML = this.td2_html();
        td3.innerHTML = this.td3_html();
        td4.innerHTML = this.td4_html();
        td5.innerHTML = this.td5_html();
        


                    
    }


}

class ReservesObserver {

    constructor(url_reserves, url_status, table) {
        this.AWAIT_TIME_MS = 10000;

        this.url = url_reserves;

        this.table = table;
        
        this.statusObserver = new StatusObserver(url_status);

        this.reserves = null;

        this.xhr = new XMLHttpRequest();

        this.interval = null;

    }
    clear_table_reserves(){        
        delete_by_class('active_reserves_tr');        
    }

    populate_table_reserves(){        
        if (this.reserves !== null){
            //console.log(this.reserves)
            for ( i=0; i < this.reserves.length; i++ ) {
                let reserve = new TrReserves(this.reserves[i], this.table);
                reserve.insert_tr()                
            }
        }        

    }

    set_status_clients(){        
        this.statusObserver.set_clients(document.getElementsByClassName('btn-client-connect'))
        this.statusObserver.check_status_clients();
    }

    set_reserves() {        
        this.xhr.open("POST", this.url, true);    	
        this.xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');                
        this.xhr.send();   

        // Uso funcion flecha porque hacienco function() { ....}, "this"
        // pasaría a ser el entorno de function.
        this.xhr.onreadystatechange = () => {
            this.xhr.onreadystatechange = () => {
                if (this.xhr.readyState == 4 && this.xhr.status == 200) {        	
                    this.reserves = JSON.parse(this.xhr.responseText);
                    this.clear_table_reserves();
                    this.populate_table_reserves();
                    this.set_status_clients();
                } 
            }             
        }
         
    }

    run() {        
        this.set_reserves()
        this.interval = setInterval( this.set_reserves.bind(this) , this.AWAIT_TIME_MS);					                
    }

    stop() {        
        clearInterval(this.interval);
    }


}
