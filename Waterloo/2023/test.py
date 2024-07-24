def searchAround(r,c, x, y, matrix, word, w):
  res=[]
  for j in (-1,0,1):
    for k in (-1,0,1):
      if x+j>=0 and x+j<r and y+k>=0 and y+k<c and matrix[x+j][y+k]==word[w+1]: 
        res=[matrix[x+j][y+k], x+j, y+k]
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
    res = searchAround(r,c, x, y, matrix, word,w)
    if res not in pos and res:
      path += [[p]+[res]]
    #   print("path is  ssssssss  ",path) 
  return path

def nested(r,c,matrix,word,w,ppath): 
  path=[]
  for p in ppath:
    x=p[w][1]
    y=p[w][2]
    res = searchAround(r,c, x, y, matrix, word,w)
    if res not in ppath and res:
      p += [res]
    #   print("path is  ssssssss  ",path) 
  return ppath
 
 

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
for w in range(1, len(word2)-1,1):
    rpath=nested(rr,cc,matrix2,word2,w,path)
    print(len(rpath))