def searchAround(r,c, x, y, matrix, word, w):
  res=[]
  for j in (-1,0,1):
    for k in (-1,0,1):
      if x+j>=0 and x+j<r and y+k>=0 and y+k<c and matrix[x+j][y+k]==word[w+1]: 
        res+=[[matrix[x+j][y+k], x+j, y+k]]
  return res
        
def mytha(r,c,matrix,word,w):
  pos=[]
  for row in range(r):
    for col in range(c):
      if ([matrix[row][col], row, col][0][0]==word[w]):
        pos+=[[matrix[row][col], row, col]]
  npos=[]
  path=[]
  for p in pos:  
    x=p[1]
    y=p[2]
    ress = searchAround(r,c, x, y, matrix, word,w)
    for res in ress:
      if res not in pos and res:
        path += [[p]+[res]] 
        print(path)
  return path

def nested(r,c,matrix,word,w,ppath): 
  path=[]
  for p in ppath:
    try:
      if len(p)<w+2 and p[w][1] and p[w][2]:  
        x=p[w][1]
        y=p[w][2]
        p1=p.copy()
        ress = searchAround(r,c, x, y, matrix, word,w)
        for i, res in enumerate(ress):
          if res not in ppath and res and i==0:
            p += [res] 
            print(ppath)
          elif res not in ppath and res:
            p[i]=p1
            ppath+=[p[i]]
            p[i]+=[res] 
            print(ppath)
    except IndexError:
      pass
  return ppath


# r=5
# c=7
# matrix=[['F','T','R','U','B','L','K'],\
#         ['P','M','N','A','X','C','U'],\
#         ['A','E','R','C','N','E','O'],\
#         ['M','N','E','U','A','R','M'],\
#         ['M','U','N','E','M','N','S']]
# word='MENU'
# w=0 
# path=mytha(r,c,matrix,word,0)
# print(f'1> first test result ===============================================')
# for w in range(1, len(word)-1,1):    
#     rpath=nested(r,c,matrix,word,w,path)
#     print(len(rpath))    
# print(f'                                                                    ')

rr=6
cc=9
matrix2=[['N','A','T','S','F','E','G','Q','N'], \
         ['S','A','I','B','M','R','H','F','A'], \
          ['C','F','T','J','C','U','C','L','T'], \
           ['K','B','H','U','P','T','A','N','U'], \
            ['D','P','R','R','R','J','D','I','R'], \
             ['I','E','E','K','M','E','G','B','E']] 
word2='NATURE'
w=0 
path=mytha(rr,cc,matrix2,word2,0)
print(f'2> second test result ===============================================')
for w in range(1, len(word2)-1,1):    
    rpath=nested(rr,cc,matrix2,word2,w,path)
    print(len(rpath)) 
for path in rpath:
  print(len(path))