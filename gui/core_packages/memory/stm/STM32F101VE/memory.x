/* memory.x - Linker script for the STM32F101VE */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 48K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 512K
}
