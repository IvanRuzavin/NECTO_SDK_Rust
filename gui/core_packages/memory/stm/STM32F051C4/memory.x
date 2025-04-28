/* memory.x - Linker script for the STM32F051C4 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 8K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 16K
}
