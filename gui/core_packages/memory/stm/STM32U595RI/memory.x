/* memory.x - Linker script for the STM32U595RI */
MEMORY
{
  RAM (xrw)   : ORIGIN = 0x20000000, LENGTH = 2496K
  SRAM4 (xrw) : ORIGIN = 0x28000000, LENGTH = 16K
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 2048K
}
