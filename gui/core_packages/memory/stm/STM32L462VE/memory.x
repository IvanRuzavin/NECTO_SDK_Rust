/* memory.x - Linker script for the STM32L462VE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 160K
  RAM2    : ORIGIN = 0x10000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
