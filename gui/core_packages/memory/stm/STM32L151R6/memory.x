/* memory.x - Linker script for the STM32L151R6 */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 10K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 32K
}
