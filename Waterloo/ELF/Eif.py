# Define a variable for debugging
elf="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
holding=""" 12 red, 13 green, 14 blue"""

# This function will unpack and flattern all game values to be indivdual dictionary for condition checking
def color_dict(colorPair):
    _, camt, colkey = colorPair.split(' ')
    cdict=dict.fromkeys([colkey],camt)
    return cdict
    
# This function is to handle one more split by ';'
def color_handler(gamevalue):
    dlist=[]
    for color in gamevalue.split(';'):
        for col in color.split(','):
            dlist.append(color_dict(col))
    return dlist

# using the upack and dict directly to make a list of dictionaries
def getGameDict(elf):
    gamedict=[]
    for l in elf.split('\n'):
        gamekey, gamevalue = l.split(':')[0], l.split(':')[1]
        gdict = dict.fromkeys([gamekey],gamevalue)
        gamedict.append(gdict)
    return gamedict

# using the unpack and zip to make a dict
def flatternDict(elf):
    gamekey=[]
    gamevalue=[]
    for l in elf.split('\n'):
        k, v = l.split(':')[0], l.split(':')[1]
        gamekey.append(k)
        gamevalue.append(color_handler(v))
    gamedict = dict(zip(gamekey, gamevalue))
    return gamedict

# convert holding to dict
def holder_to_dict(holding):
    dlist=[]
    for col in holding.split(','):
        dlist.append(color_dict(col))
        print(col)
    return dlist

condition=holder_to_dict(holding)
gameFlatDict=flatternDict(elf)
print(gameFlatDict)

fullList=[]
excludeList=[]
gnumset=set()
fullset=set()
for g, gv in gameFlatDict.items():
    for i in gv:
        for c in condition:
            fullList = [g for k in c if k in i] 
            excludeList = [g for k in c if k in i and int(c[k])<int(i[k])]
            gnumset.update(set([int(str(excludeList[0][5:])) if len(excludeList)>0 else 0]))
            fullset.update(set([int(str(fullList[0][5:])) if len(fullList)>0 else 0]))
print(sum(fullset.difference(gnumset)))