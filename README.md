# Overview
This script uses cdp to build a list of hosts and their neighbors.
Each item in the list is a tuple of (local_device+interface, remote_device+interface).
Then using set theory, it validates this against a source of truth (master_list.yaml)

## Pre-requisites:
- Requires cdp (lldp in future)
- Each end's view of the link must be in the master_list.yaml file (current limitation)

## Example
```
python l1_validator.py 

Please select a group: ['campus', 'datacenter'] campus

Enter device username: admin
Enter device password: 

The following links are missing: 
PDX-3560-STAGING_GigabitEthernet0/3  >  PDX-3850-03_GigabitEthernet1/0/24    

The following links are not in the Master List DB:          
PDX-5548-01_Ethernet1/6              >  PDXL-2960-B_TenGigabitEthernet1/0/2  
PDX-5548-02_Ethernet1/3              >  PDX-5548-01_Ethernet1/3              
PDX-3650-STAGING_GigabitEthernet0/9  >  PDX-3850-02_GigabitEthernet0/0       
PDX-5548-01_Ethernet2/1              >  cucm-pub_eth0                        
PDX-3850-CORE_GigabitEthernet2/0/6   >  vedge-8004_GigabitEthernet0/0/1      
pdx-ucs-01-B_Ethernet1/2             >  PDX-5548-01_Ethernet1/2              
AP30f7_GigabitEthernet0              >  PDX-3560-STAGING_GigabitEthernet0/6  
Leaf101_Ethernet1/42                 >  PDX-5548-02_Ethernet1/21             
PDX-5548-02_Ethernet1/2              >  pdx-ucs-01-B_Ethernet1/1             
```

## Notes:
- Uses custom CDP TextFSM template to grab necessary data, you may need to modify.

## To-do:
- Create a csv report



