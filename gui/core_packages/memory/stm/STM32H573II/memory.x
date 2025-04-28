/* memory.x - Linker script for the STM32H573II */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 640K
  FLASH    (rx)    : ORIGIN = 0x08000000,   LENGTH = 2048K
}
