/* memory.x - Linker script for the STM32F103C4 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 6K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 16K
}
