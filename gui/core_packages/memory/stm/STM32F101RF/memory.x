/* memory.x - Linker script for the STM32F101RF */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 768K
}
