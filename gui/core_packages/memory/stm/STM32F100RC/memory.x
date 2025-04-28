/* memory.x - Linker script for the STM32F100RC */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 24K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 256K
}
