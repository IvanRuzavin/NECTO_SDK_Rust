/* memory.x - Linker script for the STM32F103RG */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 96K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 1024K
}
