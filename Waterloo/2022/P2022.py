def cupcake(rbox, sbox):
  member = 28
  if member < rbox * 8 + sbox * 3:
    return rbox * 8 + sbox * 3 - member
  else:
    return 0
  
print(f'===================================================================') 
print(f'1> The first question - 1st test ' + str(cupcake(2, 5)))
print(f'The first question - 2nd test ' + str(cupcake(2, 4)))  
print(f'=====The first question - end -------------------------------------') 
print(f'                                                                   ') 

def Fergusonball(N, Points, Fouls):
  n_gplayer = 0
  for i in range(N):
    totScore = Points[i]*5 - Fouls[i]*3 
    if totScore > 40:
      n_gplayer += 1
  if n_gplayer == N:
    return str(n_gplayer) + '+'
  else:
    return str(n_gplayer)

print(f'2> The second question - 1st test ' + str(Fergusonball(3, [12,10,9],[4,3,1])))
print(f'The second question - 1st test ' + str(Fergusonball(2, [8,12],[0,1])))
print(f'=====The second question - end -------------------------------------') 
print(f'                                                                   ') 

import re
def mTurns(input):
#   rList = re.findall(r"\w+\+\d|\w+\-\d", input)
  rList = re.findall(r"\w+[\+|\-]\d", input)
  for r in rList:
    print(r.replace('+', ' tighten ').replace('-', ' loose '))

print(f'3> The Third question - 1st test ------------------------------ ')
mTurns('AFB+8SC-4H-2GDPE+9')
print(f'=====The Third question - end -------------------------------------') 
print(f'                                                                   ') 

def grp(M, same, N, diff, O, lgrp):
  vio=0
  for i in range(O):
    for j in range(M):
      print(same[j][1] , lgrp[i])
      if same[j][0] in lgrp[i] and same[j][1] not in lgrp[i]:
          vio+=1
    for k in range(N):
      print(diff[j][0] , lgrp[i])
      if diff[k][0] in lgrp[i] and diff[k][1] in lgrp[i]:
          vio+=1
  return vio      


print(f'4> The Fouth question - 1st test ------------------------------ ')
grp(1, [['ELODIE', 'CHI']],0,[[]],2,[['DWAYNE', 'BEN', 'CHI'],['PPP', 'FRANCOIS', 'ELODIE']])
print(f'=====The Fouth question - end -------------------------------------') 
print(f'                                                                   ') 

def square(M):
  rk=[]
  for i in range(1, M+1):
    for j in range(1, M+1):
      rk.append([i,j])
  return rk

def map(M, N, trees):
  apoint=[]
  ss=[]
  for i in range(1, M+1):
    for j in range(1, M+1):
      for k in range(1, M+1):
        for point in square(k):
          apoint=[point[0]+i, point[1]+j] 
          if apoint == trees:
            ss.append(k-1)
  return max(ss)

print(f'5> The Third question - 1st test ------------------------------ ')
print(map(5, 1, [2,4]))  
print(f'=====The Third question - end -------------------------------------') 
 
