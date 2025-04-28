/* memory.x - Linker script for the STM32F777ZI */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 512K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 2048K
}
