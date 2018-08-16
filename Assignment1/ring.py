#!/usr/bin/python

"""
   reference: https://www.youtube.com/watch?v=yHUNeyaQKWY

   mesh topology

       s2------s3 ----h2
       | *   * |
       |   *   |
       | *   * |
 h1----s1-----s4------h0(c0) 

 **** To prevent broadcast storm(by arp messages), 
      enable spanning tree in each switch !!!!!

      : in each switch, 
         type "ovs-vsctl set bridge <bridge_name> stp-enable=true"
   
"""

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
    net.addController('c0', controller=RemoteController,ip="127.0.0.1",port=6633)
    h0 = net.addHost('h0', ip='127.0.0.1')

    info( '*** Adding hosts\n' )
    host = []
    switch = []
    for i in range(10):
      host.append(net.addHost('h' + str(i+1)))	

    for i in range(10):
      switch.append(net.addSwitch('s' + str(i+1), cls=OVSSwitch))

    info( '*** Creating links\n' )
    ## controller - switch (s4)
    net.addLink( h0, switch[0] )

    ## host - switch
    for i in range(10):
      net.addLink(host[i], switch[i], delay=dl, loss=ls, max_queue_size=qs,bw=baw)

    ## switches
    for index in range (0, len(switch)-1):
        net.addLink(switch[index], switch[index+1],bw = baw,delay=dl,loss=ls,max_queue_size=qs)
    net.addLink(switch[0], switch[9],bw=baw,loss=ls,delay=dl,max_queue_size=qs)
    info( '*** Starting network\n')
    net.start()

    #info('*** Set ip address to switch\n')
    for i in range (10):
      switch[i].cmd('ifconfig s' + str(i+1) + ' 10.0.1.' + str(i+1))

    info('*** Enable spanning tree\n')
    for i in range(10): 
      switch[i].cmd('ovs-vsctl set bridge s' + str(i+1) + 'stp-enable=true')

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
