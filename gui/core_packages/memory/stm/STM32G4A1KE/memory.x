/* memory.x - Linker script for the STM32G4A1KE */
MEMORY
{
  RAM    (xrw)    : ORIGIN = 0x20000000,   LENGTH = 112K
  FLASH    (rx)    : ORIGIN = 0x8000000,   LENGTH = 512K
}
