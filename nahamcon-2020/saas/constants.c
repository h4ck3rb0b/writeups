#include <asm/prctl.h>
#include <fcntl.h>
#include <stdio.h>
#include <sys/prctl.h>
#include <sys/stat.h>
#include <sys/types.h>

int main()
{
    printf("ARCH_SET_GS = 0x%x\n", ARCH_SET_GS);
    printf("ARCH_GET_GS = 0x%x\n", ARCH_GET_GS);
    printf("AT_FDCWD = 0x%x\n", AT_FDCWD);
    return 0;
}
