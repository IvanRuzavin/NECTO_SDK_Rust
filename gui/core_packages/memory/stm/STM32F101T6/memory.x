/* memory.x - Linker script for the STM32F101T6 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 6K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 32K
}
