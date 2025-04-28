/* memory.x - Linker script for the STM32F334R6 */
MEMORY
{
  CCMRAM    : ORIGIN = 0x10000000,   LENGTH = 4K
  RAM    : ORIGIN = 0x20000000,   LENGTH = 12K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 32K
}
