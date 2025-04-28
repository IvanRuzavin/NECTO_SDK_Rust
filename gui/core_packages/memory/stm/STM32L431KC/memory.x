/* memory.x - Linker script for the STM32L431KC */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 64K
  RAM2    : ORIGIN = 0x10000000,   LENGTH = 16K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 256K
}
