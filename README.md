# Overview
This script uses cdp to build a list of hosts and their neighbors.
Each item in the is a tuple of (local_device+interface, remote_device+interface).
Then using set theory, it validates this against a source of truth (master_list.yaml)

## Pre-requisites:
- requires cdp (lldp in future)
- Each end's view of the link must be in the master_list.yaml file

## Example
```
$ python l1_validator.py 

The following links are missing: 
{('PDX-3560-STAGING_GigabitEthernet0/3', 'PDX-3850-03_GigabitEthernet1/0/24')}

The following links are not in the Master List DB: 
{   ('PDX-3560-STAGING_GigabitEthernet0/3', '2702GBR_GigabitEthernet0'),
    ('PDX-3560-STAGING_GigabitEthernet0/6', 'AP30f7_GigabitEthernet0'),
    ('PDX-3560-STAGING_GigabitEthernet0/9', 'PDX-3850-02_GigabitEthernet0/0'),
    ('PDX-3850-02_GigabitEthernet0/0', 'PDX-3650-STAGING_GigabitEthernet0/9'),
    ('PDX-3850-02_GigabitEthernet1/0/13', 'fg-edge1_GigabitEthernet0/0'),
    ('PDX-3850-02_GigabitEthernet1/0/14', 'fg-edge2_GigabitEthernet0/0'),
    ('PDX-3850-CORE_GigabitEthernet2/0/6', 'vedge-8004_GigabitEthernet0/0/1')}
```

## Notes:
- Uses custom CDP TextFSM template to grab necessary data

## To-do:
- Need to remove duplicates so you need A's and B's view of the links

This is currently required - how to stop the need for this?

 - [ PDX-3850-02_GigabitEthernet1/0/24, PDX-3650-STAGING_GigabitEthernet0/2 ]
 - [ PDX-3560-STAGING_GigabitEthernet0/2, PDX-3850-02_GigabitEthernet1/0/24 ]

