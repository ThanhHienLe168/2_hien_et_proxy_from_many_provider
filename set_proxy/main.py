

import json
import time
import requests
import os
import concurrent.futures
from set_proxy import *

# Set up all proxy config file path 
account_and_api_control_file_path= 'account_and_api_control.json'
proxy_config_path= 'proxy_config.json'

# Set up provider_id 
priority_provider_id = 'tin'
alternative_provider_id_list= ['luna','brightdata']
provider_id_list = [id for id in alternative_provider_id_list]
provider_id_list.append(priority_provider_id)
host_ip = '222.253.53.241'

# Sample single thread function
def single_thread(thread_proxy_config, priority_provider_id= priority_provider_id, alternative_provider_id_list=alternative_provider_id_list,account_and_api_control_file_path= account_and_api_control_file_path):
    # Set up and optimize proxy in all situations | back up proxy
    priority_proxy_failed_max = 4
    priority_proxy_failed_checking = 0
    
    start_time =0
    for test_program in range(10):
        print('-------------------------------')
        print('This is testing_program ', test_program,'of thread ', thread_proxy_config['thread_name'])
        # For back up proxy
        if priority_proxy_failed_checking== priority_proxy_failed_max:
            priority_provider_id = alternative_provider_id_list.pop()    
            print('Change priority_provider to ', priority_provider_id)
            
        final_proxy = set_proxy(priority_provider_id,alternative_provider_id_list,thread_proxy_config)
        proxy = final_proxy['proxy']
        priority_proxy_failed = final_proxy['priority_proxy_failed']
        proxy = final_proxy['proxy']
        
        
        priority_proxy_failed_checking+= int(priority_proxy_failed)
        check_ip_link = 'http://myip.lunaproxy.com'
        text =requests.get(check_ip_link,proxies=proxy).text
        print('\n\n\n Tui hien tai dang o day  : ',text,'\n\n')
        # print('*************************')
        # time.sleep(4)
        
    # Using remove_thread_proxy_cofig after being done to put back the account or API_key is available for another thread.
    remove_thread_proxy_config(thread_proxy_config,account_and_api_control_file_path)
    return 0

try:
    os.remove('account_and_api_control.json')
except:
    pass

thread_proxy_config_list =[]
for max_workers in range(8):
    thread_name = str(max_workers)
    thread_proxy_config = create_thread_proxy_config(thread_name,host_ip,provider_id_list,account_and_api_control_file_path,proxy_config_path)
    thread_proxy_config_list.append(thread_proxy_config)
    


with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(single_thread,thread_proxy_config_list)
    # executor.submit(single_thread,thread_proxy_config_list.pop())
  
print('\n\n\n\n CHUNG TA DA XONG \n\n\n\n')
try:
    os.remove('account_and_api_control.json')
except:
    pass