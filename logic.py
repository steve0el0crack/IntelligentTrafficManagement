import random


#WORLD
#Stellen
places = []
placesnum = 5
autosnum = 3

for i in range(0,placesnum):
    places.append([{"state" : 1}])

#AUTO hinzufuegen
for x in range(0, autosnum):
    places[random.randint(0,len(places)-1)].append({"auto" : "auto", "ID" : x})

#LAMP
lpos = random.randint(0,len(places)-1)
places[lpos].append({"lampe" : ""})


#0 ROT
#1 GRUENN
def lamphandlung(ziel):
    for x in range(0,len(places)):
        for i in range(0, len(places[x])):
            if places[x][i].keys()[0] == "lampe":
                places[x][i]["lampe"] = ziel                                                                                                                    
lamphandlung(0)


def render():
    print "\n------"
    for x in places:
        print x
    print "-------\n"

def move():
    #Shows the world before THE CHANGE
    render()
    
    autostellen ={} 
    #print "AUTO PLACES SEARCH\n............"
    for stelle in places:
        #print "STELLE: " + str(stelle)
        for dicc in stelle:
            #print "DICC: " + str(dicc)
            if "auto" in dicc.keys():
                autostellen[places.index(stelle)] = dicc
    
    #print "AUTOS: " + str(autostellen)
    #print "............\n"
    
    tmpanzahl = len(autostellen.keys())
    
    for bewegnumber in range(0,tmpanzahl): 
        autopos = autostellen.keys()[bewegnumber]
        #print "AUTO MOVEMENT\nXXXXXXXXXXX"
        #print type(autopos)
            
        # Um zu gucken was es da ueberhaupt gibt
        tmp = []
        for i in range(0, len(places[autopos])):
            tmp.append(places[autopos][i].values()[0])
        #print "Es gibt da: " + str(tmp)
        #Wenn da eine Lampe ist, nicht bewegen.        
        if 0 in tmp and "auto" in tmp:
            continue #Wird das naechste Auto angegriffen um zu bewegen, in der Liste Autostellen.keys()
        else:                
            #Um sich zu bewegen
            autostruc = autostellen.values()[bewegnumber]
            #print places[autopos]
            #print autostruc
            #places[autopos].index(autostruc)
            places[autopos].remove(autostruc)
            if autopos == placesnum - 1:
                #print "APPEND"
                places[0].append(autostruc)
            else:
                places[autopos+1].append(autostruc)
  
    return "1 BEWEGUNG"
        

#For every car, until they all state at the lamp
while autosnum > len(places[lpos]) - 2:
    move()

#Shows the final state of the world
render()

