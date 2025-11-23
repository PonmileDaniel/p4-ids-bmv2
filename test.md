Here is the manual procedure to run it and the fix for your topology code.

Phase 1: Prepare the Network Interfaces (Terminal 1)
The P4 switch needs virtual interfaces to "plug into". You must create these manually before starting the switch.

# 1. Create virtual ethernet pairs
sudo ip link add veth0 type veth peer name veth2
sudo ip link add veth1 type veth peer name veth3

# 2. Bring interfaces up
sudo ip link set veth0 up
sudo ip link set veth1 up
sudo ip link set veth2 up
sudo ip link set veth3 up

# 3. Disable IPv6 (optional, reduces noise)
sudo sysctl -w net.ipv6.conf.veth0.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.veth1.disable_ipv6=1



Phase 2: Start the P4 Switch (Terminal 1)
Now start the switch manually, binding it to the interfaces we just created.

# Run the switch in the foreground
sudo simple_switch_grpc \
    --log-console \
    --thrift-port 9090 \
    --grpc-server-addr localhost:9559 \
    -i 0@veth0 \
    -i 1@veth1 \
    build/simple_switch.json

Keep this terminal open. You should see logs appearing here.

Phase 3: Load the Rules (Terminal 2)
In a new terminal, inject your blacklist rules.

python3 control_plane.py


Phase 4: Fix and Run Topology (Terminal 3)
This is why your application wasn't detecting anything. Your current topo.py creates a standard OVS switch (s1) that is completely isolated from the P4 switch running in Terminal 1. The traffic goes h1 -> OVS -> h2 and never touches your P4 code.