/* memory.x - Linker script for the STM32H503EB */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 32K
  FLASH    (rx)    : ORIGIN = 0x08000000,   LENGTH = 128K
}
