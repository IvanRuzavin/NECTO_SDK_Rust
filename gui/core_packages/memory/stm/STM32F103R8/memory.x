/* memory.x - Linker script for the STM32F103R8 */
MEMORY
{
  RAM    : ORIGIN = 0x20000000,   LENGTH = 20K
  FLASH    : ORIGIN = 0x8000000,   LENGTH = 64K
}
