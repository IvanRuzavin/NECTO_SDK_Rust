/* memory.x - Linker script for the STM32L4A6ZG */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 320K
  RAM2    : ORIGIN = 0x10000000,   LENGTH = 64K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 1024K
}
