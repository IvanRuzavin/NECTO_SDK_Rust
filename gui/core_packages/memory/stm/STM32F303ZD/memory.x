/* memory.x - Linker script for the STM32F303ZD */
MEMORY
{
  CCMRAM    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 16K
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 64K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 384K
}
