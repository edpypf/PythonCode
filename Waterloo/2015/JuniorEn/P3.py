l = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11, 'l':12, 'm':13, 'n':14, 'o':15, 'p':16, 'q':17, 'r':18, 's':19, 't':20, 'u':21, 'v':22, 'w':23, 'x':24, 'y':25, 'z':26}
vowel = ['a','e','i', 'o', 'u']
x=input('please input a word: ')

def closevowel(i):
    if i in vowel:
        return ''
    min=0
    for j in vowel:
        current=(l[i]-l[j])
        if abs(min)>abs(current) or min==0:
            min=current
    return [k for k, v in l.items() if v == l[i]-min][0]

def nextcons(i):
    if i in vowel:
        return ''
    for n in range(1, 3):
        letter= [k for k,v in l.items() if v == l[i]+n]
        if letter[0] not in vowel:
            return letter[0]
    if i in vowel:
        return
tsr=''.join([i+closevowel(i)+nextcons(i) for i in x])
print(tsr) 

# print(closevowel('h'))

# joy --> jik  o  yuz