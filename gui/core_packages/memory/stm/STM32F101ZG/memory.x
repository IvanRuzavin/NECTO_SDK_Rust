/* memory.x - Linker script for the STM32F101ZG */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 1024K
}
