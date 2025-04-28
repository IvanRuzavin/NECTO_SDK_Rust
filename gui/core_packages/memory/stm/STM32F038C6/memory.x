/* memory.x - Linker script for the STM32F038C6 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 4K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 32K
}
