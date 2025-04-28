/* memory.x - Linker script for the STM32L4R5VI */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 640K
  RAM2    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 64K
  RAM3    (xrw)    : ORIGIN = 0x20040000,   LENGTH = 384K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 2048K
}
