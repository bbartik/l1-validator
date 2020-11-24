from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import textfsm
from ntc_templates.parse import parse_output
import pprint
from ruamel.yaml import YAML
import numpy as np
import pdb
import getpass
import sys

yaml = YAML()
nr = InitNornir(config_file="config.yaml")
pp = pprint.PrettyPrinter(indent=4)

# you can also set these in the inventory/defaults.yaml file
#username = input("\nEnter device username: ")
#password = getpass.getpass("Enter device password: ")
nr.inventory.defaults.username = "admin"
nr.inventory.defaults.password = "cisco123"

def duplicate(connections):
    return None

def l1_validate(task):

    cmd = "show cdp neighbors detail"
    output = task.run(task=netmiko_send_command, command_string=cmd)
    cdp_results = output[0].result

    with open("cisco_ios_show_cdp_detail.textfsm") as f:
        template = textfsm.TextFSM(f)
    parsed_results = template.ParseText(cdp_results)
    
    # initialize neighbor list
    nbr_list = []
    local_host = str(task.host.name)

    for nbr in parsed_results:
        # strip of domain
        neighbor_hostname = nbr[0].split(".")[0]

        # create link set
        local_intf = f"{local_host}_{nbr[2]}"
        remote_intf = f"{neighbor_hostname}_{nbr[3]}"
        if "mgmt" not in local_intf:
            nbr_set = {local_intf, remote_intf}

            # append tuple to list of actual links
            nbr_list.append(nbr_set)

    return nbr_list


# initialize live complete neighbor list
live_nbr_list = []
# filter if needed
#campus_switches = nr.filter(F(groups__contains="datacenter"))
result = nr.run(task=l1_validate)

if len(result.failed_hosts) > 0:
    print("One or more hosts failed to connect. Please run again.")
    print(result.failed_hosts)
    sys.exit()

# populate new list from all nodes
for x in result.keys():
    x_links = result[x].result
    for link in x_links:
        live_nbr_list.append(link)

# remove duplicates, this is the set that will be used for comparison
live_nbr_set = set()
for nbr in live_nbr_list:
    live_nbr_set.add(tuple(nbr))
temp_live_nbr_list = list(live_nbr_set)
live_nbr_list = [set(x) for x in temp_live_nbr_list ]

# load master list of links
with open("l1_spine_leaf.yaml", "r") as f:
    master_file = f.read()

# initialize empty set of lists, create set of tuples for set thoery operations
master_list = []
connections = yaml.load(master_file)
for conn in connections:
    #pdb.set_trace()
    # convert to set to normalize the order
    conn = set(conn)
    # convert to tuple so you can add it to the list and convert to set
    master_list.append(conn)

'''
deugging the set order issue
print(len(master_set))
pprint.pprint(master_set)
sys.exit()
'''

# subtract existing list from master list to find missing links
missing = [x for x in master_list if x not in live_nbr_list]
not_in_db = [x for x in live_nbr_list if x not in master_list]

# pretty printing the columns
try:
    print("\nThe following links are missing: ")
    col_width = max(len(word) for link in missing for word in link) + 2  # padding
    for link in missing:
        #link = list(link)
        print(">  ".join(word.ljust(col_width) for word in link))
except:
    print("Looks like there are no missing links!")

print("\nThe following links are not in the Master List DB: ")
# pretty printing the columns
try:
    col_width = max(len(word) for link in not_in_db for word in link) + 2  # padding
    for link in not_in_db:
        #link = list(link)
        print(">  ".join(word.ljust(col_width) for word in link))
except:
    print("Looks like all links are in the Master DB")
