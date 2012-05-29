import random
import math
import getopt
import sys
import GeneticAlgorithm

# Octagon
# 26,2 62,2 87,26 87,62 62,87 26,87 2,62 2,26
# Star
# 350,75 379,161 469,161 397,215 423,301 350,250 277,301 303,215 231,161 321,161

# -- Config for generating random cities --
# Number of cities
citiesN = 10
# x & y range for positions
width = 250
height = 250

# -- Config for Generic Algorithm
# The number of routes in each generation.
population = 3
# Number of generations.
generations = 150
# The change a crossover happens for every 2 routes that go from the
# old generation to the next.
crossoverChance = 0.7
# The change of a mutation for each route that goes from the old
# generation to the next.
mutationChance = 0.5


class Route(GeneticAlgorithm.SolutionCandidate):
        def __init__(self, cities):
                self.cities = cities
                
        def _distance(self, city1, city2):
                """Calculate the distance between two cities."""
                return math.hypot(city2[0] - city1[0],
                                  city2[1] - city1[1])
	
        def getLength(self):
                """Calculate the length of the route."""
                return sum([self._distance(self.cities[i-1],
                                           self.cities[i]) \
                                    for i in range(len(self.cities))])
        
        def getFitness(self):
                return 1 / pow(self.getLength(), 2)

        def crossover(self, route):
                x1 = len(self.cities) / 3
                x2 = x1 * 2
                routes = [self.cities, route.cities]
                
                crossParts = [r[x1:x2] for r in routes]	
                crossParts.reverse()
	
                for i in range(len(routes)):   
                        route = routes[i]
                        cross = crossParts[i]

                        for j in range(x1) + range(x2, len(route)):
                                while route[j] in cross:
                                        route[j] = crossParts[i-1][cross.index(route[j])]
                        for j in range(x1,x2):
                                route[j] = cross[j-x1]
                                
#muteerd de gegeven routes door twee steden van plaats te verwisselen
        def mutate(self):
                index1 = random.randint(0, len(self.cities) - 1)
                index2 = random.randint(0, len(self.cities) - 1)
                n = self.cities[index1]
                self.cities[index1] = self.cities[index2]
                self.cities[index2] = n

        def copy(self):
                return Route(self.cities[:])

        def createMap(self):
                """Generate a svg image with the given route."""
                left = min([pos[0] for pos in self.cities]) - 5
                right = max([pos[0] for pos in self.cities])
                top = min([pos[1] for pos in self.cities]) - 5
                bottom = max([pos[1] for pos in self.cities])
                
                width = right - left + 5
                height = bottom - top + 5

                ret = '<?xml version="1.0"?>' + "\n"
                ret += '<svg xmlns="http://www.w3.org/2000/svg" width="' + \
                    str(width) + '" height="' + str(height) + \
                    '" version="1.1">' + "\n" 

                ret += '<polygon fill="none" stroke="currentColor" points="' + \
                    " ".join([str(pos[0] - left) + "," + str(pos[1] - top) \
                                      for pos in self.cities]) + \
                    '"/>' + "\n"
        
                ret += '<g fill="#f00">' + "\n"
                for pos in self.cities:
                        ret += '   <circle cx="' + \
                            str(pos[0] - left) + '" cy="' + \
                            str(pos[1] - top) + '" r="5"/>' + "\n"
                ret += "</g></svg>\n"
                return ret

                
class RandomRouteFactory(GeneticAlgorithm.SolutionCandidateFactory):
        def __init__(self, cities):
                self.cities = cities
                
        def generate(self):
                cities = self.cities[:]
                random.shuffle(cities)
                return Route(cities)

def usage ():
        print "Usage tsp.py [-h -r -i image.svg]"

def generateRandomCities(n, width, height):
        return [[random.randint(0,width),
                 random.randint(0,height)] for x in range(n)]

def parseCities(args):
        cities = []
        for arg in args:
                arg = arg.split(',')
                if len(arg) == 2:
                        cities.append([int(arg[0]), int(arg[1])])        
        return cities

def writeMap(mapFile, route):
        f = open(mapFile, 'w')
        f.write(route.createMap())
        f.close()

cityPositions = []
mapFile = False

opts, args = getopt.getopt(sys.argv[1:], "hri:")

for opt, value in opts:
        if opt == '-h':
                usage()
                exit()
        elif opt == '-r':
                cityPositions = generateRandomCities(citiesN, width, height)
        elif opt == '-i':
                mapFile = value

if cityPositions == []:
        cityPositions = parseCities(args)

if cityPositions == []:
        usage()
        exit(1)
        
generator = RandomRouteFactory(cityPositions)
ga = GeneticAlgorithm.GeneticAlgorithm(generator,
                                       crossoverChance,
                                       mutationChance,
                                       population)
print "Gen.\tAvg.\tBest"
for i in range(generations):
        # create a new generation
	ga.evolve()

        # Calculate the lengths of the routes
	lengths = [route.getLength() for route in ga.getSolutions()]
        
        # Print the average length of the routes and the length of the
        # shortest route
	print i + 1,"\t", \
            int(sum(lengths) / len(lengths)),"\t", \
            int(min(lengths))

shortest = ga.getBestSolution()

print "Shortest route: " + " ".join([str(pos[0]) + "," + str(pos[1]) \
                                             for pos in shortest.cities])

if mapFile != False:
        writeMap(mapFile, shortest)


