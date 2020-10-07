# l2-sockets

A small hands-on experiment with L2 layer socket programming.

## Create the sockets

Use `ip link` to create virtual sockets to play with:
```
sudo make links
```

This creates a `veth` pair of interfaces. The thing about the `veth` pair is that bytes going into one come out of the other.

Use `sudo make clean` when you are down to remove the virtual interfaces.

## Start a L2 sniffer

Run:
```
sudo ./l2.py sniff
```
to start a L2 sniffer that only looks for the specific header `0x6001`. This is a randomly chosen number that is not used in any common protocols.


## Inject packets

Run:
```
sudo ./l2.py inject my-veth0
```
The Sniffer should capture this coming in.

Note:
1. Trt to inject into `my-veth1`; the sniffer will capture it on the other interface.
2. Try to inject into `lo`.

## Acknowledgements

1. https://gabhijit.github.io/linux-virtual-interfaces.html
2. https://gist.github.com/davidlares/e841c0f9d9b31f3cd8859575d061c467
