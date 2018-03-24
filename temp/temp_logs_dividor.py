import os
import re
from datetime import datetime
from time import strptime as time_strptime

logs_data = {}
subcategories_name_to_description = { #Don't worry about the lower and the uppercase - the code changes it to lowercase anyway 
    'FW_ARP' : 'ARP Spoofing',
    'FW_DHCP': 'Rouge DHCP',
    'FW_DOS' : 'DOS',
    'FW_MISC': 'Misc',
    'SHM_SC' : 'File descriptors',
    'SHM_SD' : 'Directories',
    'SHM_SE' : 'Executions',
    'SHM_SF' : 'Files',
    'SHM_SH' : 'Manager',
    'SHM_SP' : 'Permissions',
    'SHM_SS' : 'Sockets'
}

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def is_ip(s):
    return (s.count('.') == 3) 

def replace_all(string,to_replace,what):
    for letter in to_replace:
        string = string.replace(letter,what)
    return string

def get_normal_date(d):
    date_splited = d.split(' ')
    needed_date = '%s:%s:%s:%s' % (date_splited[3],str(time_strptime(date_splited[1],'%b').tm_mon), date_splited[5], date_splited[4])
    #needed_date looks like: '9-3-2018 11:22:03'
    perfect_date = {}
    needed_date_splitted = needed_date.split(':')

    perfect_date['day'] = needed_date_splitted[0]
    perfect_date['month'] = needed_date_splitted[1]
    perfect_date['year'] = needed_date_splitted[2]
    perfect_date['hour'] = needed_date_splitted[3]
    perfect_date['min'] = needed_date_splitted[4]
    perfect_date['sec'] = needed_date_splitted[5]


    return perfect_date
    

def log_contains_ip_or_mac(l):
    #droped [mac][ip]
    log_info = {}
    if '[' in l and ']' in l:
        for s in [m.start() for m in re.finditer('\[', l)]:
            ip_or_mac = l[s+1:l.find(']',s)]
            if is_ip(ip_or_mac):
                log_info['ip'] = ip_or_mac
            else:
                log_info['mac']= ip_or_mac
    return log_info                



def read_logs():
    global logs_data
    logs_data_temp={}
    logs_data={}
    smt_dir = '/var/log/smt'
    if os.path.exists(smt_dir):
        smt_files = os.listdir(smt_dir)
        
        if len(smt_files) == 0:
            print 'No files :('
        
        else:
            
            for fname in smt_files:
                
                f = open( smt_dir + '/' + fname,'r')
                lines = f.readlines()
                logs_data_temp[fname] = [line.replace('\n','').rsplit('-',1) for line in lines]
                
        for name,logs in logs_data_temp.items():
            
            logs_data[name] = []
            sub =  subcategories_name_to_description[name] if name in subcategories_name_to_description else ''
            

            if name.startswith('SHM') and name[-1] != 'H':
                for log in logs:
                    
                    date = get_normal_date(replace_all(log[1],'[]',''))
                    syscall_params = log[0].split(':',1)
                    params_list = map(lambda x : x.strip(), syscall_params[1].split(' | ')) 
                    params_dic = {}
                    
                    for param in params_list:
                        key_val_param = param.split('=')
                        params_dic[key_val_param[0]] = key_val_param[1]
                    
                    log = {'syscall_name' : syscall_params[0],'date' : date , 'subcategory' : sub}
                    log = merge_two_dicts(log,params_dic)
                    logs_data[name].append(log)
            else:
                
                if name.startswith('FW'):
                    for log in logs:

                        date = get_normal_date(replace_all(log[1],'[]',''))
                        mes = log[0].split(':',1)[0]
                        
                        ip_and_mac = {'date' : date, 'message' : mes, 'subcategory' : sub}
                        log = merge_two_dicts(log_contains_ip_or_mac(log[0]),ip_and_mac)
                        logs_data[name].append(log)
                else:
                    for log in logs:
                        
                        date = get_normal_date(replace_all(log[1],'[]',''))
                        mes = log[0]

                        logs_data[name].append({'date' : date,'message' : mes,'subcategory' : sub})

                #else:
                #    print '%s is empty' % (name) #Actually need to read here the logs that not from the syscalls
    else:
        print '%s is not defined' % (smt_dir)
   
#This function searches inside the logs data, for example - get all logs with pid 1000 - you send 'pid' as key and 1000 as value.
#Works on every key (Go to supporting keys)
#Need to support date,subcategory
def search_in_logs(key,value):
    global logs_data
    ans = []
    for name,logs in logs_data.items():
        for log in logs:
            if key in log:
                if log[key].lower() == str(value).lower():
                    ans.append(log)
    return ans

def get_all_kinds_of(key):
    all_types = []
    for name,logs in logs_data.items():
        for log in logs:
            if key in log and log[key] not in all_types:
                all_types.append(log[key])

    return all_types            

"""
time_part = { #any seconds in 10:39 on the 9-3-2018
        'sec' : '', 
        'min' : '39',
        'hour' :'10',
        'day' : '9',
        'month' : '3',
        'year' : '2018'
    }
"""
def get_all_logs_by_date(time_part):
    all_types = []
    for name,logs in logs_data.items():
        for log in logs:
            d = log['date']
            ok=True
            for k,v in time_part.items():
                if v:  #Empty means no treatment
                    if k not in d or str(v) != str(d[k]):
                        ok = False
            if ok:
                all_types.append(log)
    return all_types                        

def delete_all_logs():
    global logs_data
    logs_data={}
    smt_dir = '/var/log/smt'
    
    if os.path.exists(smt_dir):
        smt_files = os.listdir(smt_dir)
        if len(smt_files) == 0:
            print 'No files :('
        else:
            for fname in smt_files:
                os.remove( smt_dir + '/' + fname,'r')

    else:
        print '%s is not defined' % (smt_dir)


def is_in_danger(): #This function should be checked!
    global logs_data
    attacks=[]
    fw_logs = search_in_logs('subcategory','rogue dhcp') + search_in_logs('subcategory','arp spoofing') + search_in_logs('subcategory','dos')
    if len(danger) > 0:
        for log in fw_logs:
            if 'message' in log and 'Attack' in log['message'] and log['message'].count('{') == 1 and log['message'].count('}') == 1:
                attacks.append(log)
    else:
        return None   

    if len(attacks) > 0:
        return attacks
    else:
        return None    

read_logs()   
#is_in_danger()
#print search_in_logs('subcategory','arp spoofing')
#print search_in_logs('date','09-03-2018 10:30') #Works on every key (Go to supporting keys)
#print logs_data
#print get_all_kinds_of('subcategory') #Works on every key (Go to supporting keys)
#print get_all_logs_by_date({'hour': '11', 'min': '22', 'month': '3', 'sec': '34', 'year': '2018', 'day': '9'})


"""
Supporting keys:
    * uid
    * pid
    * mac
    * ip
    * syscall_name
    * filename
    * subcategory
    * date - other function
"""