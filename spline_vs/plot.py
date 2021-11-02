import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from scipy import interpolate


# def bspline(cv, n=100, degree=3):
#     """ Calculate n samples on a bspline

#         cv :      Array ov control vertices
#         n  :      Number of samples to return
#         degree:   Curve degree
#     """
#     cv = np.asarray(cv)
#     count = cv.shape[0]

#     # Prevent degree from exceeding count-1, otherwise splev will crash
#     degree = np.clip(degree,1,count-1)

#     # Calculate knot vector
#     kv = np.array([0]*degree + list(range(count-degree+1)) + [count-degree]*degree,dtype='int')

#     # Calculate query range
#     u = np.linspace(0,(count-degree),n)

#     # Calculate result
#     return np.array(np.splev(u, (kv,cv.T,degree))).T


# x = [0, 1, 2, 3, 4]  # np.arange(0, 2*np.pi+np.pi/4, 2*np.pi/8)

# y = [0, 1, 0, -1, 1]  # np.sin(x)

# cv = np.array([[ 50.,  25.],
#    [ 59.,  12.],
#    [ 50.,  10.],
#    [ 57.,   2.],
#    [ 40.,   4.],
#    [ 40.,   14.]])

# bspline(cv, degree=2)
# # s = interpolate.InterpolatedUnivariateSpline(x, y, k=2)
# t,c,k = interpolate.splrep(x, y, s=0 ,k=2)

# xnew = np.arange(0,5,.1)
# ynew=interpolate.splev(xnew,(t,c,k))
# plt.plot(xnew,ynew,x,y,'o')
# [tx,ty]=t.reshape(-1,2).T
# plt.plot(tx,ty,'gv')
# plt.show()

k = 3
t = np.arange(6)
t = [0, 1, 5, 10, 12, 22, 25, 31]
c = [-1, 1, 3, -10, 10]

spl = interpolate.BSpline(t, c, k)

# intervals =[np.arange(a,b+.1,.1) for a,b in zip(t[0:-1],t[1:])]

# for xx in intervals:
#     plt.plot(xx, spl(xx))

xx = np.arange(t[0], t[-1]+.1, .1)
# xx= np.linspace(0,len(c)//2-k,100)
plt.plot(xx, spl(xx))
plt.plot(xx, interpolate.splev(xx, (t, c, k)), 'g')
plt.plot(t, spl(t), 'or')
plt.axis('off')

plt.savefig('instance/spline.jpg', bbox_inches='tight')
plt.show()
plt.show()
