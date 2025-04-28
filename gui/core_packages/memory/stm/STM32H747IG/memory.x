/* memory.x - Linker script for the STM32H747IG */
MEMORY
{
FLASH (rx)     : ORIGIN = 0x08100000, LENGTH = 512K
RAM (xrw)      : ORIGIN = 0x10000000, LENGTH = 288K
}
