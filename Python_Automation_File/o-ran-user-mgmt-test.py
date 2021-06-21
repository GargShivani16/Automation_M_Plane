import sys, os, warnings
#warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
import string
import xmltodict
#xml_1 = open('o-ran-interfaces.xml').read()
def demo(host, port, user, password, name, pas1, user_per):
    
    snippet = f"""
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <users xmlns="urn:o-ran:user-mgmt:1.0">
                    <user>
                        <name>{name}</name>
                        <account-type>PASSWORD</account-type>
                        <password>{pas1}</password>
                        <enabled>true</enabled>
                    </user>
                </users>
                </config>"""
    with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
        rpc=m.create_subscription()
        data1 = m.edit_config(target="running" , config=snippet)
        print(data1)
        
        ad_us = f'<user-name>{name}</user-name>'
        if user_per == "sudo":
            nacm_file = open('../Yang_xml/nacm_sudo.xml').read()
            nacm_file = nacm_file.format(add_sudo = ad_us)
        elif user_per == 'nms':
            nacm_file = open('../Yang_xml/nacm_nms.xml').read()
            nacm_file = nacm_file.format(add_nms = ad_us)
        elif user_per == 'swm':
            nacm_file = open('../Yang_xml/nacm_swm.xml').read()
            nacm_file = nacm_file.format(add_swm = ad_us)
        
        
        
        data2 = m.edit_config(target="running" , config=nacm_file, default_operation = 'replace')
        print(data2)

        
        n = m.take_notification()
        print(n.notification_xml)

        #m.edit_config(target='running', config=xml_1)

        u_name = '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <users xmlns="urn:o-ran:user-mgmt:1.0">	
                    <user>                                                        
                        <name></name>
                    </user>
                </users>
                </filter>
        '''

        
        user_name = m.get_config('running', u_name).data_xml
        dict_users = xmltodict.parse(str(user_name))
        Users = dict_users['data']['users']['user']
        for i in Users:
            User = f'''
            <users xmlns="urn:o-ran:user-mgmt:1.0">	
                <user>                                                        
                    <name>{i['name']}</name>
                </user>
            </users>
            '''
            try:
                value_user = m.get(('subtree', User)).data_xml
            except:
                print(f"Can't find the {i['name']}  user")

            dict_user = xmltodict.parse(str(value_user))
            print(f"\n\n*****validation  for {i['name']}*****\n\n")
            try:
                acc1 = dict_user['data']['users']['user']['account-type']
                if  acc1:
                    print("account-type - %s" %acc1)
            except:
                print('You have to configure usermgmt yang module for account-type')
            
            try:
                pwd1 = dict_user['data']['users']['user']['password']
                if pwd1:
                    print("password - %s" %pwd1)
            except:
                print('You have to configure usermgmt yang module for password')

            try:
                ena1 = dict_user['data']['users']['user']['enabled']
                if ena1:
                    print("enabled - %s" %ena1)
            except:
                print('You have to configure usermgmt yang module for enabled')
        
        
if __name__ == '__main__':
    #give the input configuration in xml file format
    #xml_1 = open('o-ran-hardware.xml').read()
    #give the input in the format hostname, port, username, password
    name = input("Enter name:\n")
    pas1 = input("Enter password:\n")
    user_per = input("Enter permission:\n")
    demo("192.168.1.10", 830, "root", "root", name ,pas1,user_per)

