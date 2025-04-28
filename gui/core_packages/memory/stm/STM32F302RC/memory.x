/* memory.x - Linker script for the STM32F302RC */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 40K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 256K
}
