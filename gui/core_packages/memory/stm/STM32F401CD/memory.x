/* memory.x - Linker script for the STM32F401CD */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 96K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 384K
}
