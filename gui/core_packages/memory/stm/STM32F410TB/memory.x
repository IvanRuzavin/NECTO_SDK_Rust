/* memory.x - Linker script for the STM32F410TB */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 128K
}
