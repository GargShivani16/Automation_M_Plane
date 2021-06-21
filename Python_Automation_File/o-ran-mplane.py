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
        xml_1 = open('../Yang_xml/mplane.xml').read()
        snippet = f"""
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                {xml_1}
                </config>"""
        data = m.edit_config(target='running', config = snippet, default_operation = 'replace')
        print(data)
        interfaces = '''
       <mplane-info xmlns="urn:o-ran:mplane-interfaces:1.0">
            <m-plane-interfaces>
            </m-plane-interfaces>
       </mplane-info>
       '''

        com = '''
       <mplane-info xmlns="urn:o-ran:mplane-interfaces:1.0">
       </mplane-info>
       '''
        try:
            value_interfaces = m.get(('subtree', interfaces)).data_xml
            # print(value_interfaces)
        except:
            print("Can't find the value_interfaces")

        try:
            value_com = m.get(('subtree', com)).data_xml
            # print(value_com)
        except:
            print("Can't find the value_com")

        dict_interfaces = xmltodict.parse(str(value_interfaces))
        #print('dict_module :',dict_module)
        dict_com = xmltodict.parse(str(value_com))

        print("\n\n******validation for m-plane-interfaces******\n\n")
        try:
            Searchable_Access_Vlans = dict_interfaces['data'][
                'mplane-info']['searchable-mplane-access-vlans-info']['searchable-access-vlans']
            if Searchable_Access_Vlans:
                print("Searchable_Access_Vlans = %s" % Searchable_Access_Vlans)
        except:
            print(
                'Searchable_Access_Vlans not found')

        try:
            Lowest_Vlan_id = dict_interfaces['data'][
                'mplane-info']['searchable-mplane-access-vlans-info']['vlan-range']['lowest-vlan-id']
            if Lowest_Vlan_id:
                print("Searchable_Access_Vlans = %s" % Lowest_Vlan_id)
        except:
            print(
                'Lowest_Vlan_id not found')

        try:
            Highest_Vlan_id = dict_interfaces['data'][
                'mplane-info']['searchable-mplane-access-vlans-info']['vlan-range']['highest-vlan-id']
            if Highest_Vlan_id:
                print("Highest_Vlan_id = %s" % Highest_Vlan_id)
        except:
            print(
                'Highest_Vlan_id not found')

        try:
            Call_home_ssh_port = dict_interfaces['data'][
                'mplane-info']['m-plane-interfaces']['m-plane-ssh-ports']['call-home-ssh-port']
            if Call_home_ssh_port:
                print("Call_home_ssh_port = %s" % Call_home_ssh_port)
        except:
            print(
                'Call_home_ssh_port not found')

        try:
            Server_ssh_port = dict_interfaces['data']['mplane-info']['m-plane-interfaces']['m-plane-ssh-ports']['server-ssh-port']
            if Server_ssh_port:
                print("Server_ssh_port = %s" % Server_ssh_port)
        except:
            print(
                'Server_ssh_port not found')

        try:
            Interface_Name = dict_interfaces['data']['mplane-info']['m-plane-interfaces']['m-plane-sub-interfaces']['interface-name']
            if Interface_Name:
                print("Interface_Name = %s" % Interface_Name)
        except:
            print(
                'Interface_Name not found')

        try:
            Sub_Interface = dict_interfaces['data']['mplane-info']['m-plane-interfaces']['m-plane-sub-interfaces']['sub-interface']
            if Sub_Interface:
                print("Sub_Interface = %s" % Sub_Interface)
        except:
            print(
                'Sub_Interface not found')


if __name__ == '__main__':
    # give the input configuration in xml file format
    # xml_1 = open('o-ran-hardware.xml').read()
    # give the input in the format hostname, port, username, password
    demo("192.168.1.10", 830, "root", "root")
