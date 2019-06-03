#!/usr/bin/python

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call

def topo():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    info( '*** Add controlador\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6633)

    info( '*** Add APs\n')
    ap3 = net.addAccessPoint('ap3', cls=OVSKernelAP, ssid='ap3-ssid',
                             channel='1', mode='g', position='772.0,282.0,0')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='1', mode='g', position='227.0,220.0,0')
    ap2 = net.addAccessPoint('ap2', cls=OVSKernelAP, ssid='ap2-ssid',
                             channel='1', mode='g', position='464.0,315.0,0')

    info( '*** Add estaciones Wifi\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1',
                           position='60.0,423.0,0')
    sta2 = net.addStation('sta2', ip='10.0.0.2',
                           position='477.0,500.0,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3',
                           position='881.0,490.0,0')

    info("*** Configuracion del medio\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configurando los nodos\n")
    net.configureWifiNodes()

    info( '*** Add enlaces\n')
    net.addLink(ap1, ap2)
    net.addLink(ap3, ap2)
    
    #Graficamos con matplotlib la topo
    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Empieza la topo\n')
    net.build()

    info( '*** Controladores UP\n')
    for controller in net.controllers:
        controller.start()

    info( '*** APs UP\n')
    net.get('ap3').start([c0])
    net.get('ap1').start([c0])
    net.get('ap2').start([c0])

    info( '*** Post configure nodes\n')
	
    #Entramos en matplotlib
    CLI_wifi(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topo()

