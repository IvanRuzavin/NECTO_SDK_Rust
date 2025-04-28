/* memory.x - Linker script for the STM32WLE5J8 */
MEMORY
{
  RAM2   (xrw)   : ORIGIN = 0x20008000, LENGTH = 20K
  FLASH   (rx)   : ORIGIN = 0x08000000, LENGTH = 64K
}
