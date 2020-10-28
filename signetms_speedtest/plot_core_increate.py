import matplotlib.pyplot as plt

number_of_cores = [
	1,
	2,
	4,
	8,
	16,
	32,
	40,
	64,
]

average_time = [
	60.294,
	33.087,
	30.651,
	29.344,
	26.980,
	27.766,
	27.888,
	28.122,
]

plt.plot(number_of_cores, average_time, 'bo')
plt.ylabel('Average time to perform sampling')
plt.xlabel('Number of workers')
plt.xticks(number_of_cores)
plt.savefig('workers_experiment.pdf', transparent=True)
