/* memory.x - Linker script for the STM32F302RE */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 64K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 512K
}
