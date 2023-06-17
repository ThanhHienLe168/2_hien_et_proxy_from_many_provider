# %%
import random
import json
import requests
import time

# %%
# This function is used to create or update proxy config file
def set_up_proxy_config(config_file_path):
    try:
        with open(config_file_path,'r',encoding='utf-8') as f:
            config_list = json.load(f)
            f.close()
    except:
        config_list =[]
        pass
    
    print('provider_name :')
    provider_name = str(input())
    if provider_name == 'exit':
        return 'Set up done !'
        
    print('provider_id :')
    provider_id =str(input())
    print('provider_link :')
    provider_link = str(input())
    
    while True:
        print('for_single_thread :')
        for_single_thread = str(input())
        if for_single_thread!='0' and for_single_thread!='1':
            print('just_for_single_thread must be : \n    1 if True\n    0 if False')
        else:
            break
    
    account_list =[]
    while True:
        print('user_name :')
        user_name = str(input())
        if user_name=='ok':
            break 
        password = str(input())
        account = {
            'user_name': user_name,
            'password': password
        }
        if account not in account_list:
            account_list.append(account)
        
    proxy_api_key_list = []
    while True:
        print('proxy_api_key :')
        proxy_api_key = str(input())
        if proxy_api_key == 'ok':
            break
        if proxy_api_key not in proxy_api_key_list:
            proxy_api_key_list.append(proxy_api_key)
            
    config ={
        'provider_id': provider_id,
        'provider_name': provider_name,
        'provider_link': provider_link,
        'for_single_thread': for_single_thread,
        'account_list': account_list,
        'proxy_api_key_list': proxy_api_key_list
    }
    config_list.append(config)
    with open(config_file_path,'w',encoding='utf-8') as f:
        json.dump(config_list,f,ensure_ascii=False,indent=4)
        f.close()
    return 'Set up done !'
    

# %%
# Just for testing
# set_up_proxy_config('proxy_config.json')

# %%
# This function is used to load config file to json config
def load_config_file(config_file_path):
    try:
        with open(config_file_path,'r',encoding='utf-8') as f:
            config_list = json.load(f)
            f.close()
    except:
        print('Can not load config file : ',config_file_path)
        config_list =[]
        pass
    return config_list
    

# %%
# Just for testing
# config_list = load_config_file('proxy_config.json')

# %%
# Tin proxy functions here
def set_tin_proxy(proxy_api_key,host_ip):
    proxy_api = f'https://api.tinproxy.com/proxy/get-new-proxy?api_key={proxy_api_key}&authen_ips={host_ip}&location=vn_hcm'
    for refresh in range(4):
        try:
            proxy_data =requests.get(proxy_api).json()
            # Remember to change this after testing
            if   1==1 :  #proxy_data['message']=='Lấy Proxy thành công':
                user = proxy_data['data']['authentication']['username']
                pw = proxy_data['data']['authentication']['password']
                proxy ={
                    'http': proxy_data['data']['http_ipv4'],
                    'https': proxy_data['data']['http_ipv4']
                }
                break
        except:
            proxy ={
                'http': '',
                'https': ''
            }
            pass
        # Just for testing
        # time.sleep(2)
        print('Tinproxy error ')
    
    return proxy
        


# %%
# # Just for testing
# proxy_api_key = 'VLBWOPMXo0o3nILVo62zLRA01ybdYJdn'
# host_ip = '222.253.53.241'
# check_ip_link = 'http://myip.lunaproxy.com'
# test_proxy = set_tin_proxy(proxy_api_key,host_ip)
# requests.get(check_ip_link,proxies=test_proxy).text


# %%
#Luna proxy functions here
def set_luna_proxy(user_name,password):
    location_code ='kr'
    proxy = {
    'http': f'http://user-{user_name}-region-{location_code}:{password}@as.lunaproxy.com:12233',
    'https': f'http://user-{user_name}-region-{location_code}:{password}@as.lunaproxy.com:12233',
    }
    return proxy
    

# %%
# # Just for testing
# check_ip_link = 'http://myip.lunaproxy.com'
# user_name = 'Luna_subacc_5'
# password = '123456'
# test_proxy = set_luna_proxy(user_name,password)
# requests.get(check_ip_link,proxies=test_proxy).text


# %%
# Brightdata data-center proxy functions here
def set_brightdata_proxy(user_name,password):
    port = 22225
    session_id = random.random()
    username = user_name
    password = password
    super_proxy_url = ('http://%s-country-vn-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
    proxy = {
        'http': super_proxy_url,
        'https': super_proxy_url,
    }
    return proxy

# %%
# # Just for testing
# user_name = 'brd-customer-hl_26de7fde-zone-data_center'
# password = '5aw3qou8s5kk'
# check_ip_link = 'http://myip.lunaproxy.com'
# test_proxy = set_brightdata_proxy(user_name,password)
# requests.get(check_ip_link,proxies= test_proxy).text

# %%
# This function used to create proxy config for each thread
def create_thread_proxy_config(thread_name,host_ip,provider_id_list,account_and_api_control_file_path,proxy_config_path):
      try:
            with open(account_and_api_control_file_path,'r',encoding='utf-8') as f:
                  control_account_and_api = json.load(f)
                  f.close()  
            control_account_list =control_account_and_api['control_account_list']
            control_proxy_api_key_list =control_account_and_api['control_proxy_api_key_list']
      except:
            control_account_list=[]
            control_proxy_api_key_list=[]

      config_list = load_config_file(proxy_config_path)
      thread_proxy_list =[]
      for provider_id in provider_id_list:
            proxy={}
            check_config ={}
            user_name =''
            password = ''
            proxy_api_key =''
            for config in config_list:
                  if provider_id == config['provider_id']:
                        check_config = config
                        break
            if check_config!={}:
                  for c_account in check_config['account_list']:
                        if c_account not in control_account_list:
                              if config['for_single_thread']=='1':
                                    control_account_list.append(c_account)
                              user_name = c_account['user_name']
                              password = c_account['password']
                              break
                  for c_proxy_api_key in check_config['proxy_api_key_list']:
                        if c_proxy_api_key not in control_proxy_api_key_list:
                              if config['for_single_thread']=='1':
                                    control_proxy_api_key_list.append(c_proxy_api_key)
                              proxy_api_key = c_proxy_api_key
                              break
      
            proxy['provider_id']= provider_id
            proxy['account']={
                  'user_name': user_name,
                  'password': password
            }
            proxy['proxy_api_key']= proxy_api_key
            thread_proxy_list.append(proxy)
      thread_config ={
            'thread_name':thread_name,
            'host_ip': host_ip,
            'proxy_list': thread_proxy_list
      }
      with open(account_and_api_control_file_path,'w',encoding='utf-8') as f:
            json.dump({
                  'control_proxy_api_key_list': control_proxy_api_key_list,
                  'control_account_list': control_account_list
            },f,ensure_ascii=False,indent=4)
            f.close()        
      return thread_config


# %%
# # Just for testing
# thread_name = 'thread_1'
# provider_id_list = ['tin','luna','brightdata']
# account_and_api_control_file_path= 'account_and_api_control.json'
# proxy_config_path= 'proxy_config.json'
# host_ip = '222.253.53.241'
# thread_proxy_config = create_thread_proxy_config(thread_name,host_ip,provider_id_list,account_and_api_control_file_path,proxy_config_path)

# %%

def remove_thread_proxy_config(thread_proxy_config,account_and_api_control_file_path):
    proxy_list = thread_proxy_config['proxy_list']
    try:
        with open(account_and_api_control_file_path,'r',encoding='utf-8') as f:
            control_account_and_api = json.load(f)
            f.close()  
        control_account_list = control_account_and_api['control_account_list']
        control_proxy_api_key_list = control_account_and_api['control_proxy_api_key_list']
    except:
        ontrol_account_list = []
        control_proxy_api_key_list = []
        pass
        
    for proxy in proxy_list:
        account = proxy['account']
        proxy_api_key = proxy['proxy_api_key']
        if account in control_account_list:
            control_account_list.remove(account)
        if proxy_api_key in control_proxy_api_key_list:
            control_proxy_api_key_list.remove(proxy_api_key)
    with open(account_and_api_control_file_path,'w',encoding='utf-8') as f:
                json.dump({
                    'control_proxy_api_key_list': control_proxy_api_key_list,
                    'control_account_list': control_account_list
                },f,ensure_ascii=False,indent=4)
                f.close() 
    return 'Remove thread proxy config done !'
    

# %%
# # Just for testing 
# account_and_api_control_file_path= 'account_and_api_control.json'
# remove_thread_proxy_config(thread_proxy_config,account_and_api_control_file_path)

# %%
# This function is used to get proxy IP from one proxy provider
# Maybe change many time in future

def get_proxy(provider_id,thread_proxy_config):
    for config in thread_proxy_config['proxy_list']:
        if provider_id== config['provider_id']:
            proxy_config =config
            break
    proxy = 'error_proxy'
    # If you add or remove proxy provider, you have to change the code bellow too.
    
    # Tin proxy
    if provider_id == 'tin':
        tin_proxy = set_tin_proxy(proxy_config['proxy_api_key'],thread_proxy_config['host_ip'])
        if tin_proxy['http']!='' and tin_proxy['https']!='':
            proxy= tin_proxy
       
        
    # Luna proxy
    if provider_id =='luna':
        luna_proxy = set_luna_proxy(config['account']['user_name'],config['account']['password'])
        if luna_proxy['http']!='' and luna_proxy['https']!='':
            proxy = luna_proxy
       
    
    # Brightdata data-center proxy
    if provider_id =='brightdata':
        brightdara_proxy = set_brightdata_proxy(config['account']['user_name'],config['account']['password'])
        proxy = brightdara_proxy
      
    return proxy
    

# %%
# provider_id ='tin'
# thread_proxy_config = thread_proxy_config
# proxy = get_proxy(provider_id,thread_proxy_config)
# requests.get(check_ip_link,proxies= proxy).text



# %%
# set_proxy(priority_provider_id,alternative_provider_id_list,thread_proxy_config)
def set_proxy(priority_provider_id,alternative_provider_id_list,thread_proxy_config):
    priority_proxy_failed = '0'
    proxy = get_proxy(priority_provider_id,thread_proxy_config)
    if proxy=='error_proxy':
        priority_proxy_failed = '1'
        print('Priority proxy failed. Start with alternative proxy ...')
        for provider_id in alternative_provider_id_list:
            proxy = get_proxy(provider_id,thread_proxy_config)
            if proxy!='error_proxy':
                break
    final_proxy ={
        'proxy': proxy,
        'priority_proxy_failed': priority_proxy_failed
    }
    return final_proxy

# %%
# # Just for testing 
# priority_provider_id = 'brightdata'
# alternative_provider_id_list= ['luna']
# final_proxy = set_proxy(priority_provider_id,alternative_provider_id_list,thread_proxy_config)
# proxy = final_proxy['proxy']
# requests.get(check_ip_link,proxies= proxy).text


