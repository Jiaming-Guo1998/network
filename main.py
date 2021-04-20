import read_mnist as rd
import numpy as np
train_images = rd.load_train_images()
train_labels = rd.load_train_labels()
# test_images = load_test_images()
# test_labels = load_test_labels()
train_images = train_images.reshape(60000,784)
X = train_images
Y = train_labels
w = np.zeros(785)
b = np.ones(train_images.shape[0])
X = np.insert(X, 0, values=b, axis=1)
#w[0] = 1; 
#print(w.shape)
i = 0 
interations = 500
alpha = 2e-7
B = 128
for j in range(interations):
	while True:
		w = w - np.dot((alpha / B ),(np.dot(X[i:B].T,(np.dot(X[i:B],w) - Y[i:B]))))
		i = i + B
		if (B > Y.shape[0] - i ):
			w = w - np.dot((alpha / Y.shape[0] - i ),(np.dot(X[i:Y.shape[0] - i].T,(np.dot(X[i:Y.shape[0] - i],w) - Y[i:Y.shape[0] - i]))))
			break
	i = 0
	#alpha = alpha / 2.0


print(np.dot(X[4],w))
print(Y[4])



