import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from pyshgp.gp.base import PushGPRegressor

X_train = np.round(np.arange(-2.0, 2.0, 0.1).reshape(-1, 1), 1)

def target_func(a): return (a ** 6) + (2 * a**4) + (a**2)

Y_train = []
for r in X_train:
    Y_train.append(target_func(*r))
Y_train = np.array(Y_train).reshape(-1, 1)

# print(X_train)
# print(Y_train)
# print

symbReg = PushGPRegressor(max_generations=100, n_jobs=-1,
                          verbose=1)
symbReg.fit(X_train, Y_train)

print(symbReg.best_error_)
print(symbReg.best_)

preds = symbReg.predict(X_train)

#
# Plotting
#

fig = plt.figure(1, figsize=(8, 6))

plt.scatter(X_train, Y_train,  color='black')
plt.plot(X_train, preds, color='blue', linewidth=3)

plt.xlabel('X')
plt.ylabel('Y')

plt.show()
