/* memory.x - Linker script for the STM32U5G7VJ */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 3008K
  FLASH    (rx)    : ORIGIN = 0x08000000,   LENGTH = 4096K
}
