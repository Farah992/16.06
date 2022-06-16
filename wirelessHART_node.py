import random
import time
import datetime
#WH
start = datetime.datetime.utcnow()
def calcHeaders_wh():

    h_1 = 0x01  # Управление кадром 1 байт as integer
    hh_1 = h_1.to_bytes(1, 'little') # as a 1 byte

    h_2 = 0x03  #Порядковый номер 1 байт
    hh_2 = h_2.to_bytes(1, 'little')

    # h_3 Поле адреса 16 байт
    hh_3 = bytearray([5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]) 
    split = [hh_3[i] for i in range (0,len(hh_3))]
    h3 = 0 
    for j in range (0,len(split)):
        h3 = h3 + split[j]
    h_3 = hex(h3)

    # h_4 идентификатор сети (2 байт)
    hh_4 = bytearray([25,26])
    split = [hh_4[i] for i in range (0,len(hh_4))]
    h4 = 0 
    for j in range (0,len(split)):
        h4 = h4 + split[j]
    h_4 = hex(h4)

    h_5 = 0x27 #Спецификатор адреса  int (27)
    hh_5 = h_5.to_bytes(1, 'little')
   

    h_6 = 0x28 #Тип DLPDU
    hh_6 = h_6.to_bytes(1, 'little') # msb lsb = little

    #h_7 Код целостности сообщения (MIC) Message integrity code
    hh_7 = bytearray([29,30,31,32]) 
    split = [hh_7[i] for i in range (0,len(hh_7))]
    h7 = 0 
    for j in range (0,len(split)):
        h7 = h7 + split[j]
    h_7 = hex(h7) 
    return hh_1,hh_2,hh_3,hh_4,hh_5,hh_6,hh_7,h_1, h_2,h3,h4,h_5,h_6,h7

def calcHeaderMssg_wh(hh_1 , hh_2 , hh_3 , hh_4 , hh_5 , hh_6 ,hh_7 ):
    header_msg = hh_1 + hh_2 + hh_3 + hh_4 + hh_5 + hh_6 +hh_7 # as a byte
    #print("header_msg of wh is",header_msg)
    print("header_msg of wh is","".join("\\x%02x" % i for i in header_msg))
    #print("length of headers",len(header_msg)) #26
    return header_msg

def calcPayload_wh():
    #payload (до 128 байт)
    #pay = random.randint(0,128)
    pay = 60
    print("random number of payload is",pay)
    payload_wh = bytearray()
    for i in range(pay):
        payload_wh.append(i)
    #print("payload_wh is",payload_wh)
    #print("".join("\\x%02x" % i for i in payload_wh))
    print("payload_wh is","".join("\\x%02x" % i for i in payload_wh))

    sum = 0
    for k in payload_wh:
        sum = sum + payload_wh[k]
    pay_hex = hex(sum)
    return pay_hex,sum,payload_wh

# calculation checksum
def calcCRC_wh(h_1 , h_2 , h3 , h4 , h_5 , h_6 ,h7, sum):
    headers = h_1 + h_2 + h3 + h4 + h_5 + h_6 + h7 # sum of integer headers
    headers_hex = hex(headers)  
    sum_all = sum + headers # int sum o headers + payload

    data = hex(sum_all) 
    info = data[-2:] # keeping the lowest 6 bits
    res_1 = int(info,16)
    res_2 = 255 - res_1
    h_8 = hex(res_2) #h_8  Заголовок (контрольная сумма)	
    crc = res_2.to_bytes(2, 'little') # as a  byte
    return crc,res_2,sum_all


start_time = time.time()

def getMssg_wh( header_msg , payload_wh , crc):
    seconds = 3
    count = 0
    message = header_msg + payload_wh + crc # as a byte message
    #print("message of wh is",message)
    print("message of wh is",bytes("".join("\\x%02x" % i for i in message), 'utf-8'))
    message_wh = "".join("\\x%02x" % i for i in message)
    length = len(message)
    print("length of message_wh",length)
    #
    while True:
        print("-------")
        current_time = time.time()
        print(message_wh)
        count +=1
        time.sleep(0.5) #
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:

            print("Finished iterating in: " + str(elapsed_time)  + " seconds")
            print("count",count)

            break

    return message_wh
    #
    #return message_wh


end = datetime.datetime.utcnow()
diff = end-start
execTime = diff.total_seconds()
print("execTime",execTime)
