firstpoint = input("Please input the start position with x y: ").split(' ')
secondpoint = input("please input the end position with x y: ").split(' ')
offset = [[-1,2],[1,2],[1,-2],[-1,-2],[2,1],[2,-1],[-2,1],[-2,-1]]

nestedlist=[]


def convert2pos(inputStr):
    x=int(inputStr[0])
    y=int(inputStr[1])
    return [x,y]

def nextpos(pos):
    global numberofsteps
    nextlist=[]
    for step in offset:
        if pos[0]+step[0]>0 and pos[0]+step[0]<8 and pos[1]+step[1]>0 and pos[1]+step[1]<8:
            nextlist.append([pos[0]+step[0], pos[1]+step[1]])
            if end in nextlist:
                print(numberofsteps)
                print(nextlist)
                exit(numberofsteps)
    return nextlist

if __name__=='__main__':
    global numberofsteps
    numberofsteps=1
    start = convert2pos(firstpoint)
    end = convert2pos(secondpoint)
    nlist=nextpos(start)
    
    while numberofsteps<8:
        numberofsteps+=1
        if len(nestedlist)!=0:
            nlist=nestedlist[-1]
        for count, item in enumerate(nlist):
            nestedlist.append(nextpos(item))

    
 
