/* memory.x - Linker script for the STM32L475RE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 96K
  RAM2    : ORIGIN = 0x10000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
