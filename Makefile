links:
	ip link add my-veth0 type veth peer name my-veth1
	ip link set my-veth0 up
	ip link set my-veth1 up

clean:
	ip link set my-veth0 down
	ip link set my-veth1 down
	ip link del my-veth0

show:
	ip link show
