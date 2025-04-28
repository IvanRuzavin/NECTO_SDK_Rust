/* memory.x - Linker script for the STM32F101VF */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 768K
}
