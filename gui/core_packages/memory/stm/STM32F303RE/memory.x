/* memory.x - Linker script for the STM32F303RE */
MEMORY
{
  CCMRAM    : ORIGIN = 0x10000000,   LENGTH = 16K
  RAM    : ORIGIN = 0x20000000,   LENGTH = 64K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
