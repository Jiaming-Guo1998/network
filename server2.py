from socket import *;
from time import ctime;
import threading;
import numpy as np
import pickle

class _Client(threading.Thread):
    def __init__(self,Addr,BufSize,X,Y,G,B,w,interation,alpha):
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

    def run(self):
        for j in range(self.interation):
            i = 0
            while True:
            
                E_0 = np.dot(self.G[0,1],self.X[i:self.B])
                E_1 = np.dot(self.G[1,1],self.X[i:self.B])
                F_0 = np.dot(self.G[0,1],self.w)
                F_1 = np.dot(self.G[1,1],self.w)

                self.tcpCliSock.send(pickle.dumps(E_0))
                self.tcpCliSock.send(pickle.dumps(F_0))

                rec_E = self.tcpCliSock.recv(self.BufSize)           #客户端发来的消息存入data中
                rec_F = self.tcpCliSock.recv(self.BufSize)
                E = pickle.loads(rec_E)
                F = pickle.loads(rec_F)
                
                N = E_0 + E
                N_ = F_0 + F
                Y_ = np.dot(N_,N.T)
                D = Y_ - self.Y[i:self.B]
                E_0 = np.dot(self.G[0,1],self.X[i:self.B].T)
                E_1 = np.dot(self.G[1,1],self.X[i:self.B].T)
                F_0 = np.dot(self.G[0,0],Y_[i:self.B])
                F_1 = np.dot(self.G[1,1],Y_[i:self.B])

                self.tcpCliSock.send(pickle.dumps(E_0))
                self.tcpCliSock.send(pickle.dumps(F_0))
                rec_E = self.tcpCliSock.recv(self.BufSize)           #客户端发来的消息存入data中
                rec_F = self.tcpCliSock.recv(self.BufSize)
                E = pickle.loads(rec_E)

                F = pickle.loads(rec_F)
                
                P = E_0 + E
                P_ = F_0 + F
                theta = np.dot(P_,P.T)
                w = w - np.dot((self.alpha/self.B),self.theta)
                i = i + self.B
                if(self.B > self.Y.shape[0] - i ):
                    break
        self.tcpCliSock.close()

