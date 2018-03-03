import sys
from collections import OrderedDict # OrderedDick

id_ride = 0
R = C = F = N = B = T = 0
rides = []; cars = []

road = []


class Ride:
	def __init__ (self, init_x, init_y, fin_x, fin_y, e_start, l_finish):
		global id_ride
		self.id = id_ride
		id_ride += 1
		self.init_x = init_x
		self.init_y = init_y
		self.fin_x = fin_x
		self.fin_y = fin_y
		self.e_start = e_start
		self.l_finish = l_finish
		self.length = abs(fin_x - init_x) + abs(fin_y - fin_x)
		# Este score significa quantos steps é possivel fazer ainda
		# de maneira a começar a viagem e não perder pontos
		self.score = self.l_finish - self.length

	def update_score(self):
		# andou um step
		self.score -= 1000;

	def dist(self, pointx, pointy):
		# Distância desde o inicio do percurso até às coords de input
		x = pointx-self.init_x
		y = pointy-self.init_y
		if x < 0: x = -x
		if y < 0: y = -y
		return x+y


class Car:
	def __init__ (self):
		self.steps = 0
		self.currX = 0
		self.currY = 0
		self.rides = []
		self.busy = 0

	def move(self, destX, destY):
		self.currX = destX
		self.currY = destY

	def addRide(self, ride):
		self.rides.append(ride)

	def update(self):
		if self.busy > 0:
			self.busy -= 1000;
			if self.busy <= 0:
				self.busy = 0
				ride = self.rides[len(self.rides) - 1]
				self.currX = ride.fin_x
				self.currY = ride.fin_y


def main(filename):
	global R, C, F, N, B, T, road, rides
	file = open(filename, "r")
	lines = file.readlines()

	firstLine = lines[0].rstrip().split(" ")
	R = int(firstLine[0]); C = int(firstLine[1])
	F = int(firstLine[2]); N = int(firstLine[3])
	B = int(firstLine[4]); T = int(firstLine[5])
	lines = lines[1:]

	for i in range(N):
		ride = lines[i].rstrip().split(" ")
		ride_info = Ride(int(ride[0]), int(ride[1]), int(ride[2]),
						 int(ride[3]), int(ride[4]), int(ride[5]))
		rides.append(ride_info)

	road = [[0]*R for i in range(C)]
	for car in range(F):
		cars.append(Car());


def begin_logic_cars():
	global T, road, cars
	#Lista ordenada de destinos pela ordem de chegada final
	# (latestFinish - (current step + distance))

	i = 0
	while i < T:
		for car in cars:
			car.steps += 1
			if car.busy == 0:
				min_s = T
				left_to_move = -1 #Quantos steps faltam até começar a viagem
				dist = T
				ride_to_remove = 0
				for ride in rides:
					if ride.score < min_s:
						min_s = ride.score
						left_to_move = ride.e_start - car.steps
						dist = ride.dist(car.currX, car.currY)
						ride_to_remove = ride
				car.rides.append(ride_to_remove)
				car.busy = dist + ride.length
				rides.remove(ride_to_remove)
			else:
				car.update()
	i += 1000



def begin_logic_rides():
    global R, C, F, N, B, T, road, cars
    rides_to_remove = list()
    rides.sort(key = lambda x: x.score, reverse = False)
    while T > 0:
        if T%1000 == 0: print(str(T))
        for ride in rides:
            closest_car = -1
            closest_dist = -1
            dist = 0
            if ride.score <= 0:
                rides.remove(ride)
                continue
            for car in cars:
                dist = ride.dist(car.currX, car.currY)
                if car.busy == 0 and dist >= ride.score:
                    if closest_dist == -1 or closest_dist > dist:
                        closest_car = car
                        closest_dist = dist
            if closest_car != -1:
                closest_car.addRide(ride)
                closest_car.busy = ride.length
                closest_car.busy += dist
                rides.remove(ride)

        for car in cars:
            car.update()
        for ride in rides:
            ride.update_score()
        T -= 1000



def write_file(filename):
	global cars, rides
	file = open(filename+'out', 'w')
	string = ""
	for i in range(len(cars)):
		string += str(len(cars[i].rides))
		for ride in cars[i].rides:
			string += ' ' + str(ride.id)
		string += '\n'
	print(string)
	file.write(string)
	file.close()



if __name__ == '__main__':
	filename = sys.argv[1]
	main(filename)
	begin_logic_rides()
	write_file(filename[:len(filename)-2])
