'''
MPCS 51042 S'20: Markov models and hash tables

M. Merritt Smith
'''
from hash_table import Hashtable
from math import log
import numpy as np
from datetime import datetime


HASH_CELLS = 57

# Recommended load factor and growth factor for the assignment
# TOO_FULL = 0.5
# GROWTH_RATIO = 2

class Markov:
	"""
	class Markov
	A class that represents a Markov model for speech. Takes in a speech sample
	and can give a log probability for whether a passed in text is from the same
	speaker as the original speaker. 
	"""
	def __init__(self, k, speech, state):
		"""
		__init__(self, k, speech, state)
		The initialization method for the Markov class. Takes in k, 
		the length of the substrings, speech, a text sample, and 
		a state to communicate whether to use a Hashtable or a dict.
		Creates the table using the _gen_table function.

		Gets: 
			self, a Markov instance
			k, an int
			speech, a string
			state, an int, 0 or 1
		Returns: nothing explicitly, but implicitly self
		"""
		if state == 0:
			self.table = Hashtable(HASH_CELLS, 0, 0.5, 2)
		elif state == 1:
			self.table = {}
		else:
			raise Exception
		self.k = k
		self.alphabet_len = len(set(speech))
		self._gen_table(speech)


	def _gen_table(self, text):
		"""
		_gen_table(self, text)
		A method of the Markov class. Takes in text, and turns it into a table or dict where the keys are
		the k and k+1 strings and the values are the frequencies with which those strings appear. Does 
		so by taking all strings of length k and k+1 that don't need to be wrapped, then looking 
		at the edge case where the k length one doesn't need to be wrapped but k+1 does, then
		looking at the rest of the wrapped cases. THen calls np.unique and adds all these
		to the table or dict.

		Gets: 
			self, a Markov instance
			text, a string
		Returns: nothing
		"""
		text_len = len(text)
		k_k1_len_substrings = [(text[i-1:i+self.k-1], text[i-1:i+self.k]) for i in range(text_len) if i+self.k-1 < text_len][1:]
		k_k1_len_substrings.append((text[-self.k:], text[-self.k:]+text[0]))
		if self.k > 1:
			for char_index, char in enumerate(text[-self.k+1:]):
				k_k1_len_substrings.append((text[-self.k +1 + char_index:]+text[:char_index+1], text[-self.k +1 + char_index:]+text[:char_index+2]))
		all_substrings = np.unique([substr for tup in k_k1_len_substrings for substr in tup], return_counts = True)
		for substring, count in zip(all_substrings[0], all_substrings[1]):
			self.table[substring] = count


	def log_probability(self, text):
		"""
		log_probability(self, text)
		Takes in a text sample and returns the log probability that it came from the same source as the original text
		the model was built on. Does so by creating a set of k and k+1 length strings and calculating the total log
		probability of the text using Laplacian smoothing. 

		Gets:
			self, a Markov instance
			text, a string (not the same string as _gen_table)
		"""
		def _access_values(key):
			"""
			_access_values(key)
			A helper closure to allow for a try except inside a list comp for
			the total log prob calculation. If the table is a dict, then it 
			will throw keyerrors if the key isn't found which for our purposes
			is a 0. 

			Gets: key, a string of length k or k+1
			Returns: an int
			"""
			try:
				return self.table[key]
			except KeyError:
				return 0
		k_k1_len_substrings = [(text[i-1:i+self.k-1], text[i-1:i+self.k]) for i in range(len(text)) if i+self.k-1 < len(text)][1:]
		k_k1_len_substrings.append((text[-self.k:], text[-self.k:]+text[0]))
		if self.k > 1:
			for char_index, char in enumerate(text[-self.k+1:]):
				k_k1_len_substrings.append((text[-self.k +1 + char_index:]+text[:char_index+1], text[-self.k +1 + char_index:]+text[:char_index+2]))
		total_log_prob  = sum([log((_access_values(str_tuple[1])+1) / (_access_values(str_tuple[0])+self.alphabet_len)) for str_tuple in k_k1_len_substrings])
		return total_log_prob



def identify_speaker(speaker_a, speaker_b, unknown_speech, order, state):
	"""
	identify_speaker(speaker_a, speaker_b, unknown_speech, order, state)
	Takes in two speech examples and a speech sample of unknown origin,
	as well as a variable saying which data structure to use and what k is.
	Creates Markov models for speaker_a and speaker_b, then comparies 
	the log probabilities for the unknown speech based on the model for 
	each speaker, and returns a tuple with these log probabilities and the
	name of the one with the higher probability (since log is linear).

	Gets:
		speaker_a, a string
		speaker_b, a string
		unknown_speech, a string
		order, an int, either 0 or 1
		state, an int
	Returns: a tuple of two floats and a string in that order
	"""
	speaker_a_model = Markov(order, speaker_a, state)
	speaker_b_model = Markov(order, speaker_b, state)
	speaker_a_norm_log_likelihood = speaker_a_model.log_probability(unknown_speech) / len(unknown_speech)
	speaker_b_norm_log_likelihood = speaker_b_model.log_probability(unknown_speech) / len(unknown_speech)
	if speaker_a_norm_log_likelihood > speaker_b_norm_log_likelihood:
		return (speaker_a_norm_log_likelihood, speaker_b_norm_log_likelihood, "A")
	else:
		return (speaker_a_norm_log_likelihood, speaker_b_norm_log_likelihood, "B")
