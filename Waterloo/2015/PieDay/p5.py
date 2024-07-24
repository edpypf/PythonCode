def distribute_pie(n, k, curr_dist):
    # base case: all pieces have been distributed
    print(curr_dist)
    if n == 0 and k == 0 and sorted(curr_dist) == curr_dist:
        total.append(curr_dist)
    # recursive case: distribute one piece to the current person and recurse
    if n > 0 and k > 0:
        distribute_pie(n - 1, k - 1, curr_dist + [1])
        
        # distribute remaining pieces to remaining people
        for i in range(2, n - k + 2):
            distribute_pie(n - i, k - 1, curr_dist + [i])

n = 8
k = 4

total=[]
distribute_pie(n, k, []) 
print(len(total))