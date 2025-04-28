/* memory.x - Linker script for the STM32L011E4 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 2K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 16K
}
