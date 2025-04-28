/* memory.x - Linker script for the STM32L4Q5CG */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 320K
  RAM2    (xrw)    : ORIGIN = 0x10000000,   LENGTH = 64K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 1024K
}
