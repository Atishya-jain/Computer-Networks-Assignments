#!/usr/bin/python


from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections

def emptyNet(dl, baw, ls, qs):
    if dl == 0:
      dl = None
    else:
      dl = str(dl) + 'ms'
    if baw == 1000:
      baw = None
    if ls == 0:
      ls = None
    if qs == 1000:
      qs = None

    #######################################
    # Constants
    #######################################

    #######################################
    # Run mininet
    #######################################
    net = Mininet( topo=None, build=False,host=CPULimitedHost,link=TCLink )

    info( '*** Adding controller\n' )
    net.addController('c0',ip="127.0.0.1",port=6633)
    h0 = net.addHost('h0', ip='127.0.0.1')

    info( '*** Adding hosts\n' )
    host = []
    switch = []
    for i in range(10):
      host.append(net.addHost('h' + str(i+1)))	

    for i in range(1):
      switch.append(net.addSwitch('s' + str(i+1), cls=OVSSwitch))

    info( '*** Creating links\n' )
    ## controller - switch (s1)
    net.addLink( h0, switch[0] , bw=baw, loss=ls, delay=dl, max_queue_size=qs)

    ## host - switch
    for i in range(10):
      net.addLink(host[i], switch[0], bw=baw, loss=ls, delay=dl, max_queue_size=qs)

    ## switches
    info( '*** Starting network\n')
    net.start()

    #info('*** Set ip address to switch\n')
    for i in range (1):
      switch[i].cmd('ifconfig s' + str(i+1) + ' 10.0.1.' + str(i+1))

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    delay = input("Enter Delay to introduce in ms: ")
    bw = input("Desired bandwidth in Mbps: ")
    loss = input("Enter loss %: ")
    qs = input("enter max_queue size: ")
    emptyNet(float(delay), float(bw), float(loss), float(qs))