import random
import sys
import os
import time


world = []
xdim = int(sys.argv[1])
ydim = int(sys.argv[2])
xstreets = int(sys.argv[3])
ystreets = int(sys.argv[4])
autosnum = int(sys.argv[5])
dirs = {"A" : (-1, 0), "D" : (1, 0), "W" : (0, -1), "S" : (0, 1)}		#inspired in game keyboard commands

#Function framework
def unfold(array, retain): 
	for element in array: 
        	if type(element) == list:  		
			unfold(element, retain)
        	else: 
            		retain.append(element)
	return retain 

#WORLD INITALLIZING
for y in range(ydim):
	world.append([])
	for x in range(xdim):
		world[y].append({"street" : []})				#Because it can contain more DIRS (KREUZ)




#STREETS struct		[{"street" : (dir)}, {}...]
rows = []
def setrow(row, direction):
	print row
	for index, place in enumerate(row):
		place["street"].append(dirs[direction])	
		rows.append({":x": index, ":y": world.index(row)})	
columns = []
def setcolumn(xcoor, direction):
	for index, street in enumerate(world):
		street[xcoor]["street"].append(dirs[direction])
		columns.append({":x": xcoor, ":y" : index})	
streetindex = {"x" : map(lambda x: random.randint(0, len(world) - 1), range(0, ystreets)), "y" :  map(lambda x: random.randint(0, len(world[0]) - 1), range(0, xstreets))}
map(lambda x: setrow(world[x], "A"), streetindex["y"])	
map(lambda x: setcolumn(x, "S"), streetindex["x"])

""" -------> DEBUGGING
print "JALSKDJFLAKSD;F"
print rows
print columns
print "ALSJHF A;JDFJ"
"""

def worldinfo():
	places = filter(lambda element: (columns + rows).count(element) == 1, (columns + rows)) 		#WITHOUT INTERSECTIONS
	intersections = filter(lambda element: element in rows, columns)
	purestreet = filter(lambda element: element not in intersections, places)
	xborders = [element for cond in [0, xdim - 1] for element in rows if element[":x"] == cond]	
	yborders = [element for cond in [0, ydim - 1] for element in columns if element[":y"] == cond]	
	
	print xborders
	print yborders
	
	return intersections, purestreet, places, xborders, yborders

intersections, purestreet, places, xborders, yborders = worldinfo()

map(lambda x: sys.stdout.write(str(x) + "\n\n"), world)
time.sleep(2)
os.system("clear")


#AUTO hinzufuegen
for x in range(autosnum):
	autoindex = random.choice(xborders + yborders)
	world[autoindex[":y"]][autoindex[":x"]]["auto"] = {"ID" : x, "dir" : random.choice(world[autoindex[":y"]][autoindex[":x"]]["street"]) }

map(lambda x: sys.stdout.write(str(x) + "\n\n"), world)

#LAMP INITIALLIZING

tlindex = map(lambda index: map(lambda direction: (index[0] - direction[0], index[1] - direction[1]), world[index[1]][index[0]]["street"]), intersections)

print tlindex


world[lpos[0]][lpos[1]]["lampe"] = ""
def lamphandlung(color):
	colors = {0 : u"\u001b[38;5;1m", 1 : u"\u001b[38;5;2m"}
	for y in world:
		for x in y:
			if "lampe" in x.keys():		
				x["lampe"] = colors[color]
"""
u"\u001b[38;5;1m" -------> ANSI CODE for RED
u"\u001b[38;5;2m" -------> ANSI CODE for GREEN
"""   
lamphandlung(0)

# street : (dir)
#PAINT WORLD			" " = state 0 (building) \ = = state 1 (street) \ @ = car \ H = Lampe 
def paintworld():
	for street in world:
		for place in street:
			symbols = {1 : "=", 0 : " ", "auto" : u"\u001b[38;5;39m@"}
			todraw = ""
			if "lampe" in place.keys():
				todraw = place["lampe"]
			if "auto" in place.keys():
				todraw = todraw + symbols["auto"] + " " 
			else:
				todraw = todraw + symbols[place["state"]] + " " 
			sys.stdout.write(todraw.ljust(2))
			sys.stdout.write(u"\u001b[0m")
		print ""

#MAIN FUNCTION

def detectlampe(place):
	if "lampe" in place.keys():
		if place["lampe"] == u"\u001b[38;5;1m":
			return "red"
		else:
			return "green"

def move():
	#PAINT the world before THE CHANGE
	paintworld()   

	autocoords =[] 
	for street in world:
		for place in street:
		    if "auto" in place.keys():
			y = world.index(street)
			x = street.index(place)	
			autocoords.append((y, x))
	for coords in autocoords: 
		carplace = world[coords[0]][coords[1]]
		dirs = (0, 1) 
		#DEPENDS on the DIRECTION of the MOVEMENT
		if coords[1] == xdim - 1:			#X EDGE
			nextplace = world[coords[0]][0]
			nscoords = (coords[0], 0)
			
		else:	
			nextplace = world[coords[0] + dirs[0]][coords[1] + dirs[1]]
			nscoords = (coords[0], coords[1] + 1)


		#Wenn da eine Lampe ist, nicht bewegen.        
		if detectlampe(carplace) == "red" or "car" in nextplace.keys():
		    continue #The position (coords) of the next car would be taked
		else:               
			#Um sich zu bewegen
			auto = carplace.pop("auto")	
			world[nscoords[0]][nscoords[1]]["auto"] = auto
			time.sleep(0.01)

	return "1 BEWEGUNG"

#For every car, until they all state at the lamp
while autosnum > len(world[lpos[0]][lpos[1]].keys()) - 2:
	move()
	os.system("clear")


#Shows the final state of the world
render()

