/* memory.x - Linker script for the STM32WLE4CB */
MEMORY
{
  RAM1   (xrw)   : ORIGIN = 0x20000000, LENGTH = 16K
  RAM2   (xrw)   : ORIGIN = 0x20008000, LENGTH = 32K
  FLASH   (rx)   : ORIGIN = 0x08000000, LENGTH = 128K
}
