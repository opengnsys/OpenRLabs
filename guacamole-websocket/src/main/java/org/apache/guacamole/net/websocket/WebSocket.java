package org.apache.guacamole.net.websocket;

import java.util.Map;
import java.util.List;

import javax.websocket.Session;
import javax.websocket.EndpointConfig;
import javax.websocket.server.ServerEndpoint;

import org.apache.guacamole.GuacamoleException;
import org.apache.guacamole.net.GuacamoleSocket;
import org.apache.guacamole.net.GuacamoleTunnel;
import org.apache.guacamole.net.InetGuacamoleSocket;
import org.apache.guacamole.net.SimpleGuacamoleTunnel;
import org.apache.guacamole.protocol.ConfiguredGuacamoleSocket;
import org.apache.guacamole.protocol.GuacamoleConfiguration;
import org.apache.guacamole.protocol.GuacamoleClientInformation;
import org.apache.guacamole.websocket.GuacamoleWebSocketTunnelEndpoint;

@ServerEndpoint(value = "/tunnel-websocket", subprotocols = "guacamole")
public class WebSocket 
    extends GuacamoleWebSocketTunnelEndpoint {


    @Override
    protected GuacamoleTunnel createTunnel(Session session, EndpointConfig endpointConfig)
				    throws GuacamoleException {

        Map<String, List<String>> parameterMap = session.getRequestParameterMap();
        String ip = parameterMap.get("ip").get(0);
        String protocol = parameterMap.get("protocol").get(0);
        String port = parameterMap.get("port").get(0);
        String username = parameterMap.get("username").get(0);
        String pHeight =  parameterMap.get("height").get(0);
        String pWidth =  parameterMap.get("width").get(0);
        List<String> pAudio = parameterMap.get("audio");

        // Create our client information
        GuacamoleClientInformation info = new GuacamoleClientInformation();

        // Create our configuration
        GuacamoleConfiguration config = new GuacamoleConfiguration();

        
        // Set configuration and client information from parameters
        config.setProtocol(protocol);
        config.setParameter("hostname",ip);
        config.setParameter("port", port);
        config.setParameter("username", username);
        config.setParameter("disable-audio", "false");
        config.setParameter("server-layout", "es-es-qwerty");
        config.setParameter("ignore-cert", "true");
        config.setParameter("resize-method", "reconnect");

        if (pWidth != null) {
            config.setParameter("width", pWidth);
            info.setOptimalScreenWidth(Integer.parseInt(pWidth));
	    }

        if (pHeight != null) {
            config.setParameter("height", pHeight);
            info.setOptimalScreenHeight(Integer.parseInt(pHeight));	
	    }

        // Add audio mimetypes
        if (pAudio != null) info.getAudioMimetypes().addAll(pAudio);

        // Connect to guacd - everything is hard-coded here.
        GuacamoleSocket socket = new ConfiguredGuacamoleSocket(
                new InetGuacamoleSocket("localhost", 4822),
                config, info
        );

    // Return a new tunnel which uses the connected socket
	return new SimpleGuacamoleTunnel(socket);
	
 
	
    }

}
