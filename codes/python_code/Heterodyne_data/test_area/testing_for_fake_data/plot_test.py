import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

a  = np.arange(5)
b = np.arange(5)

x = np.array([[1,0.1,0.9,0.2],[0.8,0.3,0.4,0.5],[0,1,0,1],[0,1,1,1]])

plt.clf()
plt.pcolor(a,b,x, cmap='gray')
#plt.cmap = plt.cm(gray)
plt.show()

