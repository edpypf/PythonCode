def distribute_pie(n, k):
    total = []
    queue = [(n, k, [])]  # queue stores remaining pieces of pie, people, and current distribution
    
    while queue:
        n, k, curr_dist = queue.pop(0)
        
        # base case: all pieces have been distributed
        if n == 0 and k == 0 and sorted(curr_dist) == curr_dist:    
            total.append(curr_dist)
        
        # recursive case: distribute one piece to the current person and add new state to the queue
        if n > 0 and k > 0:
            new_dist = curr_dist + [1]
            queue.append((n - 1, k - 1, new_dist))
            
            # distribute remaining pieces to remaining people and add new states to the queue
            for i in range(2, n - k + 2):
                new_dist = curr_dist + [i]
                queue.append((n - i, k - 1, new_dist))
    
    return total


n = 8
k = 4

print(distribute_pie(n, k))
 