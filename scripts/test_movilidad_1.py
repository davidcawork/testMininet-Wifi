#!/usr/bin/python



from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI_wifi



def topo():


	net = Mininet_wifi(controller= Controller, accessPoint = OVSKernelAP)
	
	info("*** Creando nodos\n")
	h1 = net.addHost( 'h1', mac='00:00:00:00:00:01',ip='10.0.0.1/8') 
	sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02',ip='10.0.0.2/8', range ='20')
	ap1 = net.addAccessPoint('ap1', ssid = 'ap1-ssid', mode='g', channel= '1', position='30,50,0', range='30')
	ap2 = net.addAccessPoint('ap2', ssid = 'ap2-ssid', mode='g', channel= '1', position='90,50,0', range='30')
	ap3 = net.addAccessPoint('ap3', ssid = 'ap3-ssid', mode='g', channel= '1', position='150,50,0', range='30')
	c1 = net.addController('c1' , controller = Controller)

	info("*** Configurando nodos\n")
	net.configureWifiNodes()


	info("*** Creando links\n")
	net.addLink(ap1, h1)
	net.addLink(ap1, ap2)
	net.addLink(ap2,ap3)

	info("*** Dibujando Topo con matplotlib\n")
	net.plotGraph(max_x=200, max_y = 200)

	info("*** Configurando Movilidad (sta1)\n")
	net.startMobility(time = 0, AC='ssf')
	net.mobility(sta1, 'start', time = 20, position='1,50,0')
	net.mobility(sta1, 'stop', time = 79, position='159,50,0')
	net.stopMobility(time=200)

	info("*** Network UP!\n")
	net.build()
	c1.start()
	ap1.start([c1])	
	ap2.start([c1])	
	ap3.start([c1])	

	info("*** Cargamos Mininet-Wifi CLI\n")
	CLI_wifi(net)

	info("*** Parando network\n")
	net.stop()


if __name__ == '__main__':
	setLogLevel('info')
	topo()

















