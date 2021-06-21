import sys
import os
import warnings
# warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
from lxml import etree
import string
import xmltodict


def demo(host, port, user, password):
   with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
        # m.edit_config(target='running', config=xml_1)
        rpc=m.create_subscription()
        xml_data = open('../Yang_xml/processing.xml').read()
        u1 = f'''
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                {xml_data}
            </config>
        '''
        data2 = m.edit_config(target="running" , config=u1, default_operation = 'replace')
        print(data2)

        
        n = m.take_notification()
        print(n.notification_xml)
        element0 = '''
        <processing-elements xmlns="urn:o-ran:processing-element:1.0">
         <ru-elements>
             <name>element0</name>
         </ru-elements>
        </processing-elements>
        '''
        com = '''
        <processing-elements xmlns="urn:o-ran:processing-element:1.0">
        </processing-elements>
        '''

        try:
            value_elements = m.get(('subtree', element0)).data_xml
        except:
            print("Can't find the element0")

        try:
            value_com = m.get(('subtree', com)).data_xml
        except:
            print("can't find the processing-elements")


        dict_elements = xmltodict.parse(str(value_elements))
        # print(dict_module)
        dict_com = xmltodict.parse(str(value_com))
        

        print("\n\n******validation failed for element0******\n\n")
        try:
            Transport_session_type = dict_com['data']['processing-elements']['transport-session-type']
            if Transport_session_type:
                print("Transport_session_type is %s" %Transport_session_type)
        except:
            print(
                'Transport_session_type not found')
                
            
        try:
            Interface_name = dict_elements['data']['processing-elements']['ru-elements']['transport-flow']['interface-name']
            if Interface_name:
                print("Interface_name is %s" %Interface_name)
        except:
            print(
                'Interface_name not found')
      
        try:
            RU_mac_address = dict_elements['data']['processing-elements']['ru-elements']['transport-flow']['eth-flow']['ru-mac-address']
            if RU_mac_address:
                print("RU_mac_addres is %s" %RU_mac_address)
        except:
            print(
                'RU_mac_addres not found')

        try:
            Vlan_id = dict_elements['data']['processing-elements']['ru-elements']['transport-flow']['eth-flow']['vlan-id']
            if Vlan_id:
                print("Vlan_id is %s" %Vlan_id)
        except:
            print(
                'Vlan_id not found')
        
        try:
            O_DU_MAC_address = dict_elements['data']['processing-elements']['ru-elements']['transport-flow']['eth-flow']['o-du-mac-address']
            if O_DU_MAC_address== '00:0e:09:87:63:7a':
                print("O_DU_MAC_address is %s" %O_DU_MAC_address)
        except:
            print(
                'O_DU_MAC_address not found')

if __name__ == '__main__':
   # give the input configuration in xml file format
   # xml_1 = open('o-ran-hardware.xml').read()
   # give the input in the format hostname, port, username, password
   demo("192.168.1.10", 830, "root", "root")
