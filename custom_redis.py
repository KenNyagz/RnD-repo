import socket  # noqa: F401
import threading
import time
#import secondary_functions
 
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
 
    # Uncomment the code below to pass the first stage
    #
    lock = threading.Lock()
    keyVal_map = {}
    existing_lists = {}
 
    def handleConn(conn):
 
        with lock: #Lock to prevent race conditions
            while True:
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
 
                if data == b"+PING\r\n":
                    conn.sendall(b"+PONG\r\n")
                    continue
                elif data == b"+ECHO hey\r\n":
                    conn.sendall(b"+hey\r\n")
                    continue
 
                elif data[1:4] == b"SET":
                    data = data[1:].decode() #Convert bytes to str, omitting the 1st char which denotes imput type
                    data = data.split() #Separate by spaces; End up with a list
                    data2 = [str(element).casefold() for element in data] # Create a duplicate for comparing
                                                                          # case insensitive elements(hence the casefold)
                    #Save key and val
                    key = data[data.index("SET") + 1]
                    val = data[data.index("SET") + 2]
                    if 'ex' in data2:
                        keyVal_map[key] = {"value": val, "EX": int(data2[data2.index("ex") + 1]), \
                                                                   "time_created": time.time()}
 
                    elif 'px' in data2:
                        keyVal_map[key] = {"value": val, "PX": int(data2[data2.index("px") + 1]), \
                                                                   "time_created": time.time()}
 
                    else:
                        keyVal_map[key] = val # For the values without TTL
                    conn.sendall(b'+OK\r\n')
                    continue
 
                elif data[1:4] == b"GET":
                    data = data[1:].decode() #Convert bytes to str, omitting the 1st char which denotes imput type
                    data = data.split() #Separate by spaces; End up with a list
 
                    if len(data) == 1: 
                        conn.sendall(b'-1\r\n')
                        continue
                    #Save key
                    key = data[data.index("GET") + 1]
 
                    if type(keyVal_map.get(key)) == dict:
                        if "time_created" in keyVal_map[key]: #if key had a TTL attr
                            if "EX" in keyVal_map[key]:
                                if time.time() <= keyVal_map[key]["time_created"] + keyVal_map[key]["EX"]:
                                    conn.sendall(str(keyVal_map[key]).encode())
                                    #conn.sendall(keyVal_map[key]["value"].encode())
                                else:
                                    del (keyVal_map[key])
                                    conn.sendall(b'+Key Expired\r\n')
                                continue
                            if "PX" in keyVal_map[key]:
                                #print(time.time() * 1000 - keyVal_map[key]["PX"], keyVal_map[key]["time_created"])
                                if time.time() * 1000 <= keyVal_map[key]["time_created"] * 1000 + keyVal_map[key]["PX"]:
                                    conn.sendall(str(keyVal_map[key]).encode())
                                    #conn.sendall(keyVal_map[key]["value"].encode())
                                else:
                                    del (keyVal_map[key])
                                    conn.sendall(b'+Key Expired\r\n')
                                continue
 
                        #elif keyVal_map.get(key, -1) != -1:  #Currently not handling keys with multiple non-TTL attributes
                        #    conn.sendall(keyVal_map[key]["value"].encode())
                        #    continue
 
                    else:
                        conn.sendall(str(str(keyVal_map.get(key, -1)) + "\r\n").encode()) # Retrieval of vals to keys without TTL
                        continue
 
                    #conn.sendall(b"$-1\r\n") #already being handled by the else just above
 
                elif data[1:6] == b"RPUSH":
                    data = data[6:] #select from 6th byte onwards only
                    data_str = data.decode()
                    elems = data_str.split()
 
                    if len(elems) < 1:
                        conn.sendall(b"-1\r\n")
                        #print(existing_lists) #for debugging
                        continue
 
                    list_name = elems[0]
                    list_elems = elems[1:]
                    if list_name not in existing_lists:
                        existing_lists[list_name] = [] #Create new list if not existent
                        for element in list_elems:
                            try:  # Check if input is an int or float, then add to list
                                if eval(element) != str:  # use eval to read str as code
                                    existing_lists[list_name].append(eval(element))
                                    continue
 
                            except Exception as e:
                                pass # if str, eval will raise a variable not defined error, ignore, move to next line
                            existing_lists[list_name].append(element)
 
                        return_val = ":" + str(len(existing_lists[list_name])) + "\r\n"
                        conn.sendall(return_val.encode())
                        continue
                    else:
                        for element in list_elems:
                            try:  # Check if input is an int or float, then add to list
                                if eval(element) != str:
                                    existing_lists[list_name].append(eval(element))
                                    continue
 
                            except Exception as e:
                                pass # if str, eval will raise a variable not defined error, move to next line
                            existing_lists[list_name].append(element)
 
                        return_val = ":" + str(len(existing_lists[list_name])) + "\r\n"
                        conn.sendall(return_val.encode())
                        continue
 
                elif data[1:7] == b"LRANGE":
                    data = data[7:] #select from 7th byte onwards, omit + and LRANGE
                    data_str = data.decode()
                    elems = data_str.split()
 
                    if len(elems) == 1:
                        list_key = elems[0]
                        if list_key not in existing_lists: #if list not existent return empty list
                            conn.sendall(b"[]\r\n")
                            continue
                        else: #if only list key, return entire list
                            lst = existing_lists[list_key]
                            rtn = str(lst) + "\r\n"
                            conn.sendall(rtn.encode())
                            continue
 
                    if len(elems) != 3:
                        conn.sendall(b"-1\r\n")
                        continue
 
                    list_key = elems[0]
                    if list_key not in existing_lists:
                        conn.sendall(b"[]\r\n")
                        continue
 
                    lst = existing_lists[list_key]
 
                    try:   # Convert str input to int, return -1 if non-int
                        start = int(elems[1])
                        stop = int(elems[2])
                    except Exception as e:
                        conn.sendall(b"-1\r\n")
                        continue
 
                    return_val = ""
                    count = 1
 
                    if stop == 0: # handling 0 as stop index; edge-case
                        conn.sendall(b"-1\r\n") # 0 can never be the stop
                        continue                # whether in +ve or -ve indexing
 
                    if start == 0: #handling 0 as start; edge case
                        counter = 1
                        if stop > 0:
                            if stop >= len(lst):
                                stop = len(lst)
 
                            for i in range(start, stop + 1): # build resp str
                                return_val += str(counter) + ') ' + str(lst[i]) + '\n'
                                counter += 1
                            conn.sendall(return_val.encode())
                            continue
                        if stop < 0:
                            stop = len(lst) + stop
                            for i in range(start, stop + 1): # build resp str
                                return_val += str(counter) + ') ' + str(lst[i]) + '\n'
                                counter += 1
 
                            conn.sendall(return_val.encode())
                            continue
 
                    #handling -ve indexing
                    if start <= 0 and stop < 0:
                        if stop <= start:
                            conn.sendall(b'-1\r\n')
                            continue
                        if start * -1 > len(lst): # if the -ve start index exceeds the 1st element,
                            start = 0 # assign the first element to be the starting index
                        else:
                            start = len(lst) + start #Deduct the index no from last index                        
 
                        stop = len(lst) + stop
                        counter = 1
                        for i in range(start, stop + 1): # build resp str
                            return_val += str(counter) + ') ' + str(lst[i]) + '\n'
                            counter += 1
 
                        conn.sendall(return_val.encode())
                        continue
 
                    # +ve indexing
                    if start >= len(lst) or start >= stop:
                        conn.sendall(b"[]\r\n")
                        continue
 
                    if stop >= len(lst):
                        stop = len(lst)
 
                    for i in range(start, stop): # build resp str
                        return_val += str(count) + ') ' + str(lst[i]) + '\n'
                        count += 1
                    #for element in lst:   # build the resp string
                    #    return_val += str(lst.index(element) + 1) + ') ' + str(element) + '\n'
 
                    conn.sendall(return_val.encode())
                    continue
 
                #elif data[1:6] == b"LPUSH":
 
 
    server_socket = socket.create_server(("127.0.0.1", 6379), reuse_port=True)
 
    while True:
        conn, _ = server_socket.accept() # wait for client
 
        print(conn, _)
        thread = threading.Thread(target=handleConn, args=(conn,))
        thread.start()
 
if __name__ == "__main__":
    main()
