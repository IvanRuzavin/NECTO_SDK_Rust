/* memory.x - Linker script for the STM32L152C6 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 10K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 32K
}
