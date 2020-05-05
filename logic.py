import random
import sys
import os
import time

xstreets = int(sys.argv[3])
ystreets = int(sys.argv[4])
autosnum = int(sys.argv[5])
tlnum = int(sys.argv[6])



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

world = []
xdim = int(sys.argv[1])
ydim = int(sys.argv[2])

for y in range(ydim):
	world.append([])
	for x in range(xdim):
		world[y].append({})				#Because it can contain more DIRS (KREUZ)

def place (coords):
        return world[coords[1]][coords[0]]
                
#Once the world *structure* is done, the streets can be divided into *rows* and *columns*

dirs = {"A" : (-1, 0), "D" : (1, 0), "W" : (0, -1), "S" : (0, 1)}		#inspired in game keyboard commands

#And the new key "dir" will be added to the place with the correspondant direction

rows = []
def setrow(ycoor, direction):
	for place in world[ycoor]:  #in case another direction was assigned before
                if len(place) > 0:
                        place["dir"].append(direction)
                else:
		        place["dir"] = [direction]	
        rows.append(ycoor)
	
columns = []
def setcolumn(xcoor, direction):
	for row in world:
                if len(row[xcoor]) > 0:  #in case of another direction
		        row[xcoor]["dir"].append(direction)
                else:
                        row[xcoor]["dir"] = [direction]
	columns.append(xcoor)

#these are the rows and columns that will be generated later... the streets. They are gonna be defined randomly first
                
streetindex = {"horizontal" : map(lambda x: random.randint(0, len(world) - 1), range(0, ystreets)),  #selected out of y coordinates range
               "vertical" :  map(lambda x: random.randint(0, len(world[0]) - 1), range(0, xstreets))}  #selected out of x coordinates range

#There are determinate directions that a vertical street, or an horizontal one can take...
[setrow(ycoor, random.choice(["A", "D"])) for ycoor in streetindex["horizontal"]]
[setcolumn(xcoor, random.choice(["W", "S"])) for xcoor in streetindex ["vertical"]]

#for easy mantainence of the code, the world was created using 0-n index!
#After the creation of the streets, I only need to know the coordenates x OR y of each one. That makes everything easier from now on.

def worldinfo():
    	intersections = [(x, y) for y in rows for x in columns]

	#FIRST and LAST place of each COLUMN and ROW. The output order must be (x, y), and therefore 2 functions.
        yborders = [(limit, ycoor) for limit in [0, ydim - 1] for ycoor in streetindex["horizontal"]]
	xborders = [(xcoor, limit) for limit in [0, ydim - 1] for xcoor in streetindex["vertical"]]
	
	return intersections, xborders, yborders

intersections, xborders, yborders = worldinfo()

#AUTO hinzufuegen
autocoords = []
for x in range(autosnum):
	autoindex = random.choice(xborders + yborders)					#AUTO ONLY SETABLE ON BORDERS!
	place(autoindex)["auto"] = {str(x) : random.choice(place(autoindex)["dir"])}
	autocoords.append(autoindex)

#LAMP INITIALLIZING

tlpos = []
for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
                  if abs(b) != abs(a):
                          for kreuz in intersections:
                                  tlpos.append((kreuz[0] + a, kreuz[1] + b))  #the edges are gonna be infinite windows, that means that negative numbers have no effect, since arrays in python can also be manipulated via negative index's

tlcolors = {"red": u"\u001b[38;5;1m", "green" : u"\u001b[38;5;2m"}			#ANSI CODE
for x in range(tlnum):  #use recursive behavior to discriminate previous already taken alternatives...
	tlindex = random.choice(tlpos)					
	world[tlindex[1]][tlindex[0]]["tl"]=  random.choice(tlcolors.keys())


for a in world:
        print a

#PAINT WORLD			" " = state 0 (building) \ = = state 1 (street) \ @ = car \ H = Lampe 
def paintworld():
	for row in world:  #a whole row is gonna be taken, because the world was defined in that order: First Y and then X
		for place in row:  #place is a dictionary
			symbols = {"auto" : u"\u001b[38;5;39m@ ",
                                   "A" : "< ",
                                   "W" : "^ ",
                                   "S" : "v ",
                                   "D" : "> "}
			todraw = ""

			if len(place) == 0:							#NOT STREET
				todraw = " "
			elif len(place["dir"]) > 1:                          #INTERSECTION when there are more dirs attached to the street
				if "auto" in place.keys():						#WITH AUTO
					todraw = symbols["auto"]		
				else:									#ALONE 
					todraw = "* "
			elif len(place) > 1:         #STREET
				if "tl" in place.keys():						#WITH TRAFFIC LIGHT
					todraw = tlcolors[place["tl"]]
				if "auto" in place.keys():						#WITH AUTO
					todraw = todraw + symbols["auto"] 
				
				else: 
					todraw = todraw + symbols[place["dir"][0]] #ONLY
			sys.stdout.write(todraw.ljust(2))
			sys.stdout.write(u"\u001b[0m")
		print ""


paintworld()
sys.exit()
                
#MAIN FUNCTION

def detectlampe(place):
	if "lampe" in place.keys():
		if place["tl"] == u"\u001b[38;5;1m":
			return "red"
		else:
			return "green"

def move(autosindex, cond):							#RECURSIVE	
	print autosindex
	print cond	
	
	paintworld()   
	
	recurindex = []

	for coords in autosindex: 
		change = random.choice(getstruct(coords, world)["street"])	#TUPLE
		
		if coords[":y"] + change[1] == ydim - 1:			#Y EDGE
			nextcoords = {":x" : coords[":x"], ":y" : 0}
			
		elif coords[":x"] + change[0] == xdim + 1:			#X EDGE
			nextcoords = {":x" : 0, ":y" : coords[":y"]}		
		else:	
			nextcoords = {":x" : coords[":x"] + change[0] , ":y" : coords[":y"] + change[1]} 
       
		if detectlampe(getstruct(coords, world)) == "red" or "auto" in getstruct(nextcoords, world).keys():		#TRAFFIC LIGHT
		    continue
		else:               
			auto = getstruct(coords, world).pop("auto")	
			getstruct(nextcoords, world)["auto"] = auto
			recurindex.append(nextcoords)
			time.sleep(1)
	if cond == 0:
		os.system("clear")
		paintworld()
		print "MAKED"
		return ["a"]	
	else:
		sys.stdout.write("RECURSIVE!")
		os.system("clear")
		move(recurindex, cond - 1)



print move(autocoords, 20)


