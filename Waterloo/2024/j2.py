# The 1st way
ssize=int(input("please input a start number: "))
sliststring=input("please input a list of numbers that are separated by comma: ")

slist = sliststring.split(',')

for e in slist:
    if ssize > int(e):
        ssize+=int(e)
    else:
        print(ssize)
        break

# The 2nd way
    
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

slist = sliststring.split(',')

for e in slist:
    if ssize > int(e):
        ssize+=int(e)
    else:
        print(ssize)
        break

