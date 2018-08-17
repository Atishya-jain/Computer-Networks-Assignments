#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

#Defining the Net from scratch
def emptyNet(dl, baw, ls, qs):

    #Conditioning parameters to be as per user or default values if user provided minimum/maximum values
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
    # Run mininet
    #######################################
    net = Mininet( topo=None, build=False, link=TCLink, host=CPULimitedHost )

    info( '*** Adding controller\n' )
    net.addController('c0', controller=RemoteController,ip="127.0.0.1",port=6633)

    #A dummy host to attach with controller and then connect that host with a switch
    h0 = net.addHost('h0', ip='127.0.0.1')

    info( '*** Adding hosts\n' )
    host = []
    switch = []
    for i in range(10):
      host.append(net.addHost('h' + str(i+1)))	

    for i in range(10):
      switch.append(net.addSwitch('s' + str(i+1), cls=OVSSwitch))

    info( '*** Creating links\n' )
    ## controller - switch (s1)
    net.addLink( h0, switch[0] )

    ## host - switch
    for i in range(10):
      net.addLink(host[i], switch[i],bw=baw,loss=ls,max_queue_size=qs,delay=dl)

    ## switche links
    for index in range (0, 10):
      for index2 in range(index+1, 10):
        net.addLink(switch[index],switch[index2], bw=baw,loss=ls,max_queue_size=qs,delay=dl)

    info( '*** Starting network\n')
    net.start()

    # Set ip address to switch
    for i in range (10):
      switch[i].cmd('ifconfig s' + str(i+1) + ' 10.0.1.' + str(i+1))

    info('*** Enable spanning tree\n')
    for i in range(10): 
      switch[i].cmd('ovs-vsctl set bridge s' + str(i+1) + 'stp-enable=true')

    #Starting up the mininet CLI for testing
    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    # Get user inputs to various parameters
    setLogLevel( 'info' )
    delay = input("Enter Delay to introduce in ms(Enter 0 for default): ")
    bw = input("Desired bandwidth in Mbps (0-1000: 1000 for default): ")
    loss = input("Enter loss % (0-100: 0 for default): ")
    qs = input("enter max_queue size (0-1000: 1000 for default): ")

    #Call the function to build the net
    emptyNet(float(delay), float(bw), float(loss), float(qs))
