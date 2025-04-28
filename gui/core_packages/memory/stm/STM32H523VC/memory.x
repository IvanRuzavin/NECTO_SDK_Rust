/* memory.x - Linker script for the STM32H523VC */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 272K
  FLASH    (rx)    : ORIGIN = 0x08000000,   LENGTH = 256K
}
