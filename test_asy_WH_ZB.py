import asyncio
from email import message
from pickle import TRUE
from tracemalloc import stop
from wsgiref import headers
import io
import random
import wirelessHART_node
import ZigBee_node
import datetime
import time
import timeit
from time import perf_counter


start = datetime.datetime.utcnow()

hh_1_wh ,hh_1_zb ,hh_2_wh, hh_2_zb ,hh_3_wh,hh_3_zb , hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh = [0xFF for i in range (10)]
h1_zb , h_2_zb , h3_zb, h_1_wh, h_2_wh, h3_wh, h4_wh, h_5_wh, h_6_wh, h7_wh = [0 for i in range (10)]
payload_wh= [0xFF for i in range (128)]
payload_zb = [0xFF for i in range (128)]
counter_wh = 0
counter_zb = 0

maxCounter = 3

hh_1_zb , hh_2_zb , hh_3_zb , h1_zb , h_2_zb, h3_zb = ZigBee_node.calcHeaders_zb()
header_msg_zb = ZigBee_node.calcHeaderMssg_zb(hh_1_zb , hh_2_zb , hh_3_zb)
pay_hex_zb, sum_zb,payload_zb = ZigBee_node.calcPayload_zb()
crc_zb,res_2_zb,sum_all_zb = ZigBee_node.calcCRC_zb(h1_zb , h_2_zb , h3_zb , sum_zb) 
message_zb = ZigBee_node.getMssg_zb( header_msg_zb , payload_zb , crc_zb)

hh_1_wh , hh_2_wh , hh_3_wh , hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh, h_1_wh, h_2_wh , h3_wh , h4_wh , h_5_wh , h_6_wh ,h7_wh = wirelessHART_node.calcHeaders_wh()
header_msg_wh = wirelessHART_node.calcHeaderMssg_wh(hh_1_wh , hh_2_wh , hh_3_wh, hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh) 
pay_hex_wh, sum_wh,payload_wh= wirelessHART_node.calcPayload_wh()
crc_wh,res_2_wh,sum_all_wh = wirelessHART_node.calcCRC_wh(h_1_wh , h_2_wh , h3_wh , h4_wh , h_5_wh , h_6_wh ,h7_wh, sum_wh )
message_wh = wirelessHART_node.getMssg_wh(header_msg_wh , payload_wh , crc_wh)


# check sum
def check_sum_wh(sum_all_wh,res_2_wh):
    check_sum_wh = sum_all_wh + res_2_wh
    data_2 = hex(check_sum_wh)
    info_2 = data_2[-2:]
    if info_2 =="ff":
        print("check_sum_wh is correct")
    else:
        print("error,check it again")
check_sum_wh(sum_all_wh,res_2_wh)

def check_sum_zb(sum_all_zb,res_2_zb):
    check_sum_zb = sum_all_zb + res_2_zb
    data_2 = hex(check_sum_zb)
    info_2 = data_2[-2:]
    if info_2 =="ff":
        print("check_sum_zb is correct")
    else:
        print("error,check it again")
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
    return unification_headers 

print("--------------------------------------------------------")

def calcCRC_wh(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_wh):
   
    header_int = h1_zb + h_2_zb + h3_zb + h4_wh + h_5_wh + h_6_wh +h7_wh # as intergers sum of headers
    headers_hex = hex(header_int)  
    headers_pay = headers_hex + pay_hex_wh # headers + payload
    sum_all_wh = sum_wh + header_int # int sum o headers + payload
    data = hex(sum_all_wh)
    info = data[-2:]
    #print (info)
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  ?????????????????? (?????????????????????? ??????????)	
    print(h_8)
    crc_wh_2 = res_2.to_bytes(2, 'little') # as a  byte
    print("crc_wh_2",crc_wh_2)
    return crc_wh_2
calcCRC_wh(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_wh)
print("--------------------------------------------------------")

def calcCRC_zb(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_zb):
   
    header_int = h1_zb + h_2_zb + h3_zb + h4_wh + h_5_wh + h_6_wh +h7_wh # as intergers sum of headers
    headers_hex = hex(header_int)  
    headers_pay = headers_hex + pay_hex_zb # headers + payload
    sum_all_zb = sum_zb + header_int # int sum o headers + payload
    data = hex(sum_all_zb)
    info = data[-2:]
    #print (info)
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  ?????????????????? (?????????????????????? ??????????)	
    print(h_8)
    crc_zb_2 = res_2.to_bytes(2, 'little') # as a  byte
    print("crc_zb_2",crc_zb_2)
    return crc_zb_2
calcCRC_zb(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_zb)
print("--------------------------------------------------------")

def getUnifiedMssg_wh(unification_headers , payload_wh , crc_wh_2):
    new_message_wh =  unification_headers + payload_wh + crc_wh_2 # as a byte message
    print(new_message_wh)
    length = len(new_message_wh)
    print("length of message_wh",length)
    return new_message_wh
print("--------------------------------------------------------")
def getUnifiedMssg_zb(unification_headers , payload_zb, crc_zb_2):
    new_message_zb =  unification_headers + payload_zb + crc_zb_2 # as a byte message
    print(new_message_zb)
    length = len(new_message_zb)
    print("length of message_zb",length)
    return new_message_zb
print("--------------------------------------------------------")



def Creat_unifided_Packet(caller):
    global counter_zb,counter_wh
    global crc_wh_2,crc_zb_2
    start_time_wh

    t = 0
    unification_headers = unification(hh_1_wh, hh_1_zb, hh_2_wh, hh_2_zb ,hh_3_wh,hh_3_zb , hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh)
    pay_hex_wh,sum_wh,payload_wh = wirelessHART_node.calcPayload_wh()
    pay_hex_zb,sum_zb,payload_zb = ZigBee_node.calcPayload_zb()
    crc_wh_2 = calcCRC_wh(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_wh)
    crc_zb_2= calcCRC_zb(h1_zb , h_2_zb , h3_zb , h4_wh , h_5_wh , h_6_wh , h7_wh , sum_zb)

    if (caller =="zb" and counter_zb <= counter_wh):
        new_message_zb = getUnifiedMssg_zb(unification_headers , payload_zb, crc_zb_2)
        #new_message_wh  = getUnifiedMssg_wh(unification_headers , payload_wh , crc_wh_2)
        print("new_message_zb is",new_message_zb)
        print("counter_zb",counter_zb)
        print("counter_wh",counter_wh)
        
        final_execution_time_wh = datetime.datetime.utcnow() - start_time_wh
        execTime_final_wh = final_execution_time_wh.total_seconds()
        print("Time until now is ", execTime_final_wh)
        print("time from - to: ", start_time_wh, datetime.datetime.utcnow())

    if (caller =="wh" and counter_wh >= counter_zb):
        
        new_message_wh = getUnifiedMssg_wh(unification_headers , payload_wh , crc_wh_2)
        #new_message_zb = getUnifiedMssg_zb(unification_headers , payload_zb, crc_zb_2)
        print("new_message_wh is",new_message_wh)
        print("counter_wh",counter_wh)
        print("counter_zb",counter_zb)
        
        final_execution_time_wh = datetime.datetime.utcnow() - start_time_wh
        execTime_final_wh = final_execution_time_wh.total_seconds()
        print("Time until now is ", execTime_final_wh)
        print("time from - to: ", start_time_wh, datetime.datetime.utcnow())
    if counter_wh == counter_zb == maxCounter:

        print("Execution finished")
        final_execution_time_wh = datetime.datetime.utcnow() - start_time_wh
        execTime_final_wh = final_execution_time_wh.total_seconds()
        print("Execution time is ", execTime_final_wh)
        print("time from - to: ", start_time_wh, datetime.datetime.utcnow())
        if execTime_final_wh > 3:
            print("Time exceeded by:", execTime_final_wh-3)
    



#receiver
async def WH():

    global counter_wh
    global hh_1_wh, hh_2_wh, hh_3_wh, hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh,  h_1_wh , h_2_wh ,h3_wh,h4_wh , h_5_wh , h_6_wh , h7_wh,payload_wh,crc_wh 
    #you should call the wh function from here
    hh_1_wh,hh_2_wh,hh_3_wh,hh_4_wh,hh_5_wh,hh_6_wh ,hh_7_wh,h_1_wh, h_2_wh, h_5_wh ,h_6_wh ,h3_wh, h4_wh,h7_wh  = wirelessHART_node.calcHeaders_wh()
    header_msg_wh = wirelessHART_node.calcHeaderMssg_wh(hh_1_wh, hh_2_wh, hh_3_wh, hh_4_wh , hh_5_wh , hh_6_wh ,hh_7_wh) 
    pay_hex_wh,sum_wh,payload_wh = wirelessHART_node.calcPayload_wh()
    crc_wh = wirelessHART_node.calcCRC_wh(h_1_wh , h_2_wh , h3_wh , h4_wh , h_5_wh , h_6_wh ,h7_wh, sum_wh)
    #message_wh = wirelessHART_node.getMssg_wh(header_msg_wh , payload_wh , crc_wh)
    #await asyncio.sleep(1) #just for testing 
    print("-----------------------------------------------------------------------------------")
    counter_wh += 1
    Creat_unifided_Packet("wh")


#receiver
start_zb = datetime.datetime.utcnow()
async def ZigBee():
    global counter_zb
    #you should call the Zigbee function from here
    global hh_1_zb , hh_2_zb , hh_3_zb,h1_zb , h_2_zb , h3_zb, payload_zb,crc_zb
    hh_1_zb, hh_2_zb , hh_3_zb , h1_zb, h_2_zb , h3_zb  = ZigBee_node.calcHeaders_zb()
    header_msg_zb = ZigBee_node.calcHeaderMssg_zb(hh_1_zb , hh_2_zb , hh_3_zb)
    pay_hex_zb, sum_zb,payload_zb = ZigBee_node.calcPayload_zb()
    crc_zb = ZigBee_node.calcCRC_zb(h1_zb , h_2_zb , h3_zb,sum_zb)
    #message_zb= ZigBee_node.getMssg_zb( header_msg_zb , payload_zb, crc_zb)
    #await asyncio.sleep(1) #just for testing 
    print("-----------------------------------------------------------------------------------")
    counter_zb += 1
    Creat_unifided_Packet("zb")


start_time_wh = datetime.datetime.utcnow()
start_time = time.time()

for i in range(maxCounter):
    asyncio.run(WH())
    asyncio.run(ZigBee())

#print("in seconds wh",execTime_final_wh)
print("the total count of wh",counter_wh)
print("the total count of zb",counter_zb)
print("end of unification programm")

end = datetime.datetime.utcnow()
diff = end-start 
execTime = diff.total_seconds()
print("execTime in seconds",execTime)
