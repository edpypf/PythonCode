import string
import random
# so the original code have 100*100 user name combination, it wastes memory space for all the names
# class User:
#     def __init__(self, name):
#         self.name = name

# def random_string():
#     chars = string.ascii_lowercase
#     return ''.join(
#         [random.choice(chars) for _ in range(8)]
#     )

# if __name__ == '__main__':
#     # print(random_string())
#     users = []
#     first_name = [random_string() for _ in range(100)]
#     last_name = [random_string() for _ in range(100)]

#     for first in first_name:
#         for last in last_name:
#             users.append(User(f'{first_name} {last_name}'))

# now we want to save this memory space, so we create pointers 
class User:
    def __init__(self, name):
        self.name = name

#The User2 class is more efficient in terms of memory usage compared to the User class because it reuses string objects for common substrings
class User2:
    strings = []        

    def __init__(self, full_name):
        # retrieve the index of s in strings
        def get_or_add(s):
            if s in self.strings:
                return self.strings.index(s)
            else:
                self.strings.append(s)
                return len(self.strings)-1
            
        self.nameidxs = [get_or_add(x) for x in full_name.split(' ')]

    def __str__(self):
        return ' '.join([self.strings[x] for x in self.nameidxs])        

def random_string():
    chars = string.ascii_lowercase
    return ' '.join(
        [random.choice(chars) for x in range(8)]
    )

if __name__ == '__main__':
    # print(random_string())
    users = []
    first_name = [random_string() for x in range(100)]
    last_name = [random_string() for x in range(100)]

    for first in first_name:
        for last in last_name:
            users.append(User(f'{first} {last}'))

    u2 = User2('Jim Jones')
    u3 = User2('Frank Jones')
    print(u2.nameidxs)
    print(u3.nameidxs)
    print(User2.strings)            

    for first in first_name:
        for last in last_name:
            users.append(User2(f'{first} {last}'))

    for user in users:
        print(user)
