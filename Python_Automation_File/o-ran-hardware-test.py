import sys, os, warnings
#warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager
from lxml import etree
import string
import xmltodict

def demo(host, port, user, password):
   with manager.connect(host=host, port=port, username=user, hostkey_verify=False, password=password) as m:
        xml_data = open("../Yang_xml/hardware.xml").read()
        u1 = f'''
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        {xml_data}
        </config>'''
        data = m.edit_config(target='running', config = u1, default_operation = 'replace')
        print(data)

        ru_module = '''<hardware xmlns="urn:ietf:params:xml:ns:yang:ietf-hardware">
                            <component>
                                <name>ru-module</name>
                            </component>
                        </hardware>'''

        try:
            value_module = m.get(('subtree', ru_module)).data_xml
                
        except:
            print("Can't find the ru-module")

        dict_module = xmltodict.parse(str(value_module))

        print("\n\n******validation for ru-module******\n\n")
        try:
            Class = dict_module['data']['hardware']['component']['class']['#text']
            if Class:
                print("class = %s" %Class)
        except:
            print('You have to configure usermgmt yang module for class')

        try:
            oper_state = dict_module['data']['hardware']['component']['state']['oper-state']
            if oper_state:
                print("oper-state = %s" %oper_state)
        except:
            print('You have to configure usermgmt yang module for oper-state')
        
        try:
            availability_state = dict_module['data']['hardware']['component']['state']['availability-state']['#text']
            if availability_state:
                print("availability-state = %s" %availability_state)
        except:
            print('You have to configure usermgmt yang module for availability-state')

        try:
            o_ran_name = dict_module['data']['hardware']['component']['o-ran-name']['#text']
            if o_ran_name:
                print("o-ran-name = %s" %o_ran_name)
        except:
            print('You have to configure usermgmt yang module for o-ran-name')


        try:
            description = dict_module['data']['hardware']['component']['description']
            if description:
                print("description = %s"%description)
        except:
            print('You have to configure usermgmt yang module for description')

        try:
            hw_rev = dict_module['data']['hardware']['component']['hardware-rev']
            #print(hw_rev)
        
            if not hw_rev:
                print("hardware-rev = %s" %hw_rev)
        except:
            print('You have to configure usermgmt yang module for hardware-rev')
            
        
        try:
            sw_rev = dict_module['data']['hardware']['component']['software-rev']
            #print(sw_rev)
        
            if not sw_rev:
                print("software-rev = %s" %sw_rev)
        except:
            print('You have to configure usermgmt yang module for software-rev')
            


        try:
            sl_no = dict_module['data']['hardware']['component']['serial-num']
            #print(sl_no)
        
            if not sl_no:
                print("serial-num = %s" %sl_no)
        except:
            print('You have to configure usermgmt yang module for serial-num')
            

        try:
            mfg_name = dict_module['data']['hardware']['component']['mfg-name']
            #print(mfg_name)
            if not mfg_name:
                print("mfg-name = %s" %mfg_name)
        except:
            print('You have to configure usermgmt yang module for mfg-name')
            

        try:
            model_name = dict_module['data']['hardware']['component']['model-name']
            if model_name :
                print("model-name = %s" %model_name)
        except:
            print('You have to configure usermgmt yang module for model-name')

        try:
            uuid = dict_module['data']['hardware']['component']['uuid']
            if uuid :
                print("uuid is %s" %uuid)
        except:
            print('You have to configure usermgmt yang module for uuid')

        try:
            contains_child = dict_module['data']['hardware']['component']['contains-child']
            if contains_child :
                print("contains-child = %s" %contains_child)
        except:
            print('You have to configure usermgmt yang module for contains-child')
        try:
            product_code = dict_module['data']['hardware']['component']['product-code']['#text']
            if product_code :
                print("product-code = %s" %product_code)
        except:
            print('You have to configure usermgmt yang module for product-code')

        ru_ports = '''
                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <hardware xmlns="urn:ietf:params:xml:ns:yang:ietf-hardware">
                        <component>
                            <name></name>
                        </component>
                    </hardware>
                    </filter>
            '''

        module_name = m.get_config('running', ru_ports).data_xml
        dict_module = xmltodict.parse(str(module_name))
        Ru_ports = dict_module['data']['hardware']['component']
        l = len(Ru_ports) 

        for i in range(1,l):
                Module = f'''<hardware xmlns="urn:ietf:params:xml:ns:yang:ietf-hardware">
                                <component>
                                    <name>{Ru_ports[i]['name']}</name>
                                </component>
                            </hardware>'''
                try:
                    value_port = m.get(('subtree', Module)).data_xml
                    
                except:
                    print(f"Can't find the {Ru_ports[i]['name']}")

                dict_port = xmltodict.parse(str(value_port))


                print(f"\n\n******validation failed for {Ru_ports[i]['name']}******\n\n")

                try:
                    Class1 = dict_port['data']['hardware']['component']['class']['#text']
                    if Class1 :
                        print("class = %s" %Class1)
                except:
                    print('You have to configure usermgmt yang module for class')

                try:
                    parent1 = dict_port['data']['hardware']['component']['parent']
                    if parent1:
                        print("parent = %s" %parent1)
                except:
                    print('You have to configure usermgmt yang module for parent')

                try:
                    parent_rel1 = dict_port['data']['hardware']['component']['parent-rel-pos']
                    if parent_rel1:
                        print("parent-rel-pos = %s" %parent_rel1)
                except:
                    print('You have to configure usermgmt yang module for parent-rel-pos')

                try:
                    oper_state1 = dict_port['data']['hardware']['component']['state']['oper-state']
                    if oper_state1:
                        print("oper-state = %s" %oper_state1)
                except:
                    print('You have to configure usermgmt yang module for oper-state')

                try:
                    avail_state1 = dict_port['data']['hardware']['component']['state']['availability-state']['#text']
                    if avail_state1:
                        print("availability-state = %s" %avail_state1)
                except:
                    print('You have to configure usermgmt yang module for availability-state')

                try:
                    o_ran_name1 = dict_port['data']['hardware']['component']['o-ran-name']['#text']
                    if o_ran_name1:
                        print("o-ran-name = %s" %o_ran_name1)
                except:
                    print('You have to configure usermgmt yang module for o-ran-name')

                try:
                    descrip1 = dict_port['data']['hardware']['component']['description']
                    if descrip1:
                        print("Description = %s" %descrip1)
                except:
                    print('You have to configure usermgmt yang module for description')

                try:
                    hw_rev1 = dict_port['data']['hardware']['component']['hardware-rev']
                    if hw_rev1:
                        print("hardware-rev = %s" %hw_rev1)
                except:
                    print('You have to configure usermgmt yang module for hardware-rev')

                try:
                    is_fru1 = dict_port['data']['hardware']['component']['is-fru']
                    if is_fru1:
                        print("is_fru given as %s" %is_fru1)
                except:
                    print('You have to configure usermgmt yang module for is-fru')

                try:
                    mfg_date1 = dict_port['data']['hardware']['component']['mfg-date']
                    if mfg_date1:
                        print("mfg-date = %s" %mfg_date1)
                except:
                    print('You have to configure usermgmt yang module for mfg-date')
      
       
if __name__ == '__main__':
   #give the input configuration in xml file format
   #xml_1 = open('o-ran-hardware.xml').read()
   #give the input in the format hostname, port, username, password
   demo("192.168.1.10", 830, "root", "root")

