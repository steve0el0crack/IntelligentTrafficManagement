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
tlnum = int(sys.argv[6])
dirs = {"A" : (-1, 0), "D" : (1, 0), "W" : (0, -1), "S" : (0, 1)}		#inspired in game keyboard commands

#Function framework
def unfold(array, retain): 
	for element in array: 
        	if type(element) == list:  		
			unfold(element, retain)
        	else: 
            		retain.append(element)
	return retain 

def getstruct(dicc, world):
	return world[dicc[":y"]][dicc[":x"]]

def getkeybyvalue(dicc, value):
	for relation in dicc.items():
		if relation[1] == value:
			return relation[0]

#WORLD INITALLIZING
for y in range(ydim):
	world.append([])
	for x in range(xdim):
		world[y].append({"street" : []})				#Because it can contain more DIRS (KREUZ)


#STREETS struct		[{"street" : (dir)}, {}...]
rows = []
def setrow(row, direction):
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

def worldinfo():
	places = filter(lambda element: (columns + rows).count(element) == 1, (columns + rows)) 		#WITHOUT INTERSECTIONS
	intersections = filter(lambda element: element in rows, columns)
	purestreet = filter(lambda element: element not in intersections, places)
	
	#FIRST and LAST place of each COLUMN and ROW 
	xborders = [element for cond in [0, xdim - 1] for element in rows if element[":x"] == cond]	
	yborders = [element for cond in [0, ydim - 1] for element in columns if element[":y"] == cond]	
	
	return intersections, purestreet, places, xborders, yborders

intersections, purestreet, places, xborders, yborders = worldinfo()

#AUTO hinzufuegen
for x in range(autosnum):
	autoindex = random.choice(xborders + yborders)					#AUTO ONLY SETABLE ON BORDERS!
	world[autoindex[":y"]][autoindex[":x"]]["auto"] = {"ID" : x, "dir" : random.choice(world[autoindex[":y"]][autoindex[":x"]]["street"]) }


#LAMP INITIALLIZING
tlpos = unfold(map(lambda coors: map(lambda direction: {":x": coors[":x"] - direction[0], ":y" : coors[":y"] - direction[1]} ,getstruct(coors, world)["street"]), intersections), [])

tlcolors = {"red": u"\u001b[38;5;1m", "green" : u"\u001b[38;5;2m"}			#ANSI CODE
for x in range(tlnum):
	tlindex = random.choice(tlpos)					
	world[tlindex[":y"]][tlindex[":x"]]["tl"] =  random.choice(tlcolors.values())


#PAINT WORLD			" " = state 0 (building) \ = = state 1 (street) \ @ = car \ H = Lampe 
def paintworld():
	for street in world:
		#print street
		for place in street:
			symbols = {"auto" : u"\u001b[38;5;39m@ ", (-1,0) : "< ", (0, -1) : "^ ", (0, 1) : "v ", (1, 0) : "> "}
			todraw = ""

			if len(place["street"]) == 0:							#NOT STREET
				todraw = " "
			elif len(place["street"]) > 1: 							#INTERSECTION
				if "auto" in place.keys():						#WITH AUTO
					todraw = symbols["auto"]		
				else:									#ALONE 
					todraw = "* "
			elif len(place["street"]) == 1:							#STREET
				if "tl" in place.keys():						#WITH TRAFFIC LIGHT
					todraw = place["tl"]
				if "auto" in place.keys():						#WITH AUTO
					todraw = todraw + symbols["auto"] 
				
				else:
					todraw = todraw + symbols[place["street"][0]]			#ONLY
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
			time.sleep(1)

	return "1 BEWEGUNG"




paintworld()










#For every car, until they all state at the lamp
#while autosnum > len(world[lpos[0]][lpos[1]].keys()) - 2:
#for x in range(20):
#	move()
#	os.system("clear")


#Shows the final state of the world
render()

