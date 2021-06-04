OpenRLabs v1.1.1 - 28 Julio 2020 - Copyright 2020 David Fuertes.


INTRODUCCIÓN


OpenRLabs es una aplicación Open Source, que utiliza la funcionalidad ofrecida 
por opengnsys a traves de su API REST para el acceso a escritorio 
remoto mediante un navegador web.

OpenRLAbs es una aplicación modular que utiliza como principales componentes:

 - Servidor de opengnsys: Se encarga del arranque, parada y reserva de los equipos.
 - Servidor Apache Guacamole: Se encarga de realizar la conexión a escritorio remoto (RDP, VNC...) y
			      trasladarlo a HTML5 para su uso en un navegador Web.
 - Servidor de web2py: Se encarga de usar las funcionalidades de las aplicaciones opengnsys y 
		       Apache Guacamole para mostrar los equipos disponibles, arrancarlos y conectarse
                       al escritorio remoto via web. También ofrece chequeo de estado, calendarización 
		       de disponibilidad de los laboratorios, gestión de sonido, ...etc.


En este repositorio se encuentran las siguientes carpetas:
 - web2py: Contiene el framework de python we2py y la aplicación openrlabs.
 - deploy: Se encuentran los instaladores de la aplicación.
 - guacamole-websocket: Contiene el código del servlet creado para la conexión con
			el servidor Guacamole.

PRE-REQUISITOS

Para hacer funcionar la aplicación ser necesita un sistema LINUX con:

 - Framework web2py.
 - Servidor web.
 - Servidor aplicaciones Java.

Durante el proceso de instalción se instalan y configuran todos los componentes
necesarios para poder ejecutar la aplicación.

El instalador ha sido testado en Ubuntu Server 18.04

INSTALACIÓN

Las instrucciones para la instalación se encuetran en el fichero 'LEEME.txt' de los instaladores.

Los instaladores están dentro de la carpeta 'deploy'.

Además del repositorio, es posible descargar el instalador en formato rlabs_installer_'fecha.hora'.tar.gz
de la web: 

openrlabs.es

PROBLEMAS DETECTADOS Y LIMITACIONES

La aplicación funciona correctamente con
el navegador Google Chrome.

Puede funcionar también en Mozilla Firefox,
pero se recomienda leer en el WIKI -> FAQs las
medidas a tener en cuenta.

En otros navegadores no ha sido testado.


WIKI

Toda la documentación es encuentra en:

wiki.openrlabs.es


CONTACTO

<dfuertes@unizar.es>
<jcgarcia@unizar.es>


DETALLES DE LA LICENCIA


openrlabs is released under the GNU General Public License,
version 3 or later. See file "COPYING" for full license text.

In compliance with the terms of the GPL, a full source distribution 
(openrlabs and all included libraries) is available at 
<http://openrlabs.es>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


