/* memory.x - Linker script for the STM32F071RB */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 16K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 128K
}
