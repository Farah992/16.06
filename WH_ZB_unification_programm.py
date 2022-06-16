from email import message
from itertools import count
from ntpath import join
import readline
from wsgiref import headers
import io
import subprocess
import random
import wirelessHART_node
import ZigBee_node
import datetime

start = datetime.datetime.utcnow()


hh_1_wh , hh_2_wh , hh_3_wh , hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh, h_1_wh, h_2_wh , h3_wh , h4_wh , h_5_wh , h_6_wh ,h7_wh = wirelessHART_node.calcHeaders_wh()
header_msg_wh = wirelessHART_node.calcHeaderMssg_wh(hh_1_wh , hh_2_wh , hh_3_wh, hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh) 
pay_hex_wh, sum_wh,payload_wh= wirelessHART_node.calcPayload_wh()
crc_wh,res_2_wh,sum_all_wh = wirelessHART_node.calcCRC_wh(h_1_wh , h_2_wh , h3_wh , h4_wh , h_5_wh , h_6_wh ,h7_wh, sum_wh )
message_wh = wirelessHART_node.getMssg_wh(header_msg_wh , payload_wh , crc_wh)

hh_1_zb , hh_2_zb , hh_3_zb , h1_zb , h_2_zb, h3_zb = ZigBee_node.calcHeaders_zb()
header_msg_zb = ZigBee_node.calcHeaderMssg_zb(hh_1_zb , hh_2_zb , hh_3_zb)
pay_hex_zb, sum_zb,payload_zb = ZigBee_node.calcPayload_zb()
crc_zb,res_2_zb,sum_all_zb = ZigBee_node.calcCRC_zb(h1_zb , h_2_zb , h3_zb , sum_zb) 
message_zb = ZigBee_node.getMssg_zb( header_msg_zb , payload_zb , crc_zb)

unification_headers = bytearray()
#crc_wh_2 = bytearray()
#crc_zb_2 = bytearray()

proc = subprocess.Popen(["python", "wirelessHART_node.py", ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

procOutput = proc.communicate()[0]
print(procOutput)
print("-------------------")

data1 = proc  
print(data1)

proc_2 = subprocess.Popen(["python", "ZigBee_node.py", ''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
procOutput_2 = proc_2.communicate()[0]
print(procOutput)
print("-------------------")

data2 = proc_2
print(data2)

#checking check_sum

def check_sum_wh(sum_all_wh,res_2_wh):
    check_sum_wh = sum_all_wh + res_2_wh
    data_2 = hex(check_sum_wh)
    info_2 = data_2[-2:] # the 8 lowest bytes
    if info_2 =="ff":
        print("check_sum_wh is correct")
    else:
        print("error,check it again")
        exit()

check_sum_wh(sum_all_wh,res_2_wh)

def check_sum_zb(sum_all_zb,res_2_zb):
    check_sum_zb = sum_all_zb + res_2_zb
    data_2 = hex(check_sum_zb)
    info_2 = data_2[-2:]
    if info_2 =="ff":
        print("check_sum_zb is correct")
    else:
        print("error,check it again")
        exit()
check_sum_zb(sum_all_zb,res_2_zb)
   

def unification(hh_1_wh, hh_1_zb, hh_2_wh, hh_2_zb ,hh_3_wh,hh_3_zb , hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh):
    unification_headers = bytearray()

    if hh_1_wh or hh_1_zb :
        unification_headers += hh_1_zb
    if hh_2_wh or hh_2_zb:
        unification_headers += hh_2_zb
    if hh_3_wh or hh_3_zb :
        unification_headers += hh_3_zb
    if hh_4_wh:
        unification_headers += hh_4_wh
    if hh_5_wh:
        unification_headers += hh_5_wh
    if hh_6_wh:
        unification_headers += hh_6_wh
    if hh_7_wh:
        unification_headers += hh_7_wh
    else:
        print("error")
    
    print("unification headers",unification_headers)   
    print("length of headers",len(unification_headers)) 
    #print("unification headers is","".join("\\x%02x" % i for i in unification_headers))
    print("unification headers is",bytes("".join("\\x%02x" % i for i in unification_headers), 'utf-8'))
    return unification_headers

def calcPayload_wh():
    print("payload_wh is",payload_wh)
calcPayload_wh()

def calcPayload_zb():
    print("payload_zb is",payload_zb)
calcPayload_zb()

def calcCRC_wh(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_wh):
    global crc_wh_2
    header_int = h1_zb + h_2_zb + h3_zb + h4_wh + h_5_wh + h_6_wh + h7_wh # as intergers sum of headers
    headers_hex = hex(header_int)  

    sum_all_wh = sum_wh + header_int # int sum of headers + payload
    data = hex(sum_all_wh)
    info = data[-2:]
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  Заголовок (контрольная сумма)	
    crc_wh_2 = res_2.to_bytes(2, 'little') # as a  byte
    print("crc_wh",crc_wh_2)
    return crc_wh_2
calcCRC_wh(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_wh)


def calcCRC_zb(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_zb):
    global crc_zb_2
    header_int = h1_zb + h_2_zb + h3_zb + h4_wh + h_5_wh + h_6_wh + h7_wh # as intergers sum of headers
    headers_hex = hex(header_int)  
    sum_all_zb = sum_zb + header_int # int sum o headers + payload
    data = hex(sum_all_zb)
    info = data[-2:]
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  Заголовок (контрольная сумма)	
    crc_zb_2 = res_2.to_bytes(2, 'little') # as a  byte
    print("crc_zb",crc_zb_2)
    return crc_zb_2
calcCRC_zb(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_zb)


def getUnifiedMssg_wh(unification_headers , payload_wh , crc_wh_2):
    crc_wh_2
    new_message_wh =  unification_headers + payload_wh + crc_wh_2 # as a byte message
    print("new_message_wh",new_message_wh)
    length_message_wh = len(new_message_wh)
    print("length_message_wh in bytes is",length_message_wh)
    unified_message_wh = "".join("\\x%02x" % i for i in new_message_wh)
    print("unified message of WH is",unified_message_wh)
    #print("unified message of WH is",bytes("".join("\\x%02x" % i for i in unified_message_wh), 'utf-8'))
    return unified_message_wh

getUnifiedMssg_wh(unification_headers , payload_wh , crc_wh_2)

def getUnifiedMssg_zb(unification_headers , payload_zb , crc_zb_2):
    new_message_zb =  unification_headers + payload_zb + crc_zb_2 # as a byte message
    #print(new_message_zb)
    print("new_message_zb",new_message_zb)
    length_message_zb= len(new_message_zb)
    print("length_message_zb in bytes is",length_message_zb)
    unified_message_zb = "".join("\\x%02x" % i for i in new_message_zb)
    print("unified message of zigbee is",unified_message_zb)
    #print("unified message of zigbee is",bytes("".join("\\x%02x" % i for i in unified_message_zb), 'utf-8'))
    return unified_message_zb
    
getUnifiedMssg_zb(unification_headers , payload_zb , crc_zb_2)

print("end of unification programm")

end = datetime.datetime.utcnow()
diff = end-start
execTime = diff.total_seconds()
print("execTime in seconds",execTime)
