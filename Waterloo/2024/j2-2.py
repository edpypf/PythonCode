
sline = []    
ssize=int(input("please input a number: "))
while True:
    num_in_line=input("please input a number: ")
    if num_in_line:
        sline.append(int(num_in_line))
    else:
        for e in sline:
            if ssize > int(e):
                ssize+=int(e)
            else:
                print(ssize)
                break