from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt

an = np.linspace(0, 2 * np.pi, 100)

x_val = np.empty(1440)
y_val = np.empty(1440)
et = np.empty(1440)

plt.plot(np.cos(an), np.sin(an))
for i in range(14, 1440, 15):
    x_val[i] = np.cos(i * (2. * np.pi / 1440))
    y_val[i] = np.sin(i * (2. * np.pi / 1440))
    et[i] = i

for i, mins in enumerate(et):
    if i % 60 == 59:
        plt.annotate(str(int(mins // 60)) + ':' + str(int(mins % 60)), (x_val[i], y_val[i]))

# plt.subplot(111)
plt.plot(np.cos(an), np.sin(an))
plt.axis('equal')
plt.axis([-1.5, 1.5, -1.5, 1.5])
plt.scatter(x_val[14::15], y_val[14::15])

plt.savefig('reprezentacja_czasu.png')

plt.show()
