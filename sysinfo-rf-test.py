
import requests, json, sys, re, time, warnings, argparse, os

from datetime import datetime

warnings.filterwarnings("ignore")

parser=argparse.ArgumentParser(description="Python script using Redfish API to get system hardware inventory(output will be printed to the screen and also copied to a text file). This includes information for storage controllers, memory, network devices, general system details, power supplies, hard drives, fans, backplanes, processors")
parser.add_argument('-ip',help='IPMI IP address', required=True)
parser.add_argument('-u', help='IPMI username', required=True)
parser.add_argument('-p', help='IPMI password', required=True)
parser.add_argument('-x', help='Get script examples, pass in \"y\"', required=False)
parser.add_argument('-s', help='Get system information only, pass in \"y\"', required=False)
parser.add_argument('-m', help='Get memory information only, pass in \"y\"', required=False)
parser.add_argument('-c', help='Get processor information only, pass in \"y\"', required=False)
parser.add_argument('-f', help='Get fan information only, pass in \"y\"', required=False)
parser.add_argument('-ps', help='Get power supply information only, pass in \"y\"', required=False)
parser.add_argument('-S', help='Get storage information only, pass in \"y\"', required=False)
parser.add_argument('-n', help='Get network device information only, pass in \"y\"', required=False)
parser.add_argument('-a', help='Get all system information / device information, pass in \"y\"', required=False)



args=vars(parser.parse_args())

ipmi_ip=args["ip"]
ipmi_username=args["u"]
ipmi_password=args["p"]
"""
ipmi_ip=args["172.31.3.232"]
ipmi_username=args["ADMIN"]
ipmi_password=args["$upermicro"]
"""
try:
    os.remove("hw_inventory.txt")
except:
    pass



f=open("hw_inventory.txt","a")
d=datetime.now()
current_date_time="- Data collection timestamp: %s-%s-%s  %s:%s:%s\n" % (d.month,d.day,d.year, d.hour,d.minute,d.second)
f.writelines(current_date_time)
f.close()

def get_system_information():
    f=open("hw_inventory.txt","a")
    #response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1' % ipmi_ip,verify=False,auth=(ipmi_username, ipmi_password))
    response = requests.get('https://%s/redfish/v1/Systems/1' % ipmi_ip,verify=False,auth=(ipmi_username, ipmi_password))
    data = response.json()
    if response.status_code != 200:
        print("\n- FAIL, get command failed, error is: %s" % data)
        sys.exit()
    else:
        message = "\n---- System Information ----\n"
        f.writelines(message)
        f.writelines("\n")
        print(message)
    for i in data.items():
        if i[0] == u'@odata.id' or i[0] == u'@odata.context' or i[0] == u'Links' or i[0] == u'Actions' or i[0] == u'@odata.type' or i[0] == u'Description' or i[0] == u'EthernetInterfaces' or i[0] == u'Storage' or i[0] == u'Processors' or i[0] == u'Memory' or i[0] == u'SecureBoot' or i[0] == u'NetworkInterfaces' or i[0] == u'Bios' or i[0] == u'SimpleStorage' or i[0] == u'PCIeDevices' or i[0] == u'PCIeFunctions':
            pass
        
        elif i[0] == u'Oem':
            #for ii in i[1][u'Dell'][u'DellSystem'].items():
            for ii in i[1][u'Test'][u'TestSystem'].items():
                if ii[0] == u'@odata.context' or ii[0] == u'@odata.type':
                    pass
                else:
                    message = "%s: %s" % (ii[0], ii[1])
                    f.writelines(message)
                    f.writelines("\n")
                    print(message)
             
                
        elif i[0] == u'Boot':
            try:
                message = "BiosBootMode: %s" % i[1][u'BootSourceOverrideMode']
                f.writelines(message)
                f.writelines("\n")
                print(message)
            except:
                pass
        else:
            message = "%s: %s" % (i[0], i[1])
            f.writelines(message)
            f.writelines("\n")
            print(message)
    f.close()

def get_memory_information():
    f=open("hw_inventory.txt","a")
    #response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1/Memory' % ipmic_ip,verify=False,auth=(ipmic_username, ipmic_password))
    response = requests.get('https://%s/redfish/v1/Systems/1/Memory' % ipmi_ip,verify=False,auth=(ipmi_username, ipmi_password))
    #https://172.31.3.232/redfish/v1/Systems/1/Memory
    data = response.json()
    if response.status_code != 200:
        print("\n- FAIL, get command failed, error is: %s" % data)
        sys.exit()
    else:
        message = "\n---- Memory Information ----"
        f.writelines(message)
        f.writelines("\n")
        print(message)
    for i in data[u'Members']:
        dimm = i[u'@odata.id'].split("/")[-1]
        try:
            #dimm_slot = re.search("DIMM.+",dimm).group()
            dimm_slot = re.search("Memory.+",dimm).group()

        except:
            print("\n- FAIL, unable to get dimm slot info")
            sys.exit()
        response = requests.get('https://%s%s' % (ipmi_ip, i[u'@odata.id']),verify=False,auth=(ipmi_username, ipmi_password))
        sub_data = response.json()
        if response.status_code != 200:
            print("\n- FAIL, get command failed, error is: %s" % sub_data)
            sys.exit()
        else:
            message = "\n- Memory details for %s -\n" % dimm_slot
            f.writelines(message)
            f.writelines("\n")
            print(message)
            for ii in sub_data.items():
                if ii[0] == u'@odata.id' or ii[0] == u'@odata.context' or ii[0] == u'Metrics' or ii[0] == u'Links':
                    pass
                elif ii[0] == u'Oem':
                    for iii in ii[1][u'SMC'][u'SMCMemory'].items():
                        if iii[0] == u'@odata.context' or iii[0] == u'@odata.type':
                            pass
                        else:
                            message = "%s: %s" % (iii[0], iii[1])
                            f.writelines(message)
                            f.writelines("\n")
                            print(message)
                else:
                    message = "%s: %s" % (ii[0], ii[1])
                    f.writelines(message)
                    f.writelines("\n")
                    print(message)
    f.close()

def check_supported_ipmi_version():
    response = requests.get('https://%s/redfish/v1/Systems/1' % ipmi_ip,verify=False,auth=(ipmi_username, ipmi_password))
    data = response.json()
    if response.status_code != 200:
        print("\n- WARNING, ipmi version installed does not support this feature using Redfish API")
        sys.exit()
    else:
        pass

if __name__ == "__main__":
    check_supported_ipmi_version()
    if args["x"]:
          script_examples()
    if args["s"]:
        get_system_information()
    if args["m"]:
        get_memory_information()
    if args["c"]:
        get_cpu_information()
    if args["f"]:
        get_fan_information()
    if args["ps"]:
        get_ps_information()
    if args["S"]:
        get_storage_controller_information()
        get_storage_disks_information()
        get_backplane_information()
    if args["n"]:
        get_network_information()
    if args["a"]:
        get_system_information()
        get_memory_information()
        get_cpu_information()
        get_fan_information()
        get_ps_information()
        get_storage_controller_information()
        get_storage_disks_information()
        get_backplane_information()
        get_network_information()

    print("\n- WARNING, output also captured in \"%s\hw_inventory.txt\" file" % os.getcwd())
