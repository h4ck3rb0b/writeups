from itertools import permutations
from subprocess import Popen

f1 = open("mind", "rb")
f2 = open("power", "rb")
f3 = open("reality", "rb")
f4 = open("soul", "rb")
f5 = open("space", "rb")
f6 = open("time", "rb")

for i in permutations(["mind", "power", "reality", "soul", "space", "time"], 6):
    print(i)
    x = b''
    for a in i:
        with open(a, 'rb') as f:
            x += f.read()
    with open('a.zip', 'wb') as f:
        f.write(x)

    child = Popen(['unzip', 'a', '-d', '-'.join(i)])
    child.communicate()
    if child.returncode == 0:
        break
