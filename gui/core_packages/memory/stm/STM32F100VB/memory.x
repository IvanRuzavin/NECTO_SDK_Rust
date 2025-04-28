/* memory.x - Linker script for the STM32F100VB */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 8K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 128K
}
