#!/usr/bin/env python3

import p4runtime_sh.shell as sh
import time

def populate_blacklist():
    """Add malicious IPs to the bad_sources table"""
    
    print("Connecting to P4 switch...")
    # Connect to P4 switch (adjust port if different)
    sh.setup(
        device_id=0, 
        grpc_addr='localhost:9559',  # BMv2 gRPC port
        election_id=(0, 1),
        config=sh.FwdPipeConfig('/home/daniel/p4-ids-bmv2/build/simple_switch.json')
    )
    
    print("Adding entries to bad_sources table...")
    
    # Add h1's IP (192.168.1.1) targeting HTTP port 80
    table_entry = sh.TableEntry('IngressImpl.bad_sources')(
        action='IngressImpl.drop'
    ).match(
        src_addr='192.168.1.1', 
        dst_port=80              
    )
    table_entry.insert()
    
    # You can add more malicious IPs
    # Example: Block another attacker on different port
    table_entry2 = sh.TableEntry('IngressImpl.bad_sources')(
        action='IngressImpl.drop'
    ).match(
        src_addr='192.168.1.100',
        dst_port=80
    )
    table_entry2.insert()
    
    print("Blacklist populated successfully!")
    
    # Optional: Print current table entries
    print("\nCurrent bad_sources table entries:")
    for entry in sh.TableEntry('IngressImpl.bad_sources').read():
        print(f"  {entry}")

def clear_blacklist():
    """Clear all entries from bad_sources table"""
    print("Clearing bad_sources table...")
    
    for entry in sh.TableEntry('IngressImpl.bad_sources').read():
        entry.delete()
    
    print("Table cleared!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'clear':
        sh.setup(
            device_id=0, 
            grpc_addr='localhost:9559',
            election_id=(0, 1),
            config=sh.FwdPipeConfig('/home/daniel/p4-ids-bmv2/build/simple_switch.json')
        )
        clear_blacklist()
    else:
        populate_blacklist()