/* memory.x - Linker script for the STM32F100ZE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
