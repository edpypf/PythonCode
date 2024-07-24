def searchAround(r, c, x, y, matrix, word, w):
  res=[]
  for j in (-1,0,1):
    for k in (-1,0,1):
      if x+j>=0 and x+j<r and y+k>=0 and y+k<c and matrix[x+j][y+k]==word[w+1]: 
        res.append([matrix[x+j][y+k], x+j, y+k])
  return res
        
def mytha(r, c, matrix, word, w):
  pos=[]
  for row in range(r):
    for col in range(c):
      if ([matrix[row][col], row, col][0][0]==word[w]):
        pos.append([matrix[row][col], row, col])
  npos=[]
  path=[]
  for p in pos:  
    x=p[1]
    y=p[2]
    res = searchAround(r, c, x, y, matrix, word, w)
    if res not in pos and res:
      path.append([[p]+[r] for r in res])
  return path

def nested(r, c, matrix, word, w, ppath): 
  path=[]
  for p in ppath:  
    x=p[w][1]
    y=p[w][2]
    res = searchAround(r, c, x, y, matrix, word, w)
    if res not in p:
      for r in res:
        newp = [p[i] for i in range(len(p))]
        newp.append(r)
        path.append(newp)
  return path
 
def diagonal(r, c, matrix, word):
  paths = mytha(r, c, matrix, word, 0)
  for w in range(1, len(word)-1):
    paths = nested(r, c, matrix, word, w, paths)
  return [p for p in paths if len(p) == len(word)]

r=5
c=7
matrix=[['F','T','R','U','B','L','K'],\
        ['P','M','N','A','X','C','U'],\
        ['A','E','R','C','N','E','O'],\
        ['M','N','E','U','A','R','M'],\
        ['M','U','N','E','M','N','S']]
word='MENU'

print(diagonal(r, c, matrix, word))

rr=6
cc=9
matrix2=[['N','A','T','S','F','E','G','Q','N'], \
         ['S','A','I','B','M','R','H','F','A'], \
         ['C','F','T','J','C','U','C','L','T'], \
         ['K','B','H','U','P','T','A','N','U'], \
         ['D','P','R','R','R','J','D','I','R'], \
         ['I','E','E','K','M','E','G','B','E']] 
word2='NATURE'

print(diagonal(rr, cc, matrix2, word2))
