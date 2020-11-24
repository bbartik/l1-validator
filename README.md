# Overview
This script uses cdp to build a list of hosts and their neighbors.
Each item in the list is a tuple of (local_device+interface, remote_device+interface).
Then using set theory, it validates this against a source of truth (master_list.yaml)

## Pre-requisites:
- Requires cdp (lldp in future)
- Each end's view of the link must be in the master_list.yaml file (current limitation)

## Example
```
$ python l1_validator.py 

Enter device username: admin
Enter device password: 

The following links are missing: 
leaf5_Ethernet1/1   >  spine1_Ethernet1/5  
leaf5_Ethernet1/2   >  spine2_Ethernet1/5  

The following links are not in the Master List DB: 
leaf2_Ethernet1/7  >  leaf1_Ethernet1/7    
```

## Notes:
- Uses custom CDP TextFSM template to grab necessary data, you may need to modify.



