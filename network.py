import subprocess
import time

class wireless:
    def __init__(self):
        1 == 1

    def wireless_startup(self):
        os.system("ifup wlan0")

    '''
    netowrk information format: [{id, ssid, bssid, flags}, {id, ssid, bssid, flags}]
    '''
    def list_network(self):
        # Get setting of wireless
        network_table = subprocess.Popen("wpa_cli -i wlan0 list_networks", shell=True,stdout=subprocess.PIPE).stdout.read()

        # Convert network_table to type of string 
        network_table_string = network_table.decode('utf-8')
       
        # Analysis table
        network_dic = []
        network_table_list = network_table_string.split('\n')[1:]
        for network_table_list_item in network_table_list:
            network_dic_item = {}
            network_info = network_table_list_item.split('\t')
            # Check whether length of network_info is more than 1 or not
            if(len(network_info) < 2):
                continue
            # Alloc information to dictionary
            network_dic_item["id"] = network_info[0]
            network_dic_item["ssid"] = network_info[1]
            network_dic_item["bssid"] = network_info[2]
            network_dic_item["security"] = network_info[3]
            network_dic.append(network_dic_item)

        return network_dic

    def scan_network(self):
        # Scan network
        subprocess.Popen("wpa_cli -i wlan0 scan", shell=True,stdout=subprocess.PIPE).stdout.read()

        # Wating for scanning
        time.sleep(2)

        # Obtain scan result
        network_scan_result = subprocess.Popen("wpa_cli -i wlan0 scan_result", shell=True,stdout=subprocess.PIPE).stdout.read().decode('utf-8')
        network_scan_result_array = network_scan_result.split('\n')[1:]

        # Put result into json
        ap_group = []
        for ssid_item in network_scan_result_array:
            ap_information = ssid_item.split('\t') 
            # Check whether length of ap_information is more than one or not
            if(ap_information == None):
                continue
            if(len(ap_information) != 5):
                continue
            ap = {}
            ap["bssid"] =  ap_information[0]
            ap["frequency"] =  ap_information[1]
            ap["signal_level"] =  ap_information[2]
            ap["flags"] =  ap_information[3]
            ap["ssid"] =  ap_information[4]
            ap_group.append(ap)
        return ap_group


    def set_network(self, ssid, pwd):
        # Disable network
        subprocess.Popen("wpa_cli -i wlan0 disble_network 0", shell=True,stdout=subprocess.PIPE).stdout.read()

        # Configure ssid
        subprocess.Popen("wpa_cli -i wlan0 set_network 0 ssid "+ '\'"' + ssid + '"\'', shell=True, stdout=subprocess.PIPE).stdout.read()
        
        # Configure password
        subprocess.Popen("wpa_cli -i wlan0 set_network 0 psk "+ '\'"' + pwd + '"\'', shell=True, stdout=subprocess.PIPE).stdout.read()

        # Enable network
        subprocess.Popen("wpa_cli -i wlan0 enable_network 0", shell=True, stdout=subprocess.PIPE).stdout.read()

        # Select network
        subprocess.Popen("wpa_cli -i wlan0 select_network 0", shell=True, stdout=subprocess.PIPE).stdout.read()

        # Save config
        subprocess.Popen("wpa_cli -i wlan0 save_config", shell=True, stdout=subprocess.PIPE).stdout.read()

        # Give ip by dhcp client
        subprocess.Popen("udhcpc -i wlan0", shell=True,stdout=subprocess.PIPE).stdout.read()


    