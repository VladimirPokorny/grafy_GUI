from scipy.fft import fft, fftfreq
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

table = pd.read_csv('grafy/scope_0.csv')

rozsah1 = 3
rozsah2 = len(pd.read_csv('grafy/scope_0.csv').loc[:, 'x-axis'])

t = table.iloc[rozsah1:rozsah2, 0]
t = t.astype(np.float64)

u1 = table.iloc[rozsah1:rozsah2, 1]
u1 = u1.astype(np.float64)

from scipy.fft import fft, fftfreq
# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft(y)
xf = fftfreq(N, T)[:N//2]
import matplotlib.pyplot as plt
# plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
# plt.grid()
# plt.show()


x = u1.to_numpy()

yf = fft(x)

x = list(range(1,len(yf)+1))

plt.figure(figsize=(10, 10))
plt.plot(x[15], np.abs(yf[15]), linewidth=2)
plt.grid()

plt.show()

print(len(yf))
# print(yf)
