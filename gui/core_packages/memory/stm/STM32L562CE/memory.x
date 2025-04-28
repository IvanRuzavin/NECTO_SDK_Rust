/* memory.x - Linker script for the STM32L562CE */
MEMORY
{
  RAM	(xrw)	: ORIGIN = 0x20000000,	LENGTH = 192K
  RAM2	(xrw)	: ORIGIN = 0x20030000,	LENGTH = 64K
  FLASH	(rx)	: ORIGIN = 0x8000000,	LENGTH = 512K
}
