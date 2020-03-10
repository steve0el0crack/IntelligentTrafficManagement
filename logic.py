import random
import sys
import os
import time


#WORLD
#Stellen
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

#LAMP
lpos = (random.randint(0, ydim) - 1, random.randint(0, xdim) - 1)
world[lpos[0]][lpos[1]]["lampe"] = ""


#0 ROT
#1 GRUENN
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


def render():
    print "\n------"
    for x in world:
        sys.stdout.write(str(x) + "\n")
    print "-------\n"

def move():
    #Shows the world before THE CHANGE
    render()
    
    autostellen ={} 
    for stelle in world:
        for dicc in stelle:
            if "auto" in dicc.keys():
                autostellen[world.index(stelle)] = dicc
    
    tmpanzahl = len(autostellen.keys())
    
    for bewegnumber in range(0,tmpanzahl): 
        autopos = autostellen.keys()[bewegnumber]
            
        # Um zu gucken was es da ueberhaupt gibt
        tmp = []
        for i in range(0, len(world[autopos])):
            tmp.append(world[autopos][i].values()[0])
        #Wenn da eine Lampe ist, nicht bewegen.        
        if 0 in tmp and "auto" in tmp:
            continue #Wird das naechste Auto angegriffen um zu bewegen, in der Liste Autostellen.keys()
        else:                
            #Um sich zu bewegen
            autostruc = autostellen.values()[bewegnumber]
            world[autopos].remove(autostruc)
            if autopos == xdim - 1:
                world[0].append(autostruc)
            else:
                world[autopos+1].append(autostruc)
	time.sleep(1)
	
    return "1 BEWEGUNG"

#PRESENT AND PAINT WORLD			" " = state 0 (building) \ = = state 1 (street) \ @ = car \ H = Lampe 
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
paintworld()

#For every car, until they all state at the lamp
while autosnum > len(world[lpos[0]][lpos[1]].keys()) - 2:
	move()
	os.system("clear")


#Shows the final state of the world
render()

