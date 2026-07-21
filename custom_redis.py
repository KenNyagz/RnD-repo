import socket  # noqa: F401
import threading
import time
#import secondary_functions
 
def main():
    print("Logs from the program will appear here!") # Print debugging logs.
    
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
                elif data == b"+ECHO hey\r\n":
                    conn.sendall(b"+hey\r\n")
 
                elif data[1:4] == b"SET":
                    data = data[1:].decode() #Convert bytes to str, omitting the 1st char which denotes imput type
                    data = data.split() #Separate by spaces; End up with a list
                    data2 = [str(element).casefold() for element in data] # Create a duplicate for comparing
                                                                          # case insensitive elements(hence the casefold
                    #Save key and val
                    key = data[data.index("SET") + 1]
                    val = data[data.index("SET") + 2]
                    if 'ex' in data2:
                        keyVal_map[key] = {"value": val, "EX": int(data2[data2.index("ex") + 1]), \
                                                                   "time_created": time.time()}
                        #print(keyVal_map)
                    elif 'px' in data2:
                        keyVal_map[key] = {"value": val, "PX": int(data2[data2.index("px") + 1]), \
                                                                   "time_created": time.time()}
                        #print(keyVal_map)
 
                    else:
                        keyVal_map[key] = val # For the values without TTL
                    conn.sendall(b'+OK\r\n')
 
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
 
                    else:
                        conn.sendall(str(str(keyVal_map.get(key, -1)) + "\r\n").encode()) # Retrieval of vals to keys without TTL
 
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
                        existing_lists[list_name] = [] #Create new list if not existing
                        for element in list_elems:
                            existing_lists[list_name].append(element)
 
                        return_val = ":" + str(len(existing_lists[list_name])) + "\r\n"
                        conn.sendall(return_val.encode())
                        continue
                    else:
                        for element in list_elems:
                            existing_lists[list_name].append(element)
 
                        return_val = ":" + str(len(existing_lists[list_name])) + "\r\n"
                        conn.sendall(return_val.encode())
                        continue
 
 
    server_socket = socket.create_server(("127.0.0.1", 6379), reuse_port=True)
 
    while True:
        conn, _ = server_socket.accept() # wait for client
 
        print(conn, _)
        thread = threading.Thread(target=handleConn, args=(conn,))
        thread.start()
 
if __name__ == "__main__":
    main()
