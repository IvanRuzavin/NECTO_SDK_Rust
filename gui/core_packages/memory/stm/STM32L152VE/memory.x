/* memory.x - Linker script for the STM32L152VE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
