import sys
from pathlib import Path
from markov import Markov, identify_speaker
import pandas as pd
import numpy as np
from itertools import product
import time
import seaborn as sns
import matplotlib.pyplot as plt


def open_file(filepath):
	"""
	open_file(filename)
	Takes in a filepath (in my code, a pathlib Path) and reads the contents
	from the specified file and returns them as a string

	Gets: filename, a Path
	Returns: contents, a string
	"""
	contents = []
	with open(filepath, "r") as file:
		contents = file.read()
	return contents


def plot_performance(df, run):
	"""
	plot_performance(df, run)
	Takes in a dataframe and the number of runs and plots the performance plot using groupby
	on the original dataframe.

	Gets: 
		df, a Pandas dataframe
		run, an int
	Returns: nothing
	"""
	ax = sns.pointplot(x='K', y='Time', hue='Implementation', linestyle='-', marker='o', 
					   data=df.groupby(['Run #', 'K', 'Implementation']).mean().reset_index(inplace=False))
	plt.title('Hashtable vs. Python dict')
	plt.ylabel(f'Average Time (Runs={run})')
	plt.xlabel('K')
	plt.savefig('execution_graph.png')


def process_args(performance_check):
	"""
	process_args(performance_check)
	A helper function to make the amount of code outside functions
	smaller. Takes in a bool communicating whether it's a performance
	check or not, and based on that will process the command line arguments
	accordingly, passing back a list of file paths and the provided variables
	as ints.

	Gets: performance_check, a bool
	Returns:
		files, a list of Paths
		k, an int
		one of:
			state, an int
			run, an int
	"""
	if performance_check:
		files = [Path.cwd() / sys.argv[n] for n in range(2,5)]
		k = int(sys.argv[5])
		run = int(sys.argv[6])
		return files, k, run
	else:
		files = [Path.cwd() / sys.argv[n] for n in range(1, 4)]
		k = int(sys.argv[4])
		state = int(sys.argv[5])
		return files, k, state


if __name__ == "__main__":
	if sys.argv[1] in ['--p', 'p', '-p']:
		"""
		Performance check:
		Process the arguments, create a dataframe by taking the Cartesian product
		of the parameters, run the algorithm according to the parameters and record
		the time taken, then plot those results. 
		"""
		files, k, run = process_args(True)
		texts = [open_file(file) for file in files]
		ks = list(range(1,k+1))
		runs = list(range(1,run+1))
		implementations = ['Hashtable', 'dict']
		parameters = (product(ks, runs, implementations))
		df = pd.DataFrame(parameters, columns = ['K', 'Run #', 'Implementation'])
		imp_dict = {'Hashtable': 0, 'dict': 1}
		df['Time'] = [np.nan]*len(df.index)

		for index_val in df.index.tolist():
			row = df.iloc[index_val]
			start = time.perf_counter()
			tup = identify_speaker(texts[0], texts[1], 
								   texts[2], row['K'], 
								   imp_dict[row['Implementation']])
			end = time.perf_counter()
			elapsed_time = float(f'{end - start:0.4f}')
			df.loc[index_val, 'Time'] = elapsed_time

		plot_performance(df, run)

	else:
		"""
		Single run evaluation:
		Process the arguments, identify the speaker, and print the results
		"""
		files, k, state = process_args(False)
		texts = [open_file(file) for file in files]
		results = identify_speaker(texts[0], texts[1], texts[2], k, state)
		print(f'Speaker A: {results[0]}')
		print(f'Speaker B: {results[1]}\n')		
		print(f'Conclusion: Speaker {results[2]} is most likely')