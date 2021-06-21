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
        #m.edit_config(target='running', config=xml_1)
        # print(m.get.data_link)
        xml_1 = open('../Yang_xml/operation.xml').read()
        snippet = f"""
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                {xml_1}
                </config>"""
        data = m.edit_config(target='running', config=snippet, default_operation = 'replace')
        print(data)
        operational = '''
        <operational-info xmlns="urn:o-ran:operations:1.0">
        </operational-info>
        '''

        CLOCK = '''
        <operational-info xmlns="urn:o-ran:operations:1.0">
            <clock>
                <timezone-utc-offset></timezone-utc-offset>
            </clock>
        </operational-info>
        '''

        DECLARATION = '''
        <operational-info xmlns="urn:o-ran:operations:1.0">
            <declarations></declarations>
        </operational-info>
        '''

        OPERATION_STATE = '''
        <operational-info xmlns="urn:o-ran:operations:1.0">
            <operational-state></operational-state>
        </operational-info>
        '''

        try:
            value_operational = m.get(('subtree', operational)).data_xml

        except:
            print("Can't find the value_operational")

        try:
            value_CLOCK = m.get(('subtree', CLOCK)).data_xml
            #print(value_CLOCK)

        except:
            print("Can't find the value_CLOCK")

        try:
            value_DECLARATION = m.get(('subtree', DECLARATION)).data_xml

        except:
            print("Can't find the value_DECLARATION")

        try:
            value_OPERATION_STATE = m.get(('subtree', OPERATION_STATE)).data_xml

        except:
            print("Can't find the value_OPERATION_STATE")

        dict_operational = xmltodict.parse(str(value_operational))
        # dict_CLOCK = dict_operational['data']['operational-info']['clock']
        # print(dict_CLOCK)
        # dict_DECLARATION = xmltodict.parse(str(value_DECLARATION))
        # dict_OPERATION_STATE = xmltodict.parse(str(value_OPERATION_STATE))

        print("\n\n******validation for m-plane-operations******\n\n")
        try:
            Timezone_utc_offset = dict_operational['data']['operational-info']['clock']['timezone-utc-offset']
            if Timezone_utc_offset:
                print("Timezone_utc_offset = %s" %
                      Timezone_utc_offset)
        except:
            print(
                'Timezone_utc_offset not found')

        try:
            Timezone_Name = dict_operational['data']['operational-info']['clock']['timezone-name']
            if Timezone_Name:
                print("Timezone_Name = %s" % Timezone_Name)
        except:
            print(
                'Timezone_Name not found')

        try:
            Re_call_home_no_ssh_timer = dict_operational['data'][
                'operational-info']['re-call-home-no-ssh-timer']
            if Re_call_home_no_ssh_timer:
                print("Re_call_home_no_ssh_timer = %s" %
                      Re_call_home_no_ssh_timer)
        except:
            print(
                'Re_call_home_no_ssh_timer not found')

        try:
            RU_Instance_id = dict_operational['data'][
                'operational-info']['declaration']['ru-instance-id']
            if RU_Instance_id:
                print("RU_Instance_id = %s" % RU_Instance_id)
        except:
            print(
                'RU_Instance_id not found')
        
        try:
            Supported_mplane_version = dict_operational['data'][
                'operational-info']['declaration']['supported-mplane-version']
            if Supported_mplane_version:
                print("Supported_mplane_version = %s" % Supported_mplane_version)
        except:
            print(
                'Supported_mplane_version not found')

        try:
            Supported_cusplane_version = dict_operational['data'][
                'operational-info']['declaration']['supported-cusplane-version']
            if Supported_cusplane_version:
                print("Supported_cusplane_version = %s" % Supported_cusplane_version)
        except:
            print(
                'Supported_cusplane_version not found')

        try:
            Protocol_Name = dict_operational['data'][
                'operational-info']['declaration']['supported-header-mechanism']['protocol']
            if Protocol_Name:
                print(" Protocol = %s" % Protocol_Name)
        except:
            print(
                'Protocol not found')

        try:
            Protocol_version = dict_operational['data'][
                'operational-info']['declaration']['supported-header-mechanism']['protocol-version']
            if Protocol_version:
                print(" Protocol_version = %s" % Protocol_version)
        except:
            print(
                'Protocol_version not found')

        try:
            Restart_cause = dict_operational['data'][
                'operational-info']['operational-state']['restart-cause']
            if Restart_cause:
                print(" Restart_cause = %s" % Restart_cause)
        except:
            print(
                'Restart_cause not found')

        try:
            Restart_datetime = dict_operational['data'][
                'operational-info']['operational-state']['restart-datetime']
            if Restart_datetime:
                print(" Restart_datetime = %s" % Restart_datetime)
        except:
            print(
                'Restart_datetime not found')



if __name__ == '__main__':
    # give the input configuration in xml file format
    # xml_1 = open('o-ran-hardware.xml').read()
    # give the input in the format hostname, port, username, password
    demo("192.168.1.10", 830, "root", "root")
