/* memory.x - Linker script for the STM32F207IC */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 112K
  RAM2    (xrw)    : ORIGIN = 0x2001C000,   LENGTH = 16K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 256K
}
