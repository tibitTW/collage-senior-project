from time import sleep
import matplotlib.pyplot as plt
from statistics import mean

f = open('0217_output.txt')
data = list(map(int, f.read().split('\n')))

filtered5 = [mean(data[n-4:n+1]) for n in range(4, len(data))]
filtered7 = [mean(data[n-6:n+1]) for n in range(6, len(data))]
filtered11 = [mean(data[n-10:n+1]) for n in range(10, len(data))]
filter_filtered11 = [mean(filtered11[n-2:n+3]) for n in range(4, len(filtered11))]

plt.plot(data, 'g', label = 'data')
plt.plot(filtered5, 'r', label = 'filtered5')
plt.plot(filtered7, 'b', label = 'filtered7')
plt.plot(filtered11, 'yellow', label = 'filtered11')
plt.plot(filter_filtered11, 'purple', label = 'filter_filtered11')

plt.legend(loc = 'lower right')
plt.show()