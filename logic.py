import random
import sys
import os
import time


#WORLD INITALLIZING
world = []
xdim = int(sys.argv[1])
ydim = int(sys.argv[2])
autosnum = int(sys.argv[3])

for y in range(ydim):
	world.append([])
	for x in range(xdim):
		world[y].append({"state" : 1})

#AUTO hinzufuegen
for x in range(autosnum):
    world[random.randint(0, ydim - 1)][random.randint(0, xdim - 1)]["auto"] = {"ID" : x, "dir" : ""}

#LAMP INITIALLIZING
lpos = (random.randint(0, ydim) - 1, random.randint(0, xdim) - 1)
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

#PAINT WORLD			" " = state 0 (building) \ = = state 1 (street) \ @ = car \ H = Lampe 
def paintworld():
	for street in world:
		for place in street:
			symbols = {1 : "=", 0 : " ", "auto" : "@"}
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

		#DEPENDS on the DIRECTION of the MOVEMENT
		if coords[1] == xdim - 1:
			nextplace = world[coords[0]][0]
			nscoords = (coords[0], 0)
			
		else:	
			nextplace = world[coords[0]][coords[1] + 1]
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

#For every car, until they all state at the lamp
while autosnum > len(world[lpos[0]][lpos[1]].keys()) - 2:
	move()
	os.system("clear")


#Shows the final state of the world
render()

