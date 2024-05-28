import numpy as np
import matplotlib.pyplot as plt

x = np.arange(10)
y_bot = np.linspace(30, 50, 10)
y_dif = np.linspace(10, 5, 10)

plt.bar(x, y_dif, bottom=y_bot)
plt.show()
