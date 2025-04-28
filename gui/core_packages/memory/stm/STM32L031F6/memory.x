/* memory.x - Linker script for the STM32L031F6 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 8K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 32K
}
