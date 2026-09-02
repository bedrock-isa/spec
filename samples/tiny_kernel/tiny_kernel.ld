ENTRY(_start)

SECTIONS
{
  . = 0x1000;

  .text : {
    __kernel_text_start = .;
    *(EXCLUDE_FILE (*shell.o *user_entry.o) .text .text.*)
    __kernel_text_end = .;
  }

  . = ALIGN(16384);
  .user_text : {
    __user_text_start = .;
    *shell.o(.text .text.*)
    *user_entry.o(.text .text.*)
    __user_text_end = .;
  }

  . = ALIGN(16384);
  .rodata : {
    __kernel_rodata_start = .;
    *(EXCLUDE_FILE (*shell.o) .rodata .rodata.*)
    __kernel_rodata_end = .;
  }

  . = ALIGN(16384);
  .user_rodata : {
    __user_rodata_start = .;
    *shell.o(.rodata .rodata.*)
    __user_rodata_end = .;
  }

  . = 0x28000;
  __kernel_data_start = .;
  .data : {
    *(.data .data.*)
  }
  .bss : {
    *(.bss .bss.* COMMON)
  }
  __kernel_data_end = .;

  . = ALIGN(16384);
  .tls : {
    __tls_start = .;
    *(.tdata .tdata.*)
    *(.tbss .tbss.*)
    __tls_end = .;
  }

  . = __tls_end;
  . = ALIGN(16384);
  .kernel_stack : {
    __kernel_stack_start = .;
    *(.kernel_stack)
    __kernel_stack_end = .;
  }

  . = ALIGN(16384);
  .user_stack : {
    __user_stack_start = .;
    *(.user_stack)
    __user_stack_end = .;
  }

  . = ALIGN(16384);
  .page_pool : {
    __page_pool_start = .;
    *(.page_pool)
    __page_pool_end = .;
  }

  ASSERT(__page_pool_end <= 0x100000,
         "tiny_kernel page pool exceeds the emulator RAM aperture")
}
