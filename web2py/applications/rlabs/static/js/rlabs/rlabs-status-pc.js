
class StatusObserver {
    constructor(url) {
        this.AWAIT_TIME_MS = 10000;

        this.url = url
        this.clients_to_connect_html = null;

        this.data_clients = {}

        this.xhr = new XMLHttpRequest();

        this.interval = null;

    }

    set_clients(clients){
        this.clients_to_connect_html = clients;
    }

    set_status_img_client(reserve_id, respuesta){
        document.getElementById("img_connect_reserve_" + 
                    reserve_id).setAttribute('src', "../static/images/" + getImg_pc(respuesta[reserve_id]));
    }


    set_status_img_clients(respuesta){ 
        for ( i=0; i < this.clients_to_connect_html.length; i++ ) {
            let reserve_id = this.clients_to_connect_html[i]['id'].split('_')[3]
            this.set_status_img_client(reserve_id, respuesta);            
        }
    }
        
    
    do_request(){
        //console.log(this.data_clients)
        this.xhr.open("POST", this.url, true);    	
        //this.xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        
        this.xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        //xmlhttp.send(JSON.stringify({ "email": "hello@user.com", "response": { "name": "Tester" } }));        
        this.xhr.send(JSON.stringify(this.data_clients));           

        // Uso funcion flecha porque hacienco function() { ....}, "this"
        // pasaría a ser el entorno de function.
        this.xhr.onreadystatechange = () => {
            this.xhr.onreadystatechange = () => {
                if (this.xhr.readyState == 4 && this.xhr.status == 200) {        	
                    var respuesta = JSON.parse(this.xhr.responseText);        	
                    this.set_status_img_clients(respuesta);
                    

                } 
            }             
        }
         
    }

    check_status_clients() {        
        for ( i=0; i < this.clients_to_connect_html.length; i++ ) {                
                this.data_clients[this.clients_to_connect_html[i].getAttribute('data-ip')] = this.clients_to_connect_html[i].getAttribute('data-reserve_id');                
            }
        this.do_request();     
    }    

}


