import logging
from pathlib import Path

from enoslib import *

FORCE = False
CLUSTER = "parapluie"

logging.basicConfig(level=logging.DEBUG)

job_name = Path(__file__).name


# claim the resources
conf = (
    DistemConf
    .from_settings(
        job_name=job_name,
        force_deploy=FORCE,
        image="file:///home/msimonin/public/distem-stretch.tgz"
    )
    .add_machine(
        roles=["server"],
        cluster=CLUSTER,
        number=1,
        flavour="large"
    )
    .add_machine(
        roles=["client"],
        cluster=CLUSTER,
        number=1,
        flavour="large"
    )
    .finalize()
)

provider = Distem(conf)

roles, networks = provider.init()

print(roles)
print(networks)
gateway = networks[0].gateway
print("Gateway : %s" % gateway)

roles = sync_info(roles, networks)

with play_on(roles=roles, gather_facts=False) as p:
    # We first need internet connectivity
    # Netmask for a subnet in g5k is a /14 netmask
    p.shell("ifconfig if0 $(hostname -I) netmask 255.252.0.0")
    p.shell("route add default gw %s dev if0" % gateway)


# Experimentation logic starts here
with play_on(roles=roles) as p:
    # flent requires python3, so we default python to python3
    p.apt_repository(repo="deb http://deb.debian.org/debian stretch main contrib non-free",
                     state="present")
    p.apt(name=["flent", "netperf", "python3-setuptools"],
          state="present")

with play_on(pattern_hosts="server", roles=roles) as p:
    p.shell("nohup netperf &")

with play_on(pattern_hosts="client", roles=roles) as p:
    p.shell("flent rrul -p all_scaled "
            + "-l 60 "
            + "-H {{ hostvars[groups['server'][0]].inventory_hostname }} "
            + "-t 'bufferbloat test' "
            + "-o result.png")
    p.fetch(src="result.png",
            dest="result")
