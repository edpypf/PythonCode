from sys import stdin, stdout

acceptableChars = ['I','O','S','H','Z','X','N']

while True:
    word = stdin.readline()
    out = ''
    for x in range(len(word) - 1):
        if word[x] in acceptableChars:
            out = 'YES'
        else:
            out = 'NO'
        # break

    stdout.write(out)
    stdout.write('\n')