/* memory.x - Linker script for the STM32L151RD */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 48K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 384K
}
