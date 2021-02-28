# COMAN ROBERT - 323CB

def go_right(s10, s20):
	# intoarce partea din cuvant din stanga
	# cursorului, respectiv din dreapta
	# dupa ce cursorul se deplaseaza la dreapta
	s11 = s10 + s20[0]
	s21 = s20[1:len(s20)]
	if len(s21) == 0:
		s21 = "#"
	return [s11, s21]

def go_left(s10, s20):
	# cursorul se deplaseaza la stanga
	s21 = s10[len(s10) - 1] + s20
	if s10 != "#":
		s11 = s10[:-1]
	else:
		s11 = s10
	if len(s11) == 0:
		s11 = "#"
	return [s11, s21]

def check_word(string):
	# verifica daca cuvantul respecta alfabetul
	for char in string:
		if (not(char.isalpha() or char == "#")):
			return False
	return True

def create_configuration(word):
	# creeaza configuratia initiala
	# ("#", 0, word)
	if not check_word(word):
		return False
	config = {}
	config["u"] = "#"
	config["q"] = 0
	config["v"] = word
	if word[len(word) - 1] != "#":
		config["v"] = config["v"] + "#"
	return config

def accept(TM, word):
	config = create_configuration(word)
	if not config:
		return False
	while True:
		config = step(config, TM)
		# check final state
		if config == False:
			return False
		else:
			if config["q"] in TM["final_states"]:
				return True

def k_accept(TM, word, k):
	config = create_configuration(word)
	if not config:
		return False
	current_step = 0
	while current_step < k:
		config = step(config, TM)
		current_step += 1
		# check final state
		if config == False:
			return False
		else:
			if config["q"] in TM["final_states"]:
				return True
	return False

def read_configurations():
	line = input()
	line = line.split()
	configurations = []
	for i in range(0, len(line)):
		line[i] = line[i][1:len(line[i]) - 1]
		line[i] = line[i].split(",")
		d = {	"u" : line[i][0],
				"q" : int(line[i][1]),
				"v" : line[i][2]
			}
		configurations.append(d)
	return configurations

def print_config(config):
	print("(" + config["u"] + "," + str(config["q"]) + "," + config["v"]
		 + ")", end = " ")

def task1():
	config = read_configurations()
	TM = readTM()
	for c in config:
		c = step(c, TM)
		if c == False:
			print(c, end = " ")
		else:
			print_config(c)
	print()

def get_words():
	list = input()
	list = list.split()
	return list

def get_wordlist_ksteps():
	list = input()
	list = list.split()
	word_list = []
	ksteps = []
	for string in list:
		string = string.split(",")
		word_list.append(string[0])
		ksteps.append(int(string[1]))
	return [word_list, ksteps]

def task2():
	word_list = get_words()
	TM = readTM()
	for word in word_list:
		print(accept(TM, word), end = " ")
	print()

def task3():
	word_list, steps = get_wordlist_ksteps()
	TM = readTM()
	for i in range(0, len(word_list)):
		print(k_accept(TM, word_list[i], steps[i]), end = " ")
	print()

def readTM():
	# linia 1
	nr = int(input())
	TM = {}
	TM["no_states"] = nr
	# linia 2
	line = input()
	if(line.split()[0] == "-"):
		TM["final_states"] = []
	else:
		state_list = [int(x) for x in line.split()]
		TM["final_states"] = state_list
	# urmatoarele linii
	TM["transition"] = []
	while True:
		try:
			line = input()
			line = line.split()
			if not line:
				break
			transition = {}
			transition["current_state"] = int(line[0])
			transition["current_symbol"] = line[1]
			transition["next_state"] = int(line[2])
			transition["new_symbol"] = line[3]
			transition["position"] = line[4]
			TM["transition"].append(transition)
		except EOFError as error:
		 	break
	return TM

def step(config, TM):
	for transition in TM["transition"]:
		if (transition["current_state"] == config["q"] and 
			transition["current_symbol"] == config["v"][0]):
			pos = transition["position"]
			config["v"] = transition["new_symbol"] + config["v"][1:]
			config["q"] = transition["next_state"]
			if pos == "L":
				config["u"], config["v"] = go_left(config["u"], config["v"])
			if pos == "R":
				config["u"], config["v"] = go_right(config["u"], config["v"])
			return config
	return False

execute_task = {"step" : task1, "accept" : task2, "k_accept" : task3}
input_type = input()
execute_task[input_type]()
