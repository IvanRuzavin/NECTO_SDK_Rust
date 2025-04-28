/* memory.x - Linker script for the STM32F730Z8 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 256K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 64K
}
