def person(number):
  print(f'the number is : {number}')
  return

threads=[]
for i in range(5):
  t=threading.Thread(target=person, args=(i,))
  threads.append(t)
  t.start()
