ENTRY(_start)

PHDRS
{
  text PT_LOAD FLAGS(5);
  data PT_LOAD FLAGS(6);
}

SECTIONS
{
  . = 0x00080000;

  .text : {
    *(.text .text.*)
  } :text

  . = ALIGN(4096);
  .rodata : {
    *(.rodata .rodata.*)
  } :data

  . = ALIGN(16);
  .data : {
    *(.data .data.*)
  } :data

  . = ALIGN(16);
  .bss : {
    *(.bss .bss.* COMMON)
  } :data
}
