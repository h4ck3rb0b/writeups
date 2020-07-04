# Thanos

Solution script is at `a.py`. Other files are in the folder.

When you open the given link you are greeted with this message:

> THANOS RULESSS!!!11  
> Oh no! You wouldn't believe this! Thanos got ALL of the infinity stones and DESTROYED them! what are we going to do?  
> Luckily for us STARK industries thought about this possibility and they engineered a version control device (VCS for short), through which they claim the infinity stones can be restored.  
> BUT  
> Thanos knew all about this technology... STARK industries are lost...  
> Can you help them?

VCS hints to stuff like `git`, so you try opening `http://ctf.cscml.zenysec.com:20030/.git/`
and you are greeted with a directory listing.

Let us download everything here: `wget -r -np http://ctf.cscml.zenysec.com:20030/.git/`

When you get in and run `git log`, there are no files in the repo. However, when
you run `git reflog`, you notice an interesting commit:
```
af7c13b HEAD@{...}: commit: BACKUP THE STONES
```

When we checkout to that commit (`git checkout af7c13b`) we get six files,
probably corresponding to the infinity stones.

Run `file` on all of them:
```
$ file *
mind:                data
power:               Zip archive data, at least v2.0 to extract
reality:             data
soul:                data
space:               data
time:                data
```

We see that there is a zip file. However, when we try to unzip `power` we get a
message saying that the zip file is corrupted.

This is where we guess that the files must be combined together. We try all
permutations of combining and try to unzip these files, which is shown in the
`a.py` file:
```python
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
```

Running this, you will get several folders which contain images. One of them
gives a proper image, which is `infinity-stones.png` as shown in this repo.
The flag is just there.
