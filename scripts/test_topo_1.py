#!/usr/bin/python

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi


def topology():
   
    net = Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP)

    info("*** Creamos los nodos de la topologia\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8',
                          range=20, position='10,20,0')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.3/8',
                          range=20, position='50,20,0')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1',
                             position='15,30,0', range=30)
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mode='g', channel='6',
                             position='55,30,0', range=30)
    c1 = net.addController('c1', controller=Controller)

    #Config nodos   
    info("*** Configuramos los nodos de la topologia\n")
    net.configureWifiNodes()
    net.setAssociationCtrl('ssf')

    #Matplotlib dibujo 
    net.plotGraph(max_x=100, max_y=100)

    #Enlaces 
    info("*** Creamos los links\n")
    net.addLink(ap1, ap2)
    net.addLink(ap1, sta1)
    net.addLink(ap2, sta2)

    info("*** Arrancar la red\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    info("*** MininetWifi CLI ...\n")
    CLI_wifi(net)

    info("*** Parar la red\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
