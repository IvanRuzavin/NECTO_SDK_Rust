/* memory.x - Linker script for the STM32U073H8 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 32K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 256K
}
