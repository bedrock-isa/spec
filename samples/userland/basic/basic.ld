ENTRY(_start)

PHDRS
{
  text PT_LOAD FLAGS(5);
  data PT_LOAD FLAGS(6);
}

SECTIONS
{
  . = 0x00200000;

  .text : {
    *(.text .text.*)
  } :text

  . = ALIGN(16384);
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
