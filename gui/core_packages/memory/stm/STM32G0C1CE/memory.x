/* memory.x - Linker script for the STM32G0C1CE */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 144K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 512K
}
