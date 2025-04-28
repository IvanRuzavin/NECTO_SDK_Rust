/* memory.x - Linker script for the STM32F101T6 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 6K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 32K
}
