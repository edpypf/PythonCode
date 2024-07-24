# Define a variable for debugging
elf="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

# This function will unpack and flattern all game values to be indivdual dictionary for condition checking
def color_handler(gamevalue):
    dlist=[]
    for color in gamevalue.split(';'):
        #print(color)
        for col in color.split(','):
            _, camt, colkey = col.split(' ')
            # print(colkey)
            # print(camt)
            cdict=dict.fromkeys([colkey],camt)
            # print(cdict)
            dlist.append(cdict)
    # print(dlist)
    return dlist
# color_handler(' 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')        

# using the upack and dict directly to make a list of dictionaries
gamedict=[]
for l in elf.split('\n'):
    gamekey, gamevalue = l.split(':')[0], l.split(':')[1]
    gdict = dict.fromkeys([gamekey],gamevalue)
    gamedict.append(gdict)
print(gamedict)

# using the unpack and zip to make a dict
gamekey=[]
gamevalue=[]
for l in elf.split('\n'):
    k, v = l.split(':')[0], l.split(':')[1]
    gamekey.append(k)
    gamevalue.append(color_handler(v))
gamedict = dict(zip(gamekey, gamevalue))
print(gamedict)