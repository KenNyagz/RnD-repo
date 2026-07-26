import unittest
import socket
import threading
import time
from main import main

class test_custom_Redis(unittest.TestCase):

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setUp(self):
        server_socket = threading.Thread(target=main, daemon=True) #create thread for server socket
        server_socket.start() #start server socket thread
        time.sleep(0.1) # wait for server to start listening

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #client socket
        self.socket.connect(('127.0.0.1', 6379)) # Client socket connects to server's via main thread

    def tearDown(self):
        self.socket.close()

    def testPing(self):
        self.socket.sendall(b"+PING\r\n")
        data = self.socket.recv(1024)
        self.assertEqual(data, b"+PONG\r\n")

    def testHey(self):
        self.socket.sendall(b"+ECHO hey\r\n")
        data = self.socket.recv(1024)
        self.assertEqual(data, b"+hey\r\n")

    def testSETandGET(self):
        self.socket.sendall(b"+SET\r\n")
        data = self.socket.recv(1024)
        self.assertEqual(data, b"-1\r\n")





if __name__ == "__main__":
    unittest.main()
