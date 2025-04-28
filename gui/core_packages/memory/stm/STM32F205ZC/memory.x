/* memory.x - Linker script for the STM32F205ZC */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 80K
  RAM2    : ORIGIN = 0x2001C000,   LENGTH = 16K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 256K
}
