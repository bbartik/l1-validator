from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir.core.filter import F
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
import textfsm
from ntc_templates.parse import parse_output
import pprint
from ruamel.yaml import YAML
import pdb
import getpass

yaml = YAML()
nr = InitNornir(config_file="config.yaml")
nbr_list = []
pp = pprint.PrettyPrinter(indent=4)

# you can also set these in the inventory/defaults.yaml file
username = input("\nEnter device username: ")
password = getpass.getpass("Enter device password: ")
nr.inventory.defaults.username = username
nr.inventory.defaults.password = password

def l1_validate(task, nbr_list):

    cmd = "show cdp neighbors detail"
    output = task.run(task=netmiko_send_command, command_string=cmd)
    cdp_results = output[0].result

    with open("cisco_ios_show_cdp_detail.textfsm") as f:
        template = textfsm.TextFSM(f)
    cdp_results = template.ParseText(cdp_results)

    local_host = str(task.host.name)

    for nbr in cdp_results:
        # strip of domain
        neighbor_hostname = nbr[0].split(".")[0]

        # create tuple
        local_intf = f"{local_host}_{nbr[2]}"
        remote_intf = f"{neighbor_hostname}_{nbr[3]}"
        nbr_tuple = (local_intf, remote_intf)

        # append tuple to list of actual links
        nbr_list.append(nbr_tuple)

# filter only campus switches
campus_switches = nr.filter(F(groups__contains="campus"))
r = campus_switches.run(task=l1_validate, nbr_list=nbr_list)

# load master list of links
with open("master_list.yaml", "r") as f:
    master_list = f.read()

# initialize empty set of lists, create set of tuples for set thoery operations
master_set = []
connections = yaml.load(master_list)
for c in connections:
    master_set.append(tuple(c))
master_set = set(master_set)
nbr_set = set(nbr_list)

# subtract existing set from master set to find missing links
missing = master_set - nbr_set
not_in_db = nbr_set - master_set

print("\nThe following links are missing: ")
# pretty printing the columns
col_width = max(len(word) for link in missing for word in link) + 2  # padding
for link in missing:
    #link = list(link)
    print(">  ".join(word.ljust(col_width) for word in link))

print("\nThe following links are not in the Master List DB: ")
# pretty printing the columns
col_width = max(len(word) for link in not_in_db for word in link) + 2  # padding
for link in not_in_db:
    #link = list(link)
    print(">  ".join(word.ljust(col_width) for word in link))