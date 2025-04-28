/* memory.x - Linker script for the STM32L412K8 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 40K
  RAM2    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 8K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 64K
}
