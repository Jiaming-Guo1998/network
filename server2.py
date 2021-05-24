from socket import *;
from time import ctime;
import threading;
import numpy as np
import pickle
from multiprocessing import Semaphore,Process

class _Client(threading.Thread):
    def __init__(self,Addr,BufSize,X,Y,G,B,w,interation,alpha,sem):
        threading.Thread.__init__(self)
        self.tcpCliSock=socket(AF_INET,SOCK_STREAM)
        self.tcpCliSock.connect(Addr)
        self.BufSize=BufSize
        self.X = X
        self.Y = Y
        self.G = G
        self.B = B
        self.w = w
        self.interation = interation
        self.alpha = alpha
        self.sem = sem
    def run(self):
        for j in range(self.interation):
            i = 0
            while True:
                
                E_0 = np.dot(self.G[0,1],self.X[i:self.B])
                E_1 = np.dot(self.G[1,1],self.X[i:self.B])
                F_0 = np.dot(self.G[0,1],self.w)
                F_1 = np.dot(self.G[1,1],self.w)

                rec_E = self.tcpCliSock.recv(self.BufSize)
                self.sem.release()       
                rec_F = self.tcpCliSock.recv(self.BufSize)
                self.tcpCliSock.send(pickle.dumps(E_0))
                self.sem.acquire()
                self.tcpCliSock.send(pickle.dumps(F_0))
                

                #print("2:",j)
                
                # rec_E = self.tcpCliSock.recv(self.BufSize)
                       
                # rec_F = self.tcpCliSock.recv(self.BufSize)
                
                #print("2:",j)
                E = pickle.loads(rec_E)
                F = pickle.loads(rec_F)
                
                N = E_0 + E
                N_ = F_0 + F
                Y_ = np.dot(N_,N.T)
                D = Y_ - self.Y[i:self.B]
                #print("2:",j)
                E_0 = np.dot(self.G[0,1],self.X[i:self.B].T)
                E_1 = np.dot(self.G[1,1],self.X[i:self.B].T)
                F_0 = np.dot(self.G[0,0],D[i:self.B])
                F_1 = np.dot(self.G[1,1],D[i:self.B])
               
                rec_E = self.tcpCliSock.recv(self.BufSize)
                self.sem.release()          
                rec_F = self.tcpCliSock.recv(self.BufSize)

                
                self.tcpCliSock.send(pickle.dumps(E_1))
                self.sem.acquire()
                
                self.tcpCliSock.send(pickle.dumps(F_1))
                
                # rec_E = self.tcpCliSock.recv(self.BufSize)
                          
                # rec_F = self.tcpCliSock.recv(self.BufSize)
              
                E = pickle.loads(rec_E)

                F = pickle.loads(rec_F)
                
                P = E_0 + E
                P_ = F_0 + F
                theta = np.dot(P_,P.T)
                self.w = self.w - np.dot((self.alpha/self.B),theta)
                i = i + self.B
                if(self.B > self.Y.shape[0] - i ):
                    break
        self.tcpCliSock.close()

