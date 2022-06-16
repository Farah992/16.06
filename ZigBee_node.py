import random
import time
import datetime
#ZigBee
start = datetime.datetime.utcnow()

def calcHeaders_zb():

    # управление кадром (2 байт)
    hh_1 = bytearray([1,2])
    split = [hh_1[i] for i in range (0,len(hh_1))]
    h1 = 0 
    for j in range (0,len(split)):
        h1 = h1 + split[j]
    h_1 = hex(h1)

    h_2 = 0x03  #Порядковый номер 1 байт
    hh_2 = h_2.to_bytes(1, 'little')

    # h_3 Поле адреса 20 байт
    hh_3 = bytearray([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]) 
    split = [hh_3[i] for i in range (0,len(hh_3))]
    h3 = 0 
    for j in range (0,len(split)):
        h3 = h3 + split[j]
    #print (h3)  # integer
    h_3 = hex(h3)
    return hh_1 , hh_2 , hh_3 , h1 , h_2, h3

def calcHeaderMssg_zb(hh_1 , hh_2 , hh_3): 

    header_msg = hh_1 + hh_2 + hh_3 # as a byte
    #print("header_msg of zb is",header_msg)
    print("header_msg of zb is","".join("\\x%02x" % i for i in header_msg))
    #print("length of headers",len(header_msg)) #23
    return header_msg

def calcPayload_zb():

    #payload (до 128 байт)
    #pay = random.randint(0,128) 
    pay = 50
    print("random number of payload is",pay)
    payload_zb = bytearray()
    for i in range(pay):
        payload_zb.append(i)
    #print("payload_zb is",payload_zb)
    #print("".join("\\x%02x" % i for i in payload_zb))
    print("payload_zb is","".join("\\x%02x" % i for i in payload_zb))

    sum = 0
    for k in payload_zb:
        sum = sum + payload_zb[k]
    pay_hex = hex(sum)
    return pay_hex, sum,payload_zb

def calcCRC_zb(h1 , h_2 , h3  , sum):
    # calculation checksum
    headers = h1 + h_2 + h3 # sum of integer headers
    headers_hex = hex(headers)  
    sum_all = sum + headers # int sum of headers + payload

    data = hex(sum_all)
    info = data[-2:] # keeping the lowest 6 bits
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  Заголовок (контрольная сумма)	
    crc = res_2.to_bytes(2, 'little') # as a  byte
    return crc,res_2, sum_all 


start_time = time.time()

def getMssg_zb(header_msg , payload_zb , crc):
    seconds = 3
    count = 0
    message = header_msg + payload_zb + crc # as a byte message
    #print("message of zb is",message)
    #print("message of zb is","".join("\\x%02x" % i for i in message))
    print("message of zb is",bytes("".join("\\x%02x" % i for i in message), 'utf-8'))
    message_zb = "".join("\\x%02x" % i for i in message)
    length = len(message)
    print("length of message_wh",length)
    #
    while True:
        print("-------")
        current_time = time.time()
        print(message_zb)
        count +=1
        time.sleep(0.5) # 11 packets
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:

            print("Finished iterating in: " + str(int(elapsed_time))  + " seconds")
            print("couunt",count)

            break
    #
    return message_zb


end = datetime.datetime.utcnow()
diff = end-start
execTime = diff.total_seconds()
print("execTime",execTime)
