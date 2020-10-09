links:
	ip link add my-veth0 type veth peer name my-veth0other
	ip link add my-veth1 type veth peer name my-veth1other
	ip link set my-veth0 up
	ip link set my-veth1 up
	brctl addbr my-bridge
	brctl addif my-bridge my-veth0other
	brctl addif my-bridge my-veth1other
	ip link set my-bridge up
	ip link set my-veth0other up
	ip link set my-veth1other up

clean:
	ip link set my-bridge down
	brctl delbr my-bridge
	ip link set my-veth0 down
	ip link set my-veth1 down
	ip link del my-veth0
	ip link del my-veth1

show:
	ip link show my-veth0 | tail -n1
	ip link show my-veth1 | tail -n1
