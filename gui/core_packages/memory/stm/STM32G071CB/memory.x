/* memory.x - Linker script for the STM32G071CB */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 36K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 128K
}
