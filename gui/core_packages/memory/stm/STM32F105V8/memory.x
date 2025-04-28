/* memory.x - Linker script for the STM32F105V8 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 64K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 64K
}
