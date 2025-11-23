#!/usr/bin/env python3
# Mininet topology for P4 IDS testing
# Requires: Mininet, BMv2 (simple_switch_grpc running externally)

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf

def p4Topology():
    "Connect hosts to external P4 switch via veth pairs"
    # We do NOT add a switch here because simple_switch_grpc is running externally
    net = Mininet(controller=RemoteController)

    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='192.168.1.1/24', mac='00:00:00:00:00:01')
    h2 = net.addHost('h2', ip='192.168.1.2/24', mac='00:00:00:00:00:02')

    info('*** Connecting hosts to external P4 switch\n')
    # h1 connects to veth2 (which plugs into switch port 0/veth0)
    Intf('veth2', node=h1)
    # h2 connects to veth3 (which plugs into switch port 1/veth1)
    Intf('veth3', node=h2)

    info('*** Starting network\n')
    net.start()
    
    # Fix: Ensure ARP entries are set so hosts don't need to broadcast
    h1.cmd('arp -s 192.168.1.2 00:00:00:00:00:02')
    h2.cmd('arp -s 192.168.1.1 00:00:00:00:00:01')

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    p4Topology()
