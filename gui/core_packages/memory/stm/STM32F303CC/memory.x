/* memory.x - Linker script for the STM32F303CC */
MEMORY
{
  CCMRAM    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 8K
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 40K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 256K
}
