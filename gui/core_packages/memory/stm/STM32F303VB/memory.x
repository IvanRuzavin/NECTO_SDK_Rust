/* memory.x - Linker script for the STM32F303VB */
MEMORY
{
  CCMRAM    : ORIGIN = 0x10000000,   LENGTH = 8K
  RAM    : ORIGIN = 0x20000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 128K
}
