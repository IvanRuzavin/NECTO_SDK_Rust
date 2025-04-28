/* memory.x - Linker script for the STM32WLE5JC */
MEMORY
{
  RAM    (xrw)   : ORIGIN = 0x20000000, LENGTH = 64K
  RAM2   (xrw)   : ORIGIN = 0x10000000, LENGTH = 32K
  FLASH   (rx)   : ORIGIN = 0x08000000, LENGTH = 256K
}
