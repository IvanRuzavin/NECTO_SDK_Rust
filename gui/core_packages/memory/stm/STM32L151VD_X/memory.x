/* memory.x - Linker script for the STM32L151VD_X */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 80K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 192K
  FLASH2    : ORIGIN = 0x8040000,   LENGTH = 192K
}
