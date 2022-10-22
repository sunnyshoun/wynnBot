import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import os

dbkey = json.loads(os.environ.get('firebase_api_json'))
dburl = os.environ.get('firebase_url')

try:
    cred = credentials.Certificate(dbkey)
    firebase_admin.initialize_app(cred, {'databaseURL': dburl})
except:
    pass
ref = db.reference()

vip_datas = ref.child('vipdata').get()
malicious_links = ref.child('malicious_link').get()
safe_links = ref.child('safe_link').get()
restart = ref.child('restart').get()
active_point = ref.child('active_point').get()
if active_point == None:
    active_point = {}
    
def refresh_urls():
    malicious=set(malicious_links)
    safe=set(safe_links)
    return malicious,safe

def get_vipdatas():
    boost_member_list=vip_datas['members']
    boost_channel_list=vip_datas['channels']
    chat_dict={}
    for i in range(len(boost_member_list)):
        chat_dict[boost_member_list[i]] = boost_channel_list[i]
    return chat_dict,boost_member_list,boost_channel_list

def get_vipmembers():
    return vip_datas['members']

def get_vipchats():
    return vip_datas['channels']
    
def del_vipdata(memberid):
    chat_dict,boost_member_list,boost_channel_list=get_vipdatas()
    vip_datas['members'].remove(memberid)
    vip_datas['channels'].remove(chat_dict[memberid])
    ref.child('vipdata').set(vip_datas)

def add_vipdata(memberid,chatid):
    vip_datas['members'].append(memberid)
    vip_datas['channels'].append(chatid)
    ref.child('vipdata').set(vip_datas)

def is_restart():
    restart_argument=restart['restart_context']
    if restart_argument != 'NO':
        return int(restart_argument),int(restart['edit_msg_id'])
    else:
        return False,False

def set_restart(value,edit_msg_id=''):
    restart['restart_context'] = value
    restart['edit_msg_id'] = edit_msg_id
    ref.child('restart').set(restart)

def add_malicious(url):
    if url not in set(malicious_links):
        malicious_links.append(url)
        ref.child('malicious_link').set(malicious_links)

def add_safe(domain):
    if domain not in set(safe_links):
        safe_links.append(domain)
        ref.child('safe_link').set(safe_links)

def del_malicious(url):
    if url in set(malicious_links):
        malicious_links.remove(url)
        ref.child('malicious_link').set(malicious_links)

def del_safe(domain):
    if domain in set(safe_links):
        safe_links.remove(domain)
        ref.child('safe_link').set(safe_links)

def get_active_point():
    global active_point
    active_point = ref.child('active_point').get()
    if active_point == None:
        active_point = {}
    adict = {k: v for k, v in sorted(active_point.items(), key=lambda item: item[1], reverse=True)}
    return adict

def reset_member_active_point():
    ref.child('active_point').set({})

def get_reset_num():
    return ref.child('reset_num').get()

def set_reset_num(num):
    ref.child('reset_num').set(num)

def add_active_point(id):
    id = str(id)
    if id in set(active_point.keys()):
        active_point[id] += 1
    else:
        active_point[id] = 1
    ref.child('active_point').child(id).set(active_point[id])

def remove_active_point(id):
    id = str(id)
    if id in set(active_point.keys()):
        active_point[id] -= 1
        if active_point[id] == 0:
            active_point.pop(id, None)
            ref.child('active_point').child(id).set({})
        else:
            ref.child('active_point').child(id).set(active_point[id])

def get_last_member():
    return int(ref.child('last_member').get())

def set_last_member(num):
    ref.child('last_member').set(str(num))

def add_rank_logs(name,y,m,m_week):
    rank_logs = ref.child('rank_logs').get()
    if y not in rank_logs.keys():
        rank_logs[y]={}
    if m not in rank_logs[y].keys():
        rank_logs[y][m] = {}
    rank_logs[y][m]['|'+str(m_week)+'|'] = name
    ref.child('rank_logs').set(rank_logs)

def get_rank_logs():
    return ref.child('rank_logs').get()