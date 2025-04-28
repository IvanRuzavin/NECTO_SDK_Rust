/* memory.x - Linker script for the STM32F328C8 */
MEMORY
{
  CCMRAM    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 4K
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 12K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 64K
}
