import numpy as np
import pickle

A = np.array([[1,2],[3,4],[5,6]])
#print(type(A.flatten()))
#B = A.flatten()
msg = str(A)
np.array(np.mat(msg))
print(pickle.dumps(A))
B = pickle.dumps(A)
print(pickle.loads(B))
C = pickle.loads(B)
print(type(C))

#print(np.array(msg).reshape(3,2))

#print(A)
#msg = str(A)

#msg = msg.encode("utf-8")
#msg_ = msg.decode("utf-8")
# print(msg_)
# print(list(msg_))
#print(type(msg.decode("utf-8")))

#B = np.array(msg_)
#C = B.tolist()
# print(C)
#for i in C:
 #   print(i)
# print(np.array(C).shape)

#print(msg_)
#B=np.fromstring(msg_,dtype = float,sep='')
#print(B)
#print(B.shape)