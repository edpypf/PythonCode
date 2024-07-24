from sys import stdin, stdout

YEAR = str(int(stdin.readline())+1)
lst = []
res = ''

def checkIfDuplicates(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

while True:
  for x in range(len(YEAR)):
    lst.append(YEAR[x])
#  print(lst)
  if checkIfDuplicates(lst):
    lst.clear()
    YEAR = str(int(YEAR) + 1)
  else:
    res = YEAR
    break

stdout.write(res) 