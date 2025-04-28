/* memory.x - Linker script for the STM32F767VI */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 512K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 2048K
}
