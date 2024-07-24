
def checkDup(arr):
    poss=[]
    # print([x for x in arr])
    arrpos=[poss.append(x) for x in arr if x not in poss]
    # print(len(arr), len(arrpos))
    return 0 if len(arr)==len(arrpos) else 1
        
x=-1
y=-5
pos=[[0, 0], [0, -1], [0, -2], [0, -3], [1, -3], [2, -3], [3, -3], [3, -4], [3, -5], [4, -5], [5, -5], [5, -4], [5, -3], [6, -3], [7, -3], [7, -4], [7, -5], [7, -6], [7, -7], [6, -7], [5, -7], [4, -7], [3, -7], [2, -7], [1, -7], [0, -7], [-1, -7], [-1, -6], [-1, -5]]

# x=0
# y=0
# pos=[]
move=''
while move!='q':
    m, s=input("Please enter u, d, l, f for moves, number for steps: ").split()
    move=str(m)
    steps=int(s)
    step=0
    if x >=-200 and x<=200 and y<=0 and y>=-200:
        if move=='q':   
            break    
        for step in range(1,steps+1):
            if move=='l':
                x-=1
            if move=='d':
                y-=1  
            if move=='r': 
                x+=1
            if move=='u': 
                y+=1
            pos.append([x, y])
                
        if checkDup(pos)>0:
            print(pos[-1][0], pos[-1][1], 'DANGER')
            break
        else:
            print(pos[-1][0], pos[-1][1], 'SAFE')
    else: 
        print(pos[-1][0], pos[-1][1], 'DANGER')
        print("out of limits")