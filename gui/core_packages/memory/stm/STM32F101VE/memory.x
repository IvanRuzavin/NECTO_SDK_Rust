/* memory.x - Linker script for the STM32F101VE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 48K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
