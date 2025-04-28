/* memory.x - Linker script for the STM32F769IG */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 512K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 1024K
}
