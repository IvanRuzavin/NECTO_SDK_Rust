/* memory.x - Linker script for the STM32L152VD_X */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 192K
  FLASH2    (rx)    : ORIGIN = 0x8040000,   LENGTH = 192K
}
