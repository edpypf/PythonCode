def distribute_pie(n, k):
    distributions = []
    stack = [(1, [1])]

    while stack:
        curr_sum, curr_dist = stack.pop()

        if len(curr_dist) == k:
            if curr_sum == n:
                distributions.append(curr_dist)

        else:
            for i in range(1, n-curr_sum+2):
                new_sum = curr_sum + i
                if new_sum <= n:
                    stack.append((new_sum, curr_dist + [i]))

    return distributions

n = 8
k = 2

total=[]
distribute_pie(n, k) 
print(len(total))