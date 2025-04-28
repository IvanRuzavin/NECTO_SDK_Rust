/* memory.x - Linker script for the STM32F205VB */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 48K
  RAM2    (xrw)    : ORIGIN = 0x2001C000,   LENGTH = 16K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 128K
}
