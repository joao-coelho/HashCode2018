from random import randint

def get_coords(pizza, R, C):
	while(True):
		row = randint(0, R - 1)
		col = randint(0, C - 1)
		if pizza[row][col] == 0:
			continue
		else: 
			break
	return row, col

def get_candidate_slice(slices, number_cells, tomato, mush, start_point, next_point, pizza):
	r, c = start_point
	if number_cells == H & tomato > L & mush > L: 
		return slices
	if pizza[r+1][c] != 0:
		sl = r+1, c
		slices.append(sl)
		if pizza[r+1][c] == 'T':
			tomato += 1
		else:
			mush += 1
		get_candidate_slice(slices, number_cells + 1, tomato, mush,
		start_point, sl, pizza)




file = open("example.in", "r")
lines = file.readlines()

pizza = list()
for line in lines:
	pizza.append(line.rstrip())

firstLine = pizza[0].split(" ")

R = firstLine[0]
C = firstLine[1]
L = firstLine[2]
H = firstLine[3]




