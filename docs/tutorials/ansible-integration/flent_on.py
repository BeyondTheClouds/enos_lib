from enoslib import *

import logging


logging.basicConfig(level=logging.DEBUG)

# The conf let us define the resources wanted.
# This is provider specific
conf = (
    VagrantConf()
    .from_settings(backend="libvirt")
    .add_machine(
        roles=["server"],
        flavour="tiny",
        number=1
    )
    .add_machine(
        roles=["client"],
        flavour="tiny",
        number=1
    )
    .add_network(
        roles=["mynetwork"],
        cidr="192.168.42.0/24")
    .finalize()
)

provider = Vagrant(conf)

# The code below is intended to be provider agnostic

# Start the resources
roles, networks = provider.init()


# Experimentation logic starts here
with play_on(roles=roles) as p:
    # flent requires python3, so we default python to python3
    p.shell("update-alternatives --install /usr/bin/python python /usr/bin/python3 1")
    p.apt_repository(repo="deb http://deb.debian.org/debian stretch main contrib non-free",
                     state="present")
    p.apt(name=["flent", "netperf", "python3-setuptools", "python3-matplotlib"],
          state="present")

with play_on(pattern_hosts="server", roles=roles) as p:
    p.shell("nohup netperf &")

with play_on(pattern_hosts="client", roles=roles) as p:
    # get the address of server
    server_address = roles["server"][0].address
    p.shell("flent rrul -p all_scaled "
            + "-l 60 "
            + f"-H { server_address } "
            + "-t 'bufferbloat test' "
            + "-o result.png")
    p.fetch(src="result.png",
            dest="result")
