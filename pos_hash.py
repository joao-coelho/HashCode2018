import sys
from collections import OrderedDict # OrderedDick

id_ride = 0
R = C = F = N = B = T = 0
rides = []; cars = []
free_cars = []


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
		# This score tells how many steps are still possible
		# in order to start the ride and get points for it
		self.score = self.l_finish - self.length

	# distance from input intersection to this ride's start point
	def dist(self, pointx, pointy):
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

    def update(self, steps):
        global free_cars
        if self.busy > 0:
            self.busy -= steps;
            if self.busy <= 0:
                self.busy = 0
                ride = self.rides[len(self.rides) - 1]
                self.currX = ride.fin_x
                self.currY = ride.fin_y
                free_cars.append(self)

#################################
#       Compute solution        #
#################################
def compute():
    global T, cars, free_cars
    rides.sort(key = lambda x: x.e_start, reverse = False)
    free_cars = list(cars)
    i = 0
    while i < T:
        rides_to_assign = rides[:len(free_cars)]
        for ride in rides_to_assign:
            closest_car = -1
            closest_dist = -1
            if ride.score - i < 0:
                rides.remove(ride)
                continue
            for car in free_cars:
                dist = ride.dist(car.currX, car.currY)
                if dist <= (ride.score - i):
                    if closest_dist == -1 or closest_dist > dist:
                        closest_car = car
                        closest_dist = dist
            if closest_car != -1:
                closest_car.addRide(ride)
                steps_to_finish = ride.length + closest_dist
                closest_car.busy = steps_to_finish
                free_cars.remove(closest_car)
                rides.remove(ride)
        for car in cars:
            car.update(1)
        i += 1

#################################
# Write results to filename.out #
#################################
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

#################################
#       Parse input file        #
#################################
def parse(filename):
	global R, C, F, N, B, T, rides
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

	for car in range(F):
		cars.append(Car());

def main(argv):
	filename = argv[1]
	parse(filename)
	compute()
	write_file(filename[:len(filename)-2])


if __name__ == '__main__':
	main(sys.argv)
