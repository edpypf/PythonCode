# R=int(input("please input the rows: "))
# C=int(input("please input the columns: "))

# patch=[]

# for i in range(R):
#     line=input("please input the row content: ")
#     patch.append([s for s in line.split() if len(line)==C])
#     i+=1

# start_row=int(input("please input the start rows: "))
# start_col=int(input("please input the start column: "))

# # print(patch)

# print(patch[start_row-1, start_col-1])
R=6
C=6
x=0
y=0
patch=[]
patch.append('**LMLS')
patch.append('S*LMMS')
patch.append('S*SMSM')
patch.append('***SLL')
patch.append('LLM*MS')
patch.append('SSL*SS')

start_row=2
start_col=4

# print(patch[start_row-1][start_col-1])
visited = [[False for _ in range(C)] for _ in range(R)]
directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]
pumpkin_values = {"S": 1, "M": 5, "L": 10}


def dfs(row, col):
    if not (0 <= row < R and 0 <= col < C):
      return 0
    if visited[row][col]:
      return 0
    if patch[row][col] == "*":
      return 0
    
    visited[row][col] = True
    total_value = pumpkin_values.get(patch[row][col], 0)
    for dx, dy in directions:
        total_value +=dfs(row +dy, col+dx)
    return total_value
         
print(dfs(start_row, start_col))
