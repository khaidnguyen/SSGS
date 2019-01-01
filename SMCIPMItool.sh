
#BMC_IP="172.31.49.218"
#user=ADMIN
#passwd=ADMIN

echo "Finding IPMI Devices....."
./SMCIPMITool ${BMC_IP} ${user} ${passwd} find > IPMI-find

###########################
# SAMPLE OUTPUT IPMI-find
[root@superbb SMCIPMITool_2.18]# ./SMCIPMITool 172.31.49.218 ADMIN ADMIN find
Finding IPMI Devices ...
  172.31.51.13           AST2500
Found hosts loaded
  172.31.51.25           AST2500      # 2 Intel NVME
  172.31.51.34           IPMI 2.0 ASPD_T IPMI+KVM
  172.31.51.56           AST2500
  172.31.51.77           IPMI 2.0 ASPD_T IPMI+KVM
  172.31.51.83           AST2500
  172.31.51.90           IPMI
  172.31.51.91           IPMI
  172.31.51.117          AST2500
  172.31.51.124          AST2500
  172.31.51.127          IPMI 2.0 ASPD_T IPMI+KVM
  172.31.51.177          IPMI 2.0 ASPD_T IPMI+KVM
  172.31.51.231          AST2500
  172.31.51.233          AST2500
  172.31.51.235          IPMI 2.0 ASPD_T IPMI+KVM
15 IPMI device(s) found. Use "found" to list found devices
#############################


echo "Found List from IPMI Devices."

./SMCIPMITool ${BMC_IP} ${user} ${passwd} found list > IPMI-foundlist

############################
# SAMPLE OUTPUT FOUND LIST
Found hosts loaded

Found IPMI Devices
------------------
 Index | IP               Board            DC Room  Row Rack  Num Type        | BMC
 ----- | ---------------- -----          ---- ---- ---- ---- ---- ----        | -------
     1 | 172.31.51.13                                                         |
     2 | 172.31.51.25                                                         |
     3 | 172.31.51.34                                                         |
     4 | 172.31.51.56                                                         |
     5 | 172.31.51.77                                                         |
     6 | 172.31.51.83                                                         |
     7 | 172.31.51.90                                                         |
     8 | 172.31.51.91                                                         |
     9 | 172.31.51.117                                                        |
    10 | 172.31.51.124                                                        |
    11 | 172.31.51.127                                                        |
    12 | 172.31.51.177                                                        |
    13 | 172.31.51.231                                                        |
    14 | 172.31.51.233                                                        |
    15 | 172.31.51.235                                                        |

15 IPMI device(s) found. 
#####################################





