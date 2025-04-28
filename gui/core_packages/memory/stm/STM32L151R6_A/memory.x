/* memory.x - Linker script for the STM32L151R6_A */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 16K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 32K
}
