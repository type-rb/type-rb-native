.data
.balign 8
g4s482:
	.quad 0
	.quad 12
	.byte 80
	.byte 102
	.byte 97
	.byte 110
	.byte 110
	.byte 107
	.byte 117
	.byte 99
	.byte 104
	.byte 101
	.byte 110
	.byte 40
	.byte 0
/* end data */

.data
.balign 8
g4s490:
	.quad 0
	.quad 4
	.byte 41
	.byte 32
	.byte 61
	.byte 32
	.byte 0
/* end data */

.data
.balign 8
g4_desc_record0:
	.quad 1
	.quad 0
	.quad 16
/* end data */

.data
.balign 8
g4_newline:
	.byte 10
/* end data */

.bss
.balign 8
g4_character_cache:
	.fill 2048,1,0
/* end data */

.data
.balign 8
g4_string_storage:
	.quad 0
	.quad 0
	.quad 0
/* end data */

.data
.balign 8
g4_temporary_storage:
	.quad 0
	.quad 0
/* end data */

.data
.balign 8
g4_allocation_error:
	.byte 112
	.byte 97
	.byte 110
	.byte 105
	.byte 99
	.byte 58
	.byte 32
	.byte 97
	.byte 108
	.byte 108
	.byte 111
	.byte 99
	.byte 97
	.byte 116
	.byte 105
	.byte 111
	.byte 110
	.byte 32
	.byte 102
	.byte 97
	.byte 105
	.byte 108
	.byte 101
	.byte 100
	.byte 10
/* end data */

.data
.balign 8
g4_bounds_error:
	.byte 112
	.byte 97
	.byte 110
	.byte 105
	.byte 99
	.byte 58
	.byte 32
	.byte 105
	.byte 110
	.byte 100
	.byte 101
	.byte 120
	.byte 32
	.byte 105
	.byte 115
	.byte 32
	.byte 111
	.byte 117
	.byte 116
	.byte 32
	.byte 111
	.byte 102
	.byte 32
	.byte 98
	.byte 111
	.byte 117
	.byte 110
	.byte 100
	.byte 115
	.byte 10
/* end data */

.data
.balign 8
g4_integer_error:
	.byte 112
	.byte 97
	.byte 110
	.byte 105
	.byte 99
	.byte 58
	.byte 32
	.byte 73
	.byte 110
	.byte 116
	.byte 101
	.byte 103
	.byte 101
	.byte 114
	.byte 32
	.byte 111
	.byte 112
	.byte 101
	.byte 114
	.byte 97
	.byte 116
	.byte 105
	.byte 111
	.byte 110
	.byte 32
	.byte 102
	.byte 97
	.byte 105
	.byte 108
	.byte 101
	.byte 100
	.byte 10
/* end data */

.data
.balign 8
g4_integer_range_error:
	.ascii "panic: Integer is outside the portable range"
	.byte 10
/* end data */

.data
.balign 8
g4_division_error:
	.ascii "panic: division by zero"
	.byte 10
/* end data */

.data
.balign 8
g4_usage_error:
	.ascii "usage: compiler {check|emit-qbe} SOURCE"
	.byte 10
	.ascii "       compiler build SOURCE --output OUTPUT --qbe QBE --cc CC"
	.byte 10
/* end data */

.data
.balign 8
g4_file_error:
	.ascii "compiler: cannot read source file: "
/* end data */

.data
.balign 8
g4_check:
	.ascii "check"
	.byte 0
/* end data */

.data
.balign 8
g4_emit:
	.ascii "emit-qbe"
	.byte 0
/* end data */

.data
.balign 8
g4_build:
	.ascii "build"
	.byte 0
/* end data */

.data
.balign 8
g4_output_flag:
	.ascii "--output"
	.byte 0
/* end data */

.data
.balign 8
g4_qbe_flag:
	.ascii "--qbe"
	.byte 0
/* end data */

.data
.balign 8
g4_cc_flag:
	.ascii "--cc"
	.byte 0
/* end data */

.data
.balign 8
g4_target_option:
	.ascii "--target"
	.byte 0
/* end data */

.data
.balign 8
g4_source_arg:
	.ascii "--source-content"
	.byte 0
/* end data */

.data
.balign 8
g4_rb:
	.ascii "rb"
	.byte 0
/* end data */

.data
.balign 8
g4_wb:
	.ascii "wb"
	.byte 0
/* end data */

.data
.balign 8
g4_ssa_suffix:
	.ascii ".trbn.ssa"
	.byte 0
/* end data */

.data
.balign 8
g4_asm_suffix:
	.ascii ".trbn.s"
	.byte 0
/* end data */

.data
.balign 8
g4_temp_suffix:
	.ascii ".trbn.XXXXXX"
	.byte 0
/* end data */

.data
.balign 8
g4_slash:
	.ascii "/"
	.byte 0
/* end data */

.data
.balign 8
g4_target_flag:
	.ascii "-t"
	.byte 0
/* end data */

.data
.balign 8
g4_profile_darwin_arm64:
	.ascii "darwin-arm64-v0"
	.byte 0
/* end data */

.data
.balign 8
g4_profile_linux_arm64:
	.ascii "linux-arm64-v0"
	.byte 0
/* end data */

.data
.balign 8
g4_profile_linux_amd64:
	.ascii "linux-amd64-v0"
	.byte 0
/* end data */

.data
.balign 8
g4_qbe_darwin_arm64:
	.ascii "arm64_apple"
	.byte 0
/* end data */

.data
.balign 8
g4_qbe_linux_arm64:
	.ascii "arm64"
	.byte 0
/* end data */

.data
.balign 8
g4_qbe_linux_amd64:
	.ascii "amd64_sysv"
	.byte 0
/* end data */

.data
.balign 8
g4_o_flag:
	.ascii "-o"
	.byte 0
/* end data */

.data
.balign 8
g4_math_library:
	.ascii "-lm"
	.byte 0
/* end data */

.data
.balign 8
g4_dead_strip_darwin:
	.ascii "-Wl,-dead_strip,-x"
	.byte 0
/* end data */

.data
.balign 8
g4_dead_strip_linux:
	.ascii "-Wl,--gc-sections,--strip-all"
	.byte 0
/* end data */

.data
.balign 8
g4_selected_qbe_target:
	.quad g4_qbe_darwin_arm64+0
/* end data */

.data
.balign 8
g4_selected_dead_strip:
	.quad g4_dead_strip_darwin+0
/* end data */

.data
.balign 8
g4_target_error:
	.ascii "compiler: unsupported target profile"
	.byte 10
/* end data */

.data
.balign 8
g4_intermediate_error:
	.ascii "compiler: cannot create intermediate file"
	.byte 10
/* end data */

.data
.balign 8
g4_qbe_error:
	.ascii "compiler: qbe failed"
	.byte 10
/* end data */

.data
.balign 8
g4_cc_error:
	.ascii "compiler: cc failed"
	.byte 10
/* end data */

.data
.balign 8
g4_publish_error:
	.ascii "compiler: cannot publish output"
	.byte 10
/* end data */

.text
.balign 16
g4_fail:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x2, x1
	mov	x1, x0
	mov	w0, #2
	bl	write
	mov	w0, #2
	bl	exit
	brk	#1000
.type g4_fail, @function
.size g4_fail, .-g4_fail
/* end function g4_fail */

.text
.balign 16
g4_alloc:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, x0
	mov	x0, #1
	bl	calloc
	cmp	x0, #0
	bne	.L3
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.L3:
	ldp	x29, x30, [sp], 16
	ret
.type g4_alloc, @function
.size g4_alloc, .-g4_alloc
/* end function g4_alloc */

.text
.balign 16
g4_string_alloc:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, x0
	mov	x2, #0
	adrp	x0, g4_desc_string
	add	x0, x0, #:lo12:g4_desc_string
	bl	g4_gc_alloc
	ldp	x29, x30, [sp], 16
	ret
.type g4_string_alloc, @function
.size g4_string_alloc, .-g4_string_alloc
/* end function g4_string_alloc */

.text
.balign 16
g4_temp_alloc:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	x19, x0
	adrp	x0, g4_temporary_storage
	add	x0, x0, #:lo12:g4_temporary_storage
	ldr	x2, [x0]
	cmp	x2, #0
	bne	.L9
	mov	x1, #1048576
	mov	x0, #1
	bl	calloc
	mov	x2, x0
	cmp	x2, #0
	beq	.L13
	adrp	x0, g4_temporary_storage
	add	x0, x0, #:lo12:g4_temporary_storage
	str	x2, [x0]
.L9:
	adrp	x0, g4_temporary_storage+8
	add	x0, x0, #:lo12:g4_temporary_storage+8
	ldr	x0, [x0]
	mov	x1, #7
	add	x1, x19, x1
	mov	x3, #-8
	and	x1, x1, x3
	add	x1, x1, x0
	cmp	x1, #256, lsl #12
	bgt	.L12
	add	x0, x0, x2
	adrp	x2, g4_temporary_storage+8
	add	x2, x2, #:lo12:g4_temporary_storage+8
	str	x1, [x2]
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.L12:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.L13:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_temp_alloc, @function
.size g4_temp_alloc, .-g4_temp_alloc
/* end function g4_temp_alloc */

.text
.balign 16
g4_temp_reset:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	adrp	x1, g4_temporary_storage+8
	add	x1, x1, #:lo12:g4_temporary_storage+8
	mov	x0, #0
	str	x0, [x1]
	ldp	x29, x30, [sp], 16
	ret
.type g4_temp_reset, @function
.size g4_temp_reset, .-g4_temp_reset
/* end function g4_temp_reset */

.text
.balign 16
g4_string_from_c:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	mov	x20, x0
	mov	x0, x20
	bl	strlen
	mov	x19, x0
	mov	x0, #9
	add	x0, x19, x0
	bl	g4_string_alloc
	mov	x1, x20
	mov	x2, #8
	add	x2, x0, x2
	str	x19, [x2]
	mov	x2, #16
	add	x20, x0, x2
	mov	x2, x19
	mov	x21, x0
	mov	x0, x20
	bl	memcpy
	mov	x0, x21
	add	x2, x19, x20
	mov	w1, #0
	strb	w1, [x2]
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.type g4_string_from_c, @function
.size g4_string_from_c, .-g4_string_from_c
/* end function g4_string_from_c */

.text
.balign 16
g4_read_file:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	str	x22, [x29, 16]
	adrp	x1, g4_rb
	add	x1, x1, #:lo12:g4_rb
	bl	fopen
	cmp	x0, #0
	beq	.L25
	mov	w2, #2
	mov	x1, #0
	mov	x19, x0
	bl	fseek
	mov	w1, w0
	mov	x0, x19
	cmp	w1, #0
	bne	.L24
	mov	x19, x0
	bl	ftell
	mov	x17, x0
	mov	x0, x19
	mov	x19, x17
	cmp	x19, #0
	blt	.L24
	mov	w2, #0
	mov	x1, #0
	mov	x20, x0
	bl	fseek
	mov	w1, w0
	mov	x0, x20
	cmp	w1, #0
	bne	.L24
	mov	x20, x0
	mov	x0, #9
	add	x0, x19, x0
	bl	g4_string_alloc
	mov	x22, x0
	mov	x0, x20
	mov	x1, #8
	add	x1, x22, x1
	str	x19, [x1]
	mov	x1, #16
	add	x20, x22, x1
	mov	x3, x0
	mov	x2, x19
	mov	x1, #1
	mov	x21, x0
	mov	x0, x20
	bl	fread
	mov	x17, x0
	mov	x0, x21
	mov	x21, x17
	bl	fclose
	mov	w2, w0
	mov	x0, x22
	cmp	x21, x19
	cset	w1, ne
	cmp	w2, #0
	cset	w2, ne
	orr	w1, w1, w2
	cmp	w1, #0
	bne	.L25
	add	x2, x19, x20
	mov	w1, #0
	strb	w1, [x2]
	adrp	x1, g4_gc_global_roots+8
	add	x1, x1, #:lo12:g4_gc_global_roots+8
	str	x0, [x1]
	b	.L26
.L24:
	bl	fclose
.L25:
	mov	x0, #0
.L26:
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldr	x22, [x29, 16]
	ldp	x29, x30, [sp], 48
	ret
.type g4_read_file, @function
.size g4_read_file, .-g4_read_file
/* end function g4_read_file */

.text
.balign 16
g4_file_exists:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, #16
	add	x0, x0, x1
	mov	w1, #0
	bl	access
	cmp	w0, #0
	cset	w0, eq
	mov	w0, w0
	ldp	x29, x30, [sp], 16
	ret
.type g4_file_exists, @function
.size g4_file_exists, .-g4_file_exists
/* end function g4_file_exists */

.text
.balign 16
g4_read_source:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, #16
	add	x0, x0, x1
	bl	g4_read_file
	ldp	x29, x30, [sp], 16
	ret
.type g4_read_source, @function
.size g4_read_source, .-g4_read_source
/* end function g4_read_source */

.text
.balign 16
g4_run:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	str	x20, [x29, 16]
	mov	x20, x1
	mov	x19, x0
	bl	fork
	mov	x1, x20
	cmp	w0, #0
	blt	.L40
	cmp	w0, #0
	beq	.L38
	mov	x1, #16
	sub	sp, sp, x1
	mov	x19, sp
	mov	w1, #0
	str	w1, [x19]
	mov	w2, #0
	mov	x1, x19
	bl	waitpid
	cmp	w0, #0
	blt	.L40
	ldr	w0, [x19]
	mov	w1, #127
	and	w1, w0, w1
	cmp	w1, #0
	bne	.L36
	mov	w1, #8
	lsr	w0, w0, w1
	mov	w1, #255
	and	w0, w0, w1
	b	.L41
.L36:
	mov	w0, w1
	mov	w1, #128
	add	w0, w0, w1
	b	.L41
.L38:
	mov	x0, x19
	bl	execv
	mov	w0, #127
	bl	exit
	brk	#1000
.L40:
	mov	w0, #127
.L41:
	ldr	x19, [x29, 24]
	ldr	x20, [x29, 16]
	mov sp, x29
	ldp	x29, x30, [sp], 32
	ret
.type g4_run, @function
.size g4_run, .-g4_run
/* end function g4_run */

.text
.balign 16
g4_run_qbe:
	hint	#34
	stp	x29, x30, [sp, -80]!
	mov	x29, sp
	adrp	x3, g4_selected_qbe_target
	add	x3, x3, #:lo12:g4_selected_qbe_target
	ldr	x3, [x3]
	add	x4, x29, #24
	str	x0, [x4]
	mov	x5, #8
	add	x4, x29, #24
	add	x5, x4, x5
	adrp	x4, g4_target_flag
	add	x4, x4, #:lo12:g4_target_flag
	str	x4, [x5]
	mov	x5, #16
	add	x4, x29, #24
	add	x4, x4, x5
	str	x3, [x4]
	mov	x4, #24
	add	x3, x29, #24
	add	x4, x3, x4
	adrp	x3, g4_o_flag
	add	x3, x3, #:lo12:g4_o_flag
	str	x3, [x4]
	mov	x4, #32
	add	x3, x29, #24
	add	x3, x3, x4
	str	x2, [x3]
	mov	x3, #40
	add	x2, x29, #24
	add	x2, x2, x3
	str	x1, [x2]
	mov	x2, #48
	add	x1, x29, #24
	add	x2, x1, x2
	mov	x1, #0
	str	x1, [x2]
	add	x1, x29, #24
	bl	g4_run
	ldp	x29, x30, [sp], 80
	ret
.type g4_run_qbe, @function
.size g4_run_qbe, .-g4_run_qbe
/* end function g4_run_qbe */

.text
.balign 16
g4_run_cc:
	hint	#34
	stp	x29, x30, [sp, -80]!
	mov	x29, sp
	mov	x3, x1
	adrp	x1, g4_selected_dead_strip
	add	x1, x1, #:lo12:g4_selected_dead_strip
	ldr	x1, [x1]
	add	x4, x29, #24
	str	x0, [x4]
	mov	x5, #8
	add	x4, x29, #24
	add	x4, x4, x5
	str	x3, [x4]
	mov	x4, #16
	add	x3, x29, #24
	add	x3, x3, x4
	str	x1, [x3]
	mov	x3, #24
	add	x1, x29, #24
	add	x3, x1, x3
	adrp	x1, g4_math_library
	add	x1, x1, #:lo12:g4_math_library
	str	x1, [x3]
	mov	x3, #32
	add	x1, x29, #24
	add	x3, x1, x3
	adrp	x1, g4_o_flag
	add	x1, x1, #:lo12:g4_o_flag
	str	x1, [x3]
	mov	x3, #40
	add	x1, x29, #24
	add	x1, x1, x3
	str	x2, [x1]
	mov	x2, #48
	add	x1, x29, #24
	add	x2, x1, x2
	mov	x1, #0
	str	x1, [x2]
	add	x1, x29, #24
	bl	g4_run
	ldp	x29, x30, [sp], 80
	ret
.type g4_run_cc, @function
.size g4_run_cc, .-g4_run_cc
/* end function g4_run_cc */

.text
.balign 16
g4_cleanup:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	x19, x1
	bl	unlink
	mov	x0, x19
	bl	unlink
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_cleanup, @function
.size g4_cleanup, .-g4_cleanup
/* end function g4_cleanup */

.text
.balign 16
g4_cleanup_output:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	x19, x1
	bl	unlink
	mov	x0, x19
	bl	rmdir
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_cleanup_output, @function
.size g4_cleanup_output, .-g4_cleanup_output
/* end function g4_cleanup_output */

.text
.balign 16
g4_string_concat:
	hint	#34
	stp	x29, x30, [sp, -64]!
	mov	x29, sp
	str	x19, [x29, 56]
	str	x20, [x29, 48]
	str	x21, [x29, 40]
	str	x22, [x29, 32]
	str	x23, [x29, 24]
	str	x24, [x29, 16]
	mov	x21, x0
	mov	x0, #8
	mov	x20, x1
	add	x1, x21, x0
	mov	x0, #8
	add	x0, x20, x0
	ldr	x22, [x1]
	ldr	x23, [x0]
	add	x19, x22, x23
	mov	x0, #9
	add	x0, x19, x0
	bl	g4_string_alloc
	mov	x2, x23
	mov	x1, x20
	mov	x3, #8
	add	x3, x0, x3
	str	x19, [x3]
	mov	x3, #16
	add	x20, x0, x3
	mov	x23, x1
	mov	x1, #16
	add	x1, x21, x1
	mov	x24, x2
	mov	x2, x22
	mov	x21, x0
	mov	x0, x20
	bl	memcpy
	mov	x2, x24
	mov	x1, x23
	mov	x0, x21
	mov	x21, x0
	add	x0, x22, x20
	mov	x3, #16
	add	x1, x1, x3
	bl	memcpy
	mov	x0, x21
	add	x2, x19, x20
	mov	w1, #0
	strb	w1, [x2]
	ldr	x19, [x29, 56]
	ldr	x20, [x29, 48]
	ldr	x21, [x29, 40]
	ldr	x22, [x29, 32]
	ldr	x23, [x29, 24]
	ldr	x24, [x29, 16]
	ldp	x29, x30, [sp], 64
	ret
.type g4_string_concat, @function
.size g4_string_concat, .-g4_string_concat
/* end function g4_string_concat */

.text
.balign 16
g4_string_equal:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x2, #8
	add	x2, x0, x2
	mov	x3, #8
	add	x3, x1, x3
	ldr	x2, [x2]
	ldr	x3, [x3]
	cmp	x2, x3
	beq	.L54
	mov	x0, #0
	b	.L55
.L54:
	mov	x3, #16
	add	x0, x0, x3
	mov	x3, #16
	add	x1, x1, x3
	bl	memcmp
	cmp	w0, #0
	cset	w0, eq
	mov	w0, w0
.L55:
	ldp	x29, x30, [sp], 16
	ret
.type g4_string_equal, @function
.size g4_string_equal, .-g4_string_equal
/* end function g4_string_equal */

.text
.balign 16
g4_string_index:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	x2, #8
	add	x2, x0, x2
	ldr	x3, [x2]
	cmp	x1, #0
	bge	.L58
	add	x1, x1, x3
.L58:
	cmp	x1, #0
	cset	w2, lt
	cmp	x3, x1
	cset	w3, le
	orr	w2, w2, w3
	cmp	w2, #0
	bne	.L61
	mov	x2, #16
	add	x0, x0, x2
	add	x0, x1, x0
	ldrb	w19, [x0]
	mov	x0, #10
	bl	g4_string_alloc
	mov	x1, #8
	add	x2, x0, x1
	mov	x1, #1
	str	x1, [x2]
	mov	x1, #16
	add	x1, x0, x1
	strb	w19, [x1]
	mov	x1, #17
	add	x2, x0, x1
	mov	w1, #0
	strb	w1, [x2]
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.L61:
	mov	x1, #30
	adrp	x0, g4_bounds_error
	add	x0, x0, #:lo12:g4_bounds_error
	bl	g4_fail
	brk	#1000
.type g4_string_index, @function
.size g4_string_index, .-g4_string_index
/* end function g4_string_index */

.text
.balign 16
g4_puts:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, #8
	add	x1, x0, x1
	ldr	x2, [x1]
	mov	x1, #16
	add	x1, x0, x1
	mov	w0, #1
	bl	write
	mov	x2, #1
	adrp	x1, g4_newline
	add	x1, x1, #:lo12:g4_newline
	mov	w0, #1
	bl	write
	ldp	x29, x30, [sp], 16
	ret
.type g4_puts, @function
.size g4_puts, .-g4_puts
/* end function g4_puts */

.text
.balign 16
g4_eputs:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, #8
	add	x1, x0, x1
	ldr	x2, [x1]
	mov	x1, #16
	add	x1, x0, x1
	mov	w0, #2
	bl	write
	mov	x2, #1
	adrp	x1, g4_newline
	add	x1, x1, #:lo12:g4_newline
	mov	w0, #2
	bl	write
	ldp	x29, x30, [sp], 16
	ret
.type g4_eputs, @function
.size g4_eputs, .-g4_eputs
/* end function g4_eputs */

.text
.balign 16
g4_array_new:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	str	x20, [x29, 16]
	mov	x2, #32
	mov	x1, #24
	bl	g4_gc_alloc
	mov	x1, #8
	mov	x19, x0
	mov	x0, #4
	bl	calloc
	mov	x17, x0
	mov	x0, x19
	mov	x19, x17
	cmp	x19, #0
	beq	.L69
	mov	x20, x0
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x0, [x0]
	mov	x1, #32
	add	x0, x0, x1
	adrp	x1, g4_gc_heap_bytes
	add	x1, x1, #:lo12:g4_gc_heap_bytes
	str	x0, [x1]
	adrp	x1, g4_gc_allocated_bytes
	add	x1, x1, #:lo12:g4_gc_allocated_bytes
	ldr	x1, [x1]
	mov	x2, #32
	add	x1, x1, x2
	adrp	x2, g4_gc_allocated_bytes
	add	x2, x2, #:lo12:g4_gc_allocated_bytes
	str	x1, [x2]
	bl	g4_gc_update_peak
	mov	x0, x20
	mov	x1, #8
	add	x2, x0, x1
	mov	x1, #0
	str	x1, [x2]
	mov	x1, #16
	add	x2, x0, x1
	mov	x1, #4
	str	x1, [x2]
	mov	x1, #24
	add	x1, x0, x1
	str	x19, [x1]
	ldr	x19, [x29, 24]
	ldr	x20, [x29, 16]
	ldp	x29, x30, [sp], 32
	ret
.L69:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_array_new, @function
.size g4_array_new, .-g4_array_new
/* end function g4_array_new */

.text
.balign 16
g4_array_push:
	hint	#34
	stp	x29, x30, [sp, -64]!
	mov	x29, sp
	str	x19, [x29, 56]
	str	x20, [x29, 48]
	str	x21, [x29, 40]
	str	x22, [x29, 32]
	str	x23, [x29, 24]
	str	x24, [x29, 16]
	mov	x19, x0
	mov	x0, #8
	add	x0, x19, x0
	ldr	x20, [x0]
	mov	x0, #16
	add	x0, x19, x0
	ldr	x24, [x0]
	cmp	x20, x24
	bne	.L73
	mov	x0, #2
	mul	x22, x24, x0
	mov	x0, #8
	mul	x23, x22, x0
	mov	x0, #24
	add	x0, x19, x0
	ldr	x0, [x0]
	mov	x21, x1
	mov	x1, x23
	bl	realloc
	mov	x1, x21
	mov	x21, x0
	cmp	x21, #0
	beq	.L75
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x0, [x0]
	mov	x2, #8
	mul	x2, x24, x2
	sub	x2, x23, x2
	add	x0, x0, x2
	adrp	x3, g4_gc_heap_bytes
	add	x3, x3, #:lo12:g4_gc_heap_bytes
	str	x0, [x3]
	mov	x23, x1
	adrp	x1, g4_gc_allocated_bytes
	add	x1, x1, #:lo12:g4_gc_allocated_bytes
	ldr	x1, [x1]
	add	x1, x1, x2
	adrp	x2, g4_gc_allocated_bytes
	add	x2, x2, #:lo12:g4_gc_allocated_bytes
	str	x1, [x2]
	bl	g4_gc_update_peak
	mov	x1, x23
	mov	x0, #16
	add	x0, x19, x0
	str	x22, [x0]
	mov	x0, #24
	add	x0, x19, x0
	str	x21, [x0]
.L73:
	mov	x0, #24
	add	x0, x19, x0
	ldr	x0, [x0]
	mov	x2, #8
	mul	x2, x20, x2
	add	x0, x0, x2
	str	x1, [x0]
	mov	x0, #1
	add	x0, x20, x0
	mov	x1, #8
	add	x1, x19, x1
	str	x0, [x1]
	ldr	x19, [x29, 56]
	ldr	x20, [x29, 48]
	ldr	x21, [x29, 40]
	ldr	x22, [x29, 32]
	ldr	x23, [x29, 24]
	ldr	x24, [x29, 16]
	ldp	x29, x30, [sp], 64
	ret
.L75:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_array_push, @function
.size g4_array_push, .-g4_array_push
/* end function g4_array_push */

.text
.balign 16
g4_integer_add:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	add	x2, x0, x1
	mov	x3, #9007199254740991
	cmp	x2, x3
	bgt	.L80
	mov	x3, #-9007199254740991
	cmp	x2, x3
	blt	.L80
	add	x0, x0, x1
	ldp	x29, x30, [sp], 16
	ret
.L80:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.type g4_integer_add, @function
.size g4_integer_add, .-g4_integer_add
/* end function g4_integer_add */

.text
.balign 16
g4_integer_subtract:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	sub	x2, x0, x1
	mov	x3, #9007199254740991
	cmp	x2, x3
	bgt	.L85
	mov	x3, #-9007199254740991
	cmp	x2, x3
	blt	.L85
	sub	x0, x0, x1
	ldp	x29, x30, [sp], 16
	ret
.L85:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.type g4_integer_subtract, @function
.size g4_integer_subtract, .-g4_integer_subtract
/* end function g4_integer_subtract */

.text
.balign 16
g4_integer_multiply:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	cmp	x0, #0
	beq	.L98
	cmp	x1, #0
	cmp	x1, #0
	cmp	x0, #0
	bgt	.L92
	cmp	x1, #0
	bgt	.L91
	cmp	x1, #0
	beq	.L98
	mov	x2, #9007199254740991
	sdiv	x2, x2, x1
	cmp	x0, x2
	bge	.L96
	b	.L97
.L91:
	mov	x2, #-9007199254740991
	sdiv	x2, x2, x1
	cmp	x0, x2
	bge	.L96
	b	.L97
.L92:
	cmp	x1, #0
	bgt	.L95
	cmp	x1, #0
	beq	.L98
	mov	x2, #-9007199254740991
	sdiv	x2, x2, x0
	cmp	x1, x2
	bge	.L96
	b	.L97
.L95:
	mov	x2, #9007199254740991
	sdiv	x2, x2, x1
	cmp	x0, x2
	bgt	.L97
.L96:
	mul	x0, x0, x1
	b	.L99
.L97:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L98:
	mov	x0, #0
.L99:
	ldp	x29, x30, [sp], 16
	ret
.type g4_integer_multiply, @function
.size g4_integer_multiply, .-g4_integer_multiply
/* end function g4_integer_multiply */

.text
.balign 16
g4_integer_divide:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	cmp	x1, #0
	beq	.L103
	sdiv	x0, x0, x1
	ldp	x29, x30, [sp], 16
	ret
.L103:
	mov	x1, #24
	adrp	x0, g4_division_error
	add	x0, x0, #:lo12:g4_division_error
	bl	g4_fail
	brk	#1000
.type g4_integer_divide, @function
.size g4_integer_divide, .-g4_integer_divide
/* end function g4_integer_divide */

.text
.balign 16
g4_integer_remainder:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	cmp	x1, #0
	beq	.L107
	sdiv	x17, x0, x1
	msub	x0, x17, x1, x0
	ldp	x29, x30, [sp], 16
	ret
.L107:
	mov	x1, #24
	adrp	x0, g4_division_error
	add	x0, x0, #:lo12:g4_division_error
	bl	g4_fail
	brk	#1000
.type g4_integer_remainder, @function
.size g4_integer_remainder, .-g4_integer_remainder
/* end function g4_integer_remainder */

.data
.balign 8
g4_gc_heap:
	.quad 0
/* end data */

.bss
.balign 8
g4_gc_global_roots:
	.fill 96,1,0
/* end data */

.data
.balign 8
g4_gc_temp_data:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_temp_count:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_temp_capacity:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_heap_bytes:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_heap_target:
	.quad 1048576
/* end data */

.data
.balign 8
g4_gc_collection_count:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_automatic_collection_count:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_allocated_bytes:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_reclaimed_bytes:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_peak_heap_bytes:
	.quad 0
/* end data */

.data
.balign 8
g4_gc_trace_enabled:
	.quad 0
/* end data */

.data
.balign 8
g4_desc_string:
	.quad 0
/* end data */

.data
.balign 8
g4_desc_array_scalar:
	.quad 2
	.quad 0
/* end data */

.data
.balign 8
g4_desc_array_managed:
	.quad 2
	.quad 1
/* end data */

.data
.balign 8
g4_desc_project_sources:
	.quad 1
	.quad 3
	.quad 24
	.quad 8
	.quad 16
	.quad 24
/* end data */

.data
.balign 8
g4_gc_stats_environment:
	.ascii "TYPE_RB_NATIVE_RUNTIME_STATS"
	.byte 0
/* end data */

.data
.balign 8
g4_gc_trace_environment:
	.ascii "TYPE_RB_NATIVE_RUNTIME_TRACE"
	.byte 0
/* end data */

.data
.balign 8
g4_gc_trace_collection:
	.ascii "type-rb-native-gc-trace-v1,collection,"
/* end data */

.data
.balign 8
g4_gc_trace_automatic:
	.ascii "type-rb-native-gc-trace-v1,automatic,"
/* end data */

.data
.balign 8
g4_gc_trace_live:
	.ascii "type-rb-native-gc-trace-v1,live-bytes,"
/* end data */

.data
.balign 8
g4_gc_trace_target:
	.ascii "type-rb-native-gc-trace-v1,next-target-bytes,"
/* end data */

.data
.balign 8
g4_gc_trace_roots:
	.ascii "type-rb-native-gc-trace-v1,root-count,"
/* end data */

.data
.balign 8
g4_gc_trace_capacity:
	.ascii "type-rb-native-gc-trace-v1,root-capacity,"
/* end data */

.data
.balign 8
g4_gc_report_collections:
	.ascii "type-rb-native-gc-stat-v1,collections,"
/* end data */

.data
.balign 8
g4_gc_report_automatic:
	.ascii "type-rb-native-gc-stat-v1,automatic-collections,"
/* end data */

.data
.balign 8
g4_gc_report_allocated:
	.ascii "type-rb-native-gc-stat-v1,allocated-bytes,"
/* end data */

.data
.balign 8
g4_gc_report_reclaimed:
	.ascii "type-rb-native-gc-stat-v1,reclaimed-bytes,"
/* end data */

.data
.balign 8
g4_gc_report_live:
	.ascii "type-rb-native-gc-stat-v1,live-bytes,"
/* end data */

.data
.balign 8
g4_gc_report_peak:
	.ascii "type-rb-native-gc-stat-v1,peak-heap-bytes,"
/* end data */

.text
.balign 16
g4_gc_update_peak:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	adrp	x1, g4_gc_peak_heap_bytes
	add	x1, x1, #:lo12:g4_gc_peak_heap_bytes
	ldr	x1, [x1]
	cmp	x0, x1
	ble	.L110
	adrp	x1, g4_gc_peak_heap_bytes
	add	x1, x1, #:lo12:g4_gc_peak_heap_bytes
	str	x0, [x1]
.L110:
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_update_peak, @function
.size g4_gc_update_peak, .-g4_gc_update_peak
/* end function g4_gc_update_peak */

.text
.balign 16
g4_gc_maybe_collect:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	adrp	x1, g4_gc_heap_bytes
	add	x1, x1, #:lo12:g4_gc_heap_bytes
	ldr	x1, [x1]
	add	x0, x0, x1
	adrp	x1, g4_gc_heap_target
	add	x1, x1, #:lo12:g4_gc_heap_target
	ldr	x1, [x1]
	cmp	x0, x1
	ble	.L113
	mov	w0, #1
	bl	g4_gc_collect
.L113:
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_maybe_collect, @function
.size g4_gc_maybe_collect, .-g4_gc_maybe_collect
/* end function g4_gc_maybe_collect */

.text
.balign 16
g4_gc_temp_push:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	cmp	x0, #0
	beq	.L119
	ldr	x1, [x0]
	cmp	x1, #0
	beq	.L119
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	ldr	x1, [x1]
	adrp	x2, g4_gc_temp_capacity
	add	x2, x2, #:lo12:g4_gc_temp_capacity
	ldr	x2, [x2]
	cmp	x1, x2
	beq	.L118
	adrp	x2, g4_gc_temp_data
	add	x2, x2, #:lo12:g4_gc_temp_data
	ldr	x2, [x2]
	mov	w3, #3
	lsl	x3, x1, x3
	add	x2, x2, x3
	str	x0, [x2]
	mov	x0, #1
	add	x0, x1, x0
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x0, [x1]
	b	.L119
.L118:
	bl	g4_gc_temp_grow
.L119:
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_temp_push, @function
.size g4_gc_temp_push, .-g4_gc_temp_push
/* end function g4_gc_temp_push */

.text
.balign 16
g4_gc_temp_grow:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	cmp	x2, #0
	beq	.L122
	mov	x3, #2
	mul	x19, x2, x3
	b	.L123
.L122:
	mov	x19, #64
.L123:
	mov	x21, x1
	mov	x1, #8
	mul	x1, x19, x1
	mov	x20, x0
	adrp	x0, g4_gc_temp_data
	add	x0, x0, #:lo12:g4_gc_temp_data
	ldr	x0, [x0]
	bl	realloc
	mov	x1, x21
	mov	x3, x0
	mov	x0, x20
	cmp	x3, #0
	beq	.L126
	adrp	x2, g4_gc_temp_data
	add	x2, x2, #:lo12:g4_gc_temp_data
	str	x3, [x2]
	adrp	x2, g4_gc_temp_capacity
	add	x2, x2, #:lo12:g4_gc_temp_capacity
	str	x19, [x2]
	mov	x2, #8
	mul	x2, x1, x2
	add	x2, x2, x3
	str	x0, [x2]
	mov	x0, #1
	add	x0, x1, x0
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x0, [x1]
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.L126:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_gc_temp_grow, @function
.size g4_gc_temp_grow, .-g4_gc_temp_grow
/* end function g4_gc_temp_grow */

.text
.balign 16
g4_gc_temp_reset:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x0, [x1]
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_temp_reset, @function
.size g4_gc_temp_reset, .-g4_gc_temp_reset
/* end function g4_gc_temp_reset */

.text
.balign 16
g4_gc_alloc:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	mov	x19, x1
	mov	x20, x0
	mov	x0, #16
	add	x21, x19, x0
	add	x0, x2, x21
	bl	g4_gc_maybe_collect
	mov	x0, x21
	bl	malloc
	mov	x2, x19
	mov	x19, x0
	cmp	x19, #0
	beq	.L132
	adrp	x0, g4_gc_heap
	add	x0, x0, #:lo12:g4_gc_heap
	ldr	x0, [x0]
	str	x0, [x19]
	mov	x0, #8
	add	x0, x19, x0
	str	x20, [x0]
	mov	x20, x0
	mov	x0, #16
	add	x0, x19, x0
	mov	w1, #0
	bl	memset
	mov	x0, x20
	mov	x20, x0
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x0, [x0]
	add	x0, x21, x0
	adrp	x1, g4_gc_heap_bytes
	add	x1, x1, #:lo12:g4_gc_heap_bytes
	str	x0, [x1]
	adrp	x1, g4_gc_allocated_bytes
	add	x1, x1, #:lo12:g4_gc_allocated_bytes
	ldr	x1, [x1]
	add	x1, x21, x1
	adrp	x2, g4_gc_allocated_bytes
	add	x2, x2, #:lo12:g4_gc_allocated_bytes
	str	x1, [x2]
	bl	g4_gc_update_peak
	mov	x0, x20
	adrp	x1, g4_gc_heap
	add	x1, x1, #:lo12:g4_gc_heap
	str	x19, [x1]
	mov	x19, x0
	bl	g4_gc_temp_push
	mov	x0, x19
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.L132:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_gc_alloc, @function
.size g4_gc_alloc, .-g4_gc_alloc
/* end function g4_gc_alloc */

.text
.balign 16
g4_gc_scan_fixed:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	str	x22, [x29, 16]
	mov	x2, #8
	add	x2, x1, x2
	ldr	x20, [x2]
	mov	x2, #24
	add	x21, x1, x2
	mov	x19, #0
.L135:
	cmp	x20, x19
	ble	.L137
	mov	x22, x0
	mov	x0, #8
	mul	x0, x19, x0
	add	x0, x0, x21
	ldr	x0, [x0]
	add	x0, x22, x0
	ldr	x0, [x0]
	bl	g4_gc_mark
	mov	x0, x22
	mov	x1, #1
	add	x19, x19, x1
	b	.L135
.L137:
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldr	x22, [x29, 16]
	ldp	x29, x30, [sp], 48
	ret
.type g4_gc_scan_fixed, @function
.size g4_gc_scan_fixed, .-g4_gc_scan_fixed
/* end function g4_gc_scan_fixed */

.text
.balign 16
g4_gc_scan_array:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	mov	x2, #8
	add	x1, x1, x2
	ldr	x1, [x1]
	cmp	x1, #0
	beq	.L143
	mov	x1, #8
	add	x1, x0, x1
	ldr	x20, [x1]
	mov	x1, #24
	add	x0, x0, x1
	ldr	x21, [x0]
	mov	x19, #0
.L141:
	cmp	x20, x19
	ble	.L143
	mov	x0, #8
	mul	x0, x19, x0
	add	x0, x0, x21
	ldr	x0, [x0]
	bl	g4_gc_mark
	mov	x0, #1
	add	x19, x19, x0
	b	.L141
.L143:
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.type g4_gc_scan_array, @function
.size g4_gc_scan_array, .-g4_gc_scan_array
/* end function g4_gc_scan_array */

.text
.balign 16
g4_gc_mark:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	cmp	x0, #0
	beq	.L151
	ldr	x1, [x0]
	cmp	x1, #0
	beq	.L151
	mov	x2, #1
	and	x2, x1, x2
	cmp	x2, #0
	bne	.L151
	mov	x2, #1
	orr	x2, x1, x2
	str	x2, [x0]
	mov	x2, #-2
	and	x1, x1, x2
	ldr	x2, [x1]
	cmp	x2, #1
	beq	.L150
	cmp	x2, #2
	bne	.L151
	bl	g4_gc_scan_array
	b	.L151
.L150:
	bl	g4_gc_scan_fixed
.L151:
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_mark, @function
.size g4_gc_mark, .-g4_gc_mark
/* end function g4_gc_mark */

.text
.balign 16
g4_gc_mark_roots:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	adrp	x0, g4_gc_temp_count
	add	x0, x0, #:lo12:g4_gc_temp_count
	ldr	x20, [x0]
	adrp	x0, g4_gc_temp_data
	add	x0, x0, #:lo12:g4_gc_temp_data
	ldr	x21, [x0]
	mov	x19, #0
.L154:
	cmp	x20, x19
	ble	.L156
	mov	x0, #8
	mul	x0, x19, x0
	add	x0, x21, x0
	ldr	x0, [x0]
	bl	g4_gc_mark
	mov	x0, #1
	add	x19, x19, x0
	b	.L154
.L156:
	mov	x19, #0
.L157:
	cmp	x19, #12
	bge	.L159
	mov	x0, #8
	mul	x0, x19, x0
	adrp	x1, g4_gc_global_roots
	add	x1, x1, #:lo12:g4_gc_global_roots
	add	x0, x0, x1
	ldr	x0, [x0]
	bl	g4_gc_mark
	mov	x0, #1
	add	x19, x19, x0
	b	.L157
.L159:
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.type g4_gc_mark_roots, @function
.size g4_gc_mark_roots, .-g4_gc_mark_roots
/* end function g4_gc_mark_roots */

.text
.balign 16
g4_gc_sweep:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	adrp	x0, g4_gc_heap
	add	x0, x0, #:lo12:g4_gc_heap
	ldr	x19, [x0]
	mov	x20, #0
	mov	x21, x19
.L162:
	mov	x19, x20
	cmp	x21, #0
	beq	.L178
	mov	x20, x19
	ldr	x19, [x21]
	mov	x0, #8
	add	x0, x21, x0
	ldr	x1, [x0]
	mov	x0, #1
	and	x2, x1, x0
	mov	x0, #-2
	and	x0, x1, x0
	cmp	x2, #0
	bne	.L175
	mov	x2, #-2
	and	x1, x1, x2
	ldr	x1, [x1]
	cmp	x1, #2
	beq	.L168
	cmp	x1, #1
	beq	.L167
	mov	x0, #16
	add	x0, x21, x0
	ldr	x0, [x0]
	mov	x1, #25
	add	x0, x0, x1
	b	.L171
.L167:
	mov	x1, #16
	add	x0, x0, x1
	ldr	x0, [x0]
	mov	x1, #16
	add	x0, x0, x1
	b	.L171
.L168:
	mov	x0, #32
	add	x0, x21, x0
	ldr	x0, [x0]
	mov	x1, #24
	add	x1, x21, x1
	ldr	x1, [x1]
	mov	x2, #8
	mul	x1, x1, x2
	adrp	x2, g4_gc_heap_bytes
	add	x2, x2, #:lo12:g4_gc_heap_bytes
	ldr	x2, [x2]
	sub	x2, x2, x1
	adrp	x3, g4_gc_heap_bytes
	add	x3, x3, #:lo12:g4_gc_heap_bytes
	str	x2, [x3]
	adrp	x2, g4_gc_reclaimed_bytes
	add	x2, x2, #:lo12:g4_gc_reclaimed_bytes
	ldr	x2, [x2]
	add	x1, x1, x2
	adrp	x2, g4_gc_reclaimed_bytes
	add	x2, x2, #:lo12:g4_gc_reclaimed_bytes
	str	x1, [x2]
	cmp	x0, #0
	beq	.L170
	bl	free
.L170:
	mov	x0, #40
.L171:
	cmp	x20, #0
	beq	.L173
	str	x19, [x20]
	b	.L174
.L173:
	adrp	x1, g4_gc_heap
	add	x1, x1, #:lo12:g4_gc_heap
	str	x19, [x1]
.L174:
	adrp	x1, g4_gc_heap_bytes
	add	x1, x1, #:lo12:g4_gc_heap_bytes
	ldr	x1, [x1]
	sub	x1, x1, x0
	adrp	x2, g4_gc_heap_bytes
	add	x2, x2, #:lo12:g4_gc_heap_bytes
	str	x1, [x2]
	adrp	x1, g4_gc_reclaimed_bytes
	add	x1, x1, #:lo12:g4_gc_reclaimed_bytes
	ldr	x1, [x1]
	add	x0, x0, x1
	adrp	x1, g4_gc_reclaimed_bytes
	add	x1, x1, #:lo12:g4_gc_reclaimed_bytes
	str	x0, [x1]
	mov	x0, x21
	bl	free
	b	.L177
.L175:
	mov	x20, x21
	mov	x1, #8
	add	x1, x20, x1
	str	x0, [x1]
.L177:
	mov	x21, x19
	b	.L162
.L178:
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.type g4_gc_sweep, @function
.size g4_gc_sweep, .-g4_gc_sweep
/* end function g4_gc_sweep */

.text
.balign 16
g4_gc_collect:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	w19, w0
	bl	g4_gc_mark_roots
	bl	g4_gc_sweep
	mov	w0, w19
	adrp	x1, g4_gc_collection_count
	add	x1, x1, #:lo12:g4_gc_collection_count
	ldr	x1, [x1]
	mov	x2, #1
	add	x1, x1, x2
	adrp	x2, g4_gc_collection_count
	add	x2, x2, #:lo12:g4_gc_collection_count
	str	x1, [x2]
	cmp	w0, #0
	beq	.L181
	adrp	x2, g4_gc_automatic_collection_count
	add	x2, x2, #:lo12:g4_gc_automatic_collection_count
	ldr	x2, [x2]
	mov	x3, #1
	add	x2, x2, x3
	adrp	x3, g4_gc_automatic_collection_count
	add	x3, x3, #:lo12:g4_gc_automatic_collection_count
	str	x2, [x3]
.L181:
	adrp	x2, g4_gc_heap_bytes
	add	x2, x2, #:lo12:g4_gc_heap_bytes
	ldr	x2, [x2]
	mov	x3, #2
	mul	x2, x2, x3
	mov	x3, #65536
	add	x2, x2, x3
	cmp	x2, #256, lsl #12
	blt	.L183
	adrp	x3, g4_gc_heap_target
	add	x3, x3, #:lo12:g4_gc_heap_target
	str	x2, [x3]
	b	.L184
.L183:
	adrp	x3, g4_gc_heap_target
	add	x3, x3, #:lo12:g4_gc_heap_target
	mov	x2, #1048576
	str	x2, [x3]
.L184:
	bl	g4_gc_trace
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_gc_collect, @function
.size g4_gc_collect, .-g4_gc_collect
/* end function g4_gc_collect */

.text
.balign 16
g4_gc_trace_initialize:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	adrp	x0, g4_gc_trace_environment
	add	x0, x0, #:lo12:g4_gc_trace_environment
	bl	getenv
	adrp	x1, g4_gc_trace_enabled
	add	x1, x1, #:lo12:g4_gc_trace_enabled
	str	x0, [x1]
	ldp	x29, x30, [sp], 16
	ret
.type g4_gc_trace_initialize, @function
.size g4_gc_trace_initialize, .-g4_gc_trace_initialize
/* end function g4_gc_trace_initialize */

.text
.balign 16
g4_gc_trace:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	mov	x2, x1
	adrp	x1, g4_gc_trace_enabled
	add	x1, x1, #:lo12:g4_gc_trace_enabled
	ldr	x1, [x1]
	cmp	x1, #0
	beq	.L192
	cmp	w0, #0
	beq	.L191
	mov	x1, #64
	sdiv	x17, x2, x1
	msub	x1, x17, x1, x2
	cmp	x1, #0
	bne	.L192
.L191:
	mov	x1, #38
	mov	w19, w0
	adrp	x0, g4_gc_trace_collection
	add	x0, x0, #:lo12:g4_gc_trace_collection
	bl	g4_gc_report
	mov	w0, w19
	mov	w2, w0
	mov	x1, #37
	adrp	x0, g4_gc_trace_automatic
	add	x0, x0, #:lo12:g4_gc_trace_automatic
	bl	g4_gc_report
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x2, [x0]
	mov	x1, #38
	adrp	x0, g4_gc_trace_live
	add	x0, x0, #:lo12:g4_gc_trace_live
	bl	g4_gc_report
	adrp	x0, g4_gc_heap_target
	add	x0, x0, #:lo12:g4_gc_heap_target
	ldr	x2, [x0]
	mov	x1, #45
	adrp	x0, g4_gc_trace_target
	add	x0, x0, #:lo12:g4_gc_trace_target
	bl	g4_gc_report
	adrp	x0, g4_gc_temp_count
	add	x0, x0, #:lo12:g4_gc_temp_count
	ldr	x2, [x0]
	mov	x1, #38
	adrp	x0, g4_gc_trace_roots
	add	x0, x0, #:lo12:g4_gc_trace_roots
	bl	g4_gc_report
	adrp	x0, g4_gc_temp_capacity
	add	x0, x0, #:lo12:g4_gc_temp_capacity
	ldr	x2, [x0]
	mov	x1, #41
	adrp	x0, g4_gc_trace_capacity
	add	x0, x0, #:lo12:g4_gc_trace_capacity
	bl	g4_gc_report
.L192:
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_gc_trace, @function
.size g4_gc_trace, .-g4_gc_trace
/* end function g4_gc_trace */

.text
.balign 16
g4_gc_report:
	hint	#34
	stp	x29, x30, [sp, -64]!
	mov	x29, sp
	str	x19, [x29, 56]
	mov	x19, x2
	mov	x2, x1
	mov	x1, x0
	mov	w0, #2
	bl	write
	mov	x2, x19
	mov	x1, #32
	add	x0, x29, #16
	add	x1, x0, x1
	cmp	x2, #0
	beq	.L198
	mov	x0, x1
.L195:
	cmp	x2, #0
	beq	.L197
	mov	x3, #10
	sdiv	x17, x2, x3
	msub	x3, x17, x3, x2
	mov	x4, #48
	add	x3, x3, x4
	mov	x4, #1
	sub	x0, x0, x4
	strb	w3, [x0]
	mov	x3, #10
	sdiv	x2, x2, x3
	b	.L195
.L197:
	mov	x17, x1
	mov	x1, x0
	mov	x0, x17
	b	.L199
.L198:
	mov	x2, #31
	mov	x0, x1
	add	x1, x29, #16
	add	x1, x1, x2
	mov	w2, #48
	strb	w2, [x1]
.L199:
	sub	x2, x0, x1
	mov	w0, #2
	bl	write
	mov	x2, #1
	adrp	x1, g4_newline
	add	x1, x1, #:lo12:g4_newline
	mov	w0, #2
	bl	write
	ldr	x19, [x29, 56]
	ldp	x29, x30, [sp], 64
	ret
.type g4_gc_report, @function
.size g4_gc_report, .-g4_gc_report
/* end function g4_gc_report */

.text
.balign 16
g4_gc_finish:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	adrp	x0, g4_gc_stats_environment
	add	x0, x0, #:lo12:g4_gc_stats_environment
	bl	getenv
	mov	x19, x0
	adrp	x0, g4_gc_trace_enabled
	add	x0, x0, #:lo12:g4_gc_trace_enabled
	ldr	x1, [x0]
	cmp	x19, #0
	cset	w0, eq
	cmp	x1, #0
	cset	w1, eq
	and	w0, w0, w1
	cmp	w0, #0
	bne	.L204
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	mov	x0, #0
	str	x0, [x1]
	mov	x2, #96
	mov	w1, #0
	adrp	x0, g4_gc_global_roots
	add	x0, x0, #:lo12:g4_gc_global_roots
	bl	memset
	mov	w0, #0
	bl	g4_gc_collect
	cmp	x19, #0
	beq	.L204
	adrp	x0, g4_gc_collection_count
	add	x0, x0, #:lo12:g4_gc_collection_count
	ldr	x2, [x0]
	mov	x1, #38
	adrp	x0, g4_gc_report_collections
	add	x0, x0, #:lo12:g4_gc_report_collections
	bl	g4_gc_report
	adrp	x0, g4_gc_automatic_collection_count
	add	x0, x0, #:lo12:g4_gc_automatic_collection_count
	ldr	x2, [x0]
	mov	x1, #48
	adrp	x0, g4_gc_report_automatic
	add	x0, x0, #:lo12:g4_gc_report_automatic
	bl	g4_gc_report
	adrp	x0, g4_gc_allocated_bytes
	add	x0, x0, #:lo12:g4_gc_allocated_bytes
	ldr	x2, [x0]
	mov	x1, #42
	adrp	x0, g4_gc_report_allocated
	add	x0, x0, #:lo12:g4_gc_report_allocated
	bl	g4_gc_report
	adrp	x0, g4_gc_reclaimed_bytes
	add	x0, x0, #:lo12:g4_gc_reclaimed_bytes
	ldr	x2, [x0]
	mov	x1, #42
	adrp	x0, g4_gc_report_reclaimed
	add	x0, x0, #:lo12:g4_gc_report_reclaimed
	bl	g4_gc_report
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x2, [x0]
	mov	x1, #37
	adrp	x0, g4_gc_report_live
	add	x0, x0, #:lo12:g4_gc_report_live
	bl	g4_gc_report
	adrp	x0, g4_gc_peak_heap_bytes
	add	x0, x0, #:lo12:g4_gc_peak_heap_bytes
	ldr	x2, [x0]
	mov	x1, #42
	adrp	x0, g4_gc_report_peak
	add	x0, x0, #:lo12:g4_gc_report_peak
	bl	g4_gc_report
.L204:
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_gc_finish, @function
.size g4_gc_finish, .-g4_gc_finish
/* end function g4_gc_finish */

.text
.balign 16
g4_gc_temp_reserve:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	adrp	x1, g4_gc_temp_capacity
	add	x1, x1, #:lo12:g4_gc_temp_capacity
	ldr	x19, [x1]
	cmp	x0, x19
	ble	.L213
	cmp	x19, #0
	bne	.L208
	mov	x19, #64
.L208:
	cmp	x0, x19
	ble	.L210
	mov	x1, #2
	mul	x19, x19, x1
	b	.L208
.L210:
	mov	x0, #8
	mul	x1, x19, x0
	adrp	x0, g4_gc_temp_data
	add	x0, x0, #:lo12:g4_gc_temp_data
	ldr	x0, [x0]
	bl	realloc
	cmp	x0, #0
	beq	.L212
	adrp	x1, g4_gc_temp_data
	add	x1, x1, #:lo12:g4_gc_temp_data
	str	x0, [x1]
	adrp	x0, g4_gc_temp_capacity
	add	x0, x0, #:lo12:g4_gc_temp_capacity
	str	x19, [x0]
	b	.L213
.L212:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.L213:
	ldr	x19, [x29, 24]
	ldp	x29, x30, [sp], 32
	ret
.type g4_gc_temp_reserve, @function
.size g4_gc_temp_reserve, .-g4_gc_temp_reserve
/* end function g4_gc_temp_reserve */

.text
.balign 16
g4_array_push_paced:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x2, #8
	add	x2, x0, x2
	ldr	x2, [x2]
	mov	x3, #16
	add	x3, x0, x3
	ldr	x3, [x3]
	cmp	x2, x3
	beq	.L216
	mov	x3, #1
	add	x3, x2, x3
	mov	x4, #8
	add	x4, x0, x4
	str	x3, [x4]
	mov	x3, #24
	add	x0, x0, x3
	ldr	x0, [x0]
	mov	w3, #3
	lsl	x2, x2, x3
	add	x0, x0, x2
	str	x1, [x0]
	b	.L217
.L216:
	bl	g4_array_grow_paced
.L217:
	ldp	x29, x30, [sp], 16
	ret
.type g4_array_push_paced, @function
.size g4_array_push_paced, .-g4_array_push_paced
/* end function g4_array_push_paced */

.text
.balign 16
g4_array_grow_paced:
	hint	#34
	stp	x29, x30, [sp, -64]!
	mov	x29, sp
	str	x19, [x29, 56]
	str	x20, [x29, 48]
	str	x21, [x29, 40]
	str	x22, [x29, 32]
	str	x23, [x29, 24]
	str	x24, [x29, 16]
	mov	x22, x2
	mov	x20, x1
	mov	x19, x0
	mov	w0, #2
	lsl	x21, x3, x0
	mov	w0, #3
	lsl	x24, x21, x0
	mov	w0, #3
	lsl	x0, x3, x0
	sub	x23, x24, x0
	mov	x0, x23
	bl	g4_gc_maybe_collect
	mov	x1, x24
	mov	x0, #24
	add	x0, x19, x0
	ldr	x0, [x0]
	bl	realloc
	mov	x2, x22
	mov	x1, x20
	mov	x20, x0
	cmp	x20, #0
	beq	.L221
	adrp	x0, g4_gc_heap_bytes
	add	x0, x0, #:lo12:g4_gc_heap_bytes
	ldr	x0, [x0]
	add	x0, x23, x0
	adrp	x3, g4_gc_heap_bytes
	add	x3, x3, #:lo12:g4_gc_heap_bytes
	str	x0, [x3]
	mov	x22, x1
	adrp	x1, g4_gc_allocated_bytes
	add	x1, x1, #:lo12:g4_gc_allocated_bytes
	ldr	x1, [x1]
	add	x1, x23, x1
	mov	x23, x2
	adrp	x2, g4_gc_allocated_bytes
	add	x2, x2, #:lo12:g4_gc_allocated_bytes
	str	x1, [x2]
	bl	g4_gc_update_peak
	mov	x2, x23
	mov	x1, x22
	mov	x0, #16
	add	x0, x19, x0
	str	x21, [x0]
	mov	x0, #24
	add	x0, x19, x0
	str	x20, [x0]
	mov	w0, #3
	lsl	x0, x2, x0
	add	x0, x20, x0
	str	x1, [x0]
	mov	x0, #1
	add	x0, x2, x0
	mov	x1, #8
	add	x1, x19, x1
	str	x0, [x1]
	ldr	x19, [x29, 56]
	ldr	x20, [x29, 48]
	ldr	x21, [x29, 40]
	ldr	x22, [x29, 32]
	ldr	x23, [x29, 24]
	ldr	x24, [x29, 16]
	ldp	x29, x30, [sp], 64
	ret
.L221:
	mov	x1, #26
	adrp	x0, g4_allocation_error
	add	x0, x0, #:lo12:g4_allocation_error
	bl	g4_fail
	brk	#1000
.type g4_array_grow_paced, @function
.size g4_array_grow_paced, .-g4_array_grow_paced
/* end function g4_array_grow_paced */

.text
.balign 16
g4f0:
	hint	#34
	stp	x29, x30, [sp, -96]!
	mov	x29, sp
	str	x19, [x29, 88]
	str	x20, [x29, 80]
	str	x21, [x29, 72]
	str	x22, [x29, 64]
	str	x23, [x29, 56]
	str	x24, [x29, 48]
	str	x25, [x29, 40]
	str	x26, [x29, 32]
	str	x27, [x29, 24]
	str	x28, [x29, 16]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	ldr	x27, [x1]
	mov	x1, #3
	add	x23, x27, x1
	mov	x19, x0
	mov	x0, x23
	bl	g4_gc_temp_reserve
	mov	x0, x19
	mov	x19, x0
	adrp	x0, g4_desc_array_scalar
	add	x0, x0, #:lo12:g4_desc_array_scalar
	bl	g4_array_new
	mov	x21, x0
	mov	x0, x19
	mov	x19, x0
	adrp	x0, g4_desc_array_scalar
	add	x0, x0, #:lo12:g4_desc_array_scalar
	bl	g4_array_new
	mov	x20, x0
	mov	x0, x19
	mov	x19, x0
	adrp	x0, g4_desc_array_scalar
	add	x0, x0, #:lo12:g4_desc_array_scalar
	bl	g4_array_new
	mov	x22, x0
	mov	x0, x19
	mov	x1, #8
	mul	x24, x27, x1
	mov	x25, #0
.L224:
	adrp	x1, g4_gc_temp_data
	add	x1, x1, #:lo12:g4_gc_temp_data
	ldr	x1, [x1]
	add	x1, x1, x24
	str	x21, [x1]
	mov	x2, #8
	add	x2, x1, x2
	str	x20, [x2]
	mov	x2, #16
	add	x1, x1, x2
	str	x22, [x1]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x23, [x1]
	cmp	x25, x0
	cset	w1, lt
	mov	w1, w1
	cmp	x1, #0
	beq	.L229
	mov	x1, #0
	mov	x19, x0
	mov	x0, x21
	bl	g4_array_push_paced
	mov	x0, x19
	mov	x1, x25
	mov	x19, x0
	mov	x0, x20
	bl	g4_array_push_paced
	mov	x0, x19
	mov	x1, #0
	mov	x19, x0
	mov	x0, x22
	bl	g4_array_push_paced
	mov	x0, x19
	mov	x1, #1
	add	x25, x25, x1
	mov	x1, #9007199254740991
	cmp	x25, x1
	bgt	.L228
	mov	x19, x0
	mov	x0, #-9007199254740991
	cmp	x25, x0
	blt	.L228
	mov	x0, x19
	b	.L224
.L228:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L229:
	mov	x19, x0
	mov	x25, #0
	mov	x4, #0
	mov	x26, #0
.L230:
	mov	x28, x26
	adrp	x1, g4_gc_temp_data
	add	x1, x1, #:lo12:g4_gc_temp_data
	ldr	x1, [x1]
	add	x1, x24, x1
	str	x21, [x1]
	mov	x2, #8
	add	x2, x1, x2
	str	x20, [x2]
	mov	x2, #16
	add	x1, x1, x2
	str	x22, [x1]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x23, [x1]
	mov	x26, x28
.L232:
	cmp	x0, #1
	cset	w1, ne
	mov	w1, w1
	cmp	x1, #0
	beq	.L239
	mov	x1, #1
	mov	x28, x25
	sub	x25, x0, x1
	mov	x1, #9007199254740991
	cmp	x25, x1
	bgt	.L238
	mov	x1, #-9007199254740991
	cmp	x25, x1
	blt	.L238
	mov	x1, #8
	add	x1, x22, x1
	ldr	x1, [x1]
	mov	w2, #63
	asr	x2, x25, x2
	and	x2, x1, x2
	add	x2, x2, x25
	cmp	x2, x1
	bcs	.L311
	mov	x1, #24
	add	x1, x22, x1
	ldr	x1, [x1]
	mov	x3, #8
	mul	x2, x2, x3
	add	x1, x1, x2
	str	x0, [x1]
	mov	x0, x25
	mov	x25, x28
	b	.L232
.L238:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L239:
	mov	x28, x26
	adrp	x1, g4_gc_temp_data
	add	x1, x1, #:lo12:g4_gc_temp_data
	ldr	x1, [x1]
	add	x1, x24, x1
	str	x21, [x1]
	mov	x2, #8
	add	x2, x1, x2
	str	x20, [x2]
	mov	x2, #16
	add	x1, x1, x2
	str	x22, [x1]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x23, [x1]
	mov	x26, x28
	mov	x28, x25
	mov	x1, #0
.L242:
	cmp	x1, x19
	cset	w2, lt
	mov	w2, w2
	cmp	x2, #0
	beq	.L248
	mov	x2, #8
	add	x2, x21, x2
	ldr	x2, [x2]
	mov	w3, #63
	asr	x6, x1, x3
	and	x3, x2, x6
	add	x5, x3, x1
	cmp	x5, x2
	bcs	.L311
	mov	x2, #24
	add	x2, x21, x2
	ldr	x3, [x2]
	mov	x2, #8
	add	x2, x20, x2
	ldr	x2, [x2]
	and	x6, x6, x2
	add	x6, x6, x1
	cmp	x6, x2
	bcs	.L311
	mov	x2, #24
	add	x2, x20, x2
	ldr	x2, [x2]
	mov	x7, #8
	mul	x6, x6, x7
	add	x2, x2, x6
	ldr	x2, [x2]
	mov	x6, #8
	mul	x5, x5, x6
	add	x3, x3, x5
	str	x2, [x3]
	mov	x2, #1
	add	x1, x1, x2
	mov	x2, #9007199254740991
	cmp	x1, x2
	bgt	.L247
	mov	x2, #-9007199254740991
	cmp	x1, x2
	bge	.L242
.L247:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L248:
	mov	x25, x28
	mov	x28, x26
	adrp	x2, g4_gc_temp_data
	add	x2, x2, #:lo12:g4_gc_temp_data
	ldr	x2, [x2]
	add	x2, x24, x2
	str	x21, [x2]
	mov	x3, #8
	add	x3, x2, x3
	str	x20, [x3]
	mov	x3, #16
	add	x2, x2, x3
	str	x22, [x2]
	adrp	x2, g4_gc_temp_count
	add	x2, x2, #:lo12:g4_gc_temp_count
	str	x23, [x2]
	mov	x2, #8
	add	x2, x21, x2
	ldr	x2, [x2]
	mov	x3, #0
	and	x3, x2, x3
	cmp	x3, x2
	bcs	.L311
	mov	x2, #24
	add	x2, x21, x2
	ldr	x2, [x2]
	mov	x5, #8
	mul	x3, x3, x5
	add	x2, x2, x3
	ldr	x2, [x2]
	mov	x26, x28
	mov	x28, x25
	mov	x25, #0
.L252:
	cmp	x2, #0
	cset	w3, ne
	mov	w3, w3
	cmp	x3, #0
	beq	.L272
	mov	x1, #1
	add	x1, x2, x1
	mov	x3, #9007199254740991
	cmp	x1, x3
	bgt	.L271
	mov	x3, #-9007199254740991
	cmp	x1, x3
	blt	.L271
	mov	x3, #2
	sdiv	x3, x1, x3
	mov	x1, #0
.L257:
	cmp	x1, x3
	cset	w5, lt
	mov	w5, w5
	cmp	x5, #0
	beq	.L266
	sub	x13, x2, x1
	mov	x5, #9007199254740991
	cmp	x13, x5
	bgt	.L265
	mov	x5, #-9007199254740991
	cmp	x13, x5
	blt	.L265
	mov	x5, #8
	add	x5, x21, x5
	ldr	x7, [x5]
	mov	w5, #63
	asr	x11, x1, x5
	and	x12, x11, x7
	add	x10, x12, x1
	cmp	x10, x7
	bcs	.L311
	mov	x5, #24
	add	x5, x21, x5
	ldr	x9, [x5]
	mov	x5, #8
	mul	x8, x10, x5
	add	x5, x8, x9
	ldr	x5, [x5]
	mov	w6, #63
	asr	x6, x13, x6
	and	x6, x6, x7
	add	x6, x6, x13
	cmp	x6, x7
	bcs	.L311
	mov	x7, #8
	mul	x6, x6, x7
	add	x6, x6, x9
	ldr	x7, [x6]
	add	x8, x8, x9
	str	x7, [x8]
	str	x5, [x6]
	mov	x5, #1
	add	x1, x1, x5
	mov	x5, #9007199254740991
	cmp	x1, x5
	bgt	.L264
	mov	x5, #-9007199254740991
	cmp	x1, x5
	bge	.L257
.L264:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L265:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L266:
	adrp	x2, g4_gc_temp_data
	add	x2, x2, #:lo12:g4_gc_temp_data
	ldr	x2, [x2]
	add	x2, x24, x2
	str	x21, [x2]
	mov	x3, #8
	add	x3, x2, x3
	str	x20, [x3]
	mov	x3, #16
	add	x2, x2, x3
	str	x22, [x2]
	adrp	x2, g4_gc_temp_count
	add	x2, x2, #:lo12:g4_gc_temp_count
	str	x23, [x2]
	mov	x2, #1
	add	x25, x25, x2
	mov	x2, #9007199254740991
	cmp	x25, x2
	bgt	.L270
	mov	x2, #-9007199254740991
	cmp	x25, x2
	blt	.L270
	mov	x2, #8
	add	x2, x21, x2
	ldr	x2, [x2]
	mov	x3, #0
	and	x3, x2, x3
	cmp	x3, x2
	bcs	.L311
	mov	x2, #24
	add	x2, x21, x2
	ldr	x2, [x2]
	mov	x5, #8
	mul	x3, x3, x5
	add	x2, x2, x3
	ldr	x2, [x2]
	b	.L252
.L270:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L271:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L272:
	mov	x17, x25
	mov	x25, x26
	mov	x26, x17
	mov	x17, x28
	mov	x28, x25
	mov	x25, x17
	adrp	x2, g4_gc_temp_data
	add	x2, x2, #:lo12:g4_gc_temp_data
	ldr	x2, [x2]
	add	x2, x24, x2
	str	x21, [x2]
	mov	x3, #8
	add	x3, x2, x3
	str	x20, [x3]
	mov	x3, #16
	add	x2, x2, x3
	str	x22, [x2]
	adrp	x2, g4_gc_temp_count
	add	x2, x2, #:lo12:g4_gc_temp_count
	str	x23, [x2]
	cmp	x26, x25
	cset	w2, gt
	mov	w2, w2
	cmp	x2, #0
	beq	.L275
	mov	x25, x26
.L275:
	mov	x2, #2
	sdiv	x17, x4, x2
	msub	x2, x17, x2, x4
	cmp	x2, #0
	cset	w2, eq
	mov	w2, w2
	cmp	x2, #0
	bne	.L279
	sub	x26, x28, x26
	mov	x2, #9007199254740991
	cmp	x26, x2
	bgt	.L278
	mov	x2, #-9007199254740991
	cmp	x26, x2
	bge	.L281
.L278:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L279:
	add	x26, x28, x26
	mov	x2, #9007199254740991
	cmp	x26, x2
	bgt	.L310
	mov	x2, #-9007199254740991
	cmp	x26, x2
	blt	.L310
.L281:
	mov	x2, #1
.L282:
	adrp	x1, g4_gc_temp_data
	add	x1, x1, #:lo12:g4_gc_temp_data
	ldr	x1, [x1]
	add	x1, x24, x1
	str	x21, [x1]
	mov	x3, #8
	add	x3, x1, x3
	str	x20, [x3]
	mov	x3, #16
	add	x1, x1, x3
	str	x22, [x1]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x23, [x1]
	cmp	x2, #0
	beq	.L307
	cmp	x19, x0
	cset	w1, eq
	mov	w1, w1
	cmp	x1, #0
	bne	.L305
	mov	x1, #8
	add	x1, x20, x1
	ldr	x1, [x1]
	mov	x3, #0
	and	x3, x1, x3
	cmp	x3, x1
	bcs	.L311
	mov	x1, #24
	add	x1, x20, x1
	ldr	x1, [x1]
	mov	x5, #8
	mul	x3, x3, x5
	add	x1, x1, x3
	ldr	x3, [x1]
	mov	x1, #0
.L287:
	cmp	x1, x0
	cset	w5, lt
	mov	w5, w5
	cmp	x5, #0
	beq	.L294
	mov	x5, x1
	mov	x1, #1
	add	x1, x5, x1
	mov	x6, #9007199254740991
	cmp	x1, x6
	bgt	.L293
	mov	x6, #-9007199254740991
	cmp	x1, x6
	blt	.L293
	mov	x6, #8
	add	x6, x20, x6
	ldr	x8, [x6]
	mov	w6, #63
	asr	x6, x5, x6
	and	x6, x6, x8
	add	x6, x6, x5
	cmp	x6, x8
	bcs	.L311
	mov	x5, #24
	add	x5, x20, x5
	ldr	x7, [x5]
	mov	w5, #63
	asr	x5, x1, x5
	and	x5, x5, x8
	add	x5, x5, x1
	cmp	x5, x8
	bcs	.L311
	mov	x8, #8
	mul	x5, x5, x8
	add	x5, x5, x7
	ldr	x5, [x5]
	mov	x8, #8
	mul	x6, x6, x8
	add	x6, x6, x7
	str	x5, [x6]
	b	.L287
.L293:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L294:
	adrp	x5, g4_gc_temp_data
	add	x5, x5, #:lo12:g4_gc_temp_data
	ldr	x5, [x5]
	add	x5, x24, x5
	str	x21, [x5]
	mov	x6, #8
	add	x6, x5, x6
	str	x20, [x6]
	mov	x6, #16
	add	x5, x5, x6
	str	x22, [x5]
	adrp	x5, g4_gc_temp_count
	add	x5, x5, #:lo12:g4_gc_temp_count
	str	x23, [x5]
	mov	x5, #8
	add	x5, x20, x5
	ldr	x5, [x5]
	mov	w6, #63
	asr	x7, x0, x6
	and	x6, x5, x7
	add	x6, x6, x0
	cmp	x6, x5
	bcs	.L311
	mov	x5, #24
	add	x5, x20, x5
	ldr	x5, [x5]
	mov	x8, #8
	mul	x6, x6, x8
	add	x5, x5, x6
	str	x3, [x5]
	mov	x3, #8
	add	x3, x22, x3
	ldr	x8, [x3]
	and	x10, x7, x8
	add	x9, x10, x0
	cmp	x9, x8
	bcs	.L311
	mov	x3, #24
	add	x3, x22, x3
	ldr	x5, [x3]
	mov	x3, #8
	mul	x3, x9, x3
	add	x6, x3, x5
	ldr	x6, [x6]
	mov	x11, #1
	sub	x6, x6, x11
	mov	x11, #9007199254740991
	cmp	x6, x11
	bgt	.L304
	mov	x11, #-9007199254740991
	cmp	x6, x11
	blt	.L304
	add	x7, x3, x5
	str	x6, [x7]
	add	x3, x3, x5
	ldr	x3, [x3]
	cmp	x3, #0
	cset	w3, gt
	mov	w3, w3
	cmp	x3, #0
	bne	.L302
	mov	x3, #1
	add	x28, x0, x3
	mov	x0, #9007199254740991
	cmp	x28, x0
	bgt	.L301
	mov	x0, #-9007199254740991
	cmp	x28, x0
	bge	.L303
.L301:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L302:
	mov	x28, x0
	mov	x2, #0
.L303:
	mov	x0, x28
	b	.L282
.L304:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L305:
	mov	x2, #0
	mov	x1, #16
	adrp	x0, g4_desc_record0
	add	x0, x0, #:lo12:g4_desc_record0
	bl	g4_gc_alloc
	mov	x1, #8
	add	x1, x0, x1
	str	x26, [x1]
	mov	x1, #16
	add	x1, x0, x1
	str	x25, [x1]
	adrp	x1, g4_gc_temp_count
	add	x1, x1, #:lo12:g4_gc_temp_count
	str	x27, [x1]
	mov	x19, x0
	bl	g4_gc_temp_push
	mov	x0, x19
	ldr	x19, [x29, 88]
	ldr	x20, [x29, 80]
	ldr	x21, [x29, 72]
	ldr	x22, [x29, 64]
	ldr	x23, [x29, 56]
	ldr	x24, [x29, 48]
	ldr	x25, [x29, 40]
	ldr	x26, [x29, 32]
	ldr	x27, [x29, 24]
	ldr	x28, [x29, 16]
	ldp	x29, x30, [sp], 96
	ret
.L307:
	mov	x1, #1
	add	x4, x4, x1
	mov	x1, #9007199254740991
	cmp	x4, x1
	bgt	.L309
	mov	x1, #-9007199254740991
	cmp	x4, x1
	bge	.L230
.L309:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L310:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L311:
	mov	x1, #30
	adrp	x0, g4_bounds_error
	add	x0, x0, #:lo12:g4_bounds_error
	bl	g4_fail
	brk	#1000
.type g4f0, @function
.size g4f0, .-g4f0
/* end function g4f0 */

.text
.balign 16
g4f1:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	adrp	x0, g4_gc_temp_count
	add	x0, x0, #:lo12:g4_gc_temp_count
	ldr	x19, [x0]
	mov	x0, #2
	add	x0, x19, x0
	bl	g4_gc_temp_reserve
	bl	g4_process_argv
	mov	x1, #8
	add	x1, x0, x1
	ldr	x1, [x1]
	cmp	x1, #0
	cset	w1, gt
	mov	w1, w1
	cmp	x1, #0
	bne	.L314
	mov	x0, #7
	b	.L315
.L314:
	mov	x1, #0
	bl	g4_array_address
	ldr	x0, [x0]
	bl	g4_string_to_integer
.L315:
	mov	x20, x0
	bl	g4f0
	mov	x21, x0
	mov	x0, x20
	mov	x20, x0
	mov	x0, #8
	add	x0, x21, x0
	ldr	x0, [x0]
	bl	g4_integer_to_string
	bl	g4_puts
	mov	x0, x20
	bl	g4_integer_to_string
	mov	x1, x0
	adrp	x0, g4s482
	add	x0, x0, #:lo12:g4s482
	bl	g4_string_concat
	adrp	x1, g4s490
	add	x1, x1, #:lo12:g4s490
	bl	g4_string_concat
	mov	x20, x0
	mov	x0, #16
	add	x0, x21, x0
	ldr	x0, [x0]
	bl	g4_integer_to_string
	mov	x1, x0
	mov	x0, x20
	bl	g4_string_concat
	bl	g4_puts
	adrp	x0, g4_gc_temp_count
	add	x0, x0, #:lo12:g4_gc_temp_count
	str	x19, [x0]
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldp	x29, x30, [sp], 48
	ret
.type g4f1, @function
.size g4f1, .-g4f1
/* end function g4f1 */

.text
.balign 16
.globl main
main:
	hint	#34
	stp	x29, x30, [sp, -32]!
	mov	x29, sp
	str	x19, [x29, 24]
	str	x20, [x29, 16]
	mov	x20, x1
	mov	w19, w0
	bl	g4_gc_trace_initialize
	mov	x1, x20
	mov	w0, w19
	sxtw	x0, w0
	adrp	x2, g4_process_argc
	add	x2, x2, #:lo12:g4_process_argc
	str	x0, [x2]
	adrp	x0, g4_process_argv_pointer
	add	x0, x0, #:lo12:g4_process_argv_pointer
	str	x1, [x0]
	bl	g4f1
	bl	g4_gc_finish
	mov	w0, #0
	ldr	x19, [x29, 24]
	ldr	x20, [x29, 16]
	ldp	x29, x30, [sp], 32
	ret
.type main, @function
.size main, .-main
/* end function main */

.text
.balign 16
g4_array_address:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x2, #8
	add	x2, x0, x2
	ldr	x2, [x2]
	cmp	x1, #0
	bge	.L321
	add	x1, x1, x2
.L321:
	cmp	x1, x2
	bcc	.L323
	mov	x1, #30
	adrp	x0, g4_bounds_error
	add	x0, x0, #:lo12:g4_bounds_error
	bl	g4_fail
	brk	#1000
.L323:
	mov	x2, #24
	add	x0, x0, x2
	ldr	x0, [x0]
	mov	x2, #8
	mul	x1, x1, x2
	add	x0, x0, x1
	ldp	x29, x30, [sp], 16
	ret
.type g4_array_address, @function
.size g4_array_address, .-g4_array_address
/* end function g4_array_address */

.data
.balign 8
g4_process_argc:
	.quad 0
/* end data */

.data
.balign 8
g4_process_argv_pointer:
	.quad 0
/* end data */

.text
.balign 16
g4_process_argv:
	hint	#34
	stp	x29, x30, [sp, -48]!
	mov	x29, sp
	str	x19, [x29, 40]
	str	x20, [x29, 32]
	str	x21, [x29, 24]
	str	x22, [x29, 16]
	adrp	x0, g4_desc_array_managed
	add	x0, x0, #:lo12:g4_desc_array_managed
	bl	g4_array_new
	adrp	x1, g4_process_argc
	add	x1, x1, #:lo12:g4_process_argc
	ldr	x21, [x1]
	adrp	x1, g4_process_argv_pointer
	add	x1, x1, #:lo12:g4_process_argv_pointer
	ldr	x22, [x1]
	mov	x20, x0
	mov	x19, #1
.L327:
	cmp	x21, x19
	ble	.L329
	mov	x0, #8
	mul	x0, x19, x0
	add	x0, x22, x0
	ldr	x0, [x0]
	bl	g4_string_from_c
	mov	x1, x0
	mov	x0, x20
	bl	g4_array_push_paced
	mov	x0, #1
	add	x19, x19, x0
	b	.L327
.L329:
	mov	x0, x20
	ldr	x19, [x29, 40]
	ldr	x20, [x29, 32]
	ldr	x21, [x29, 24]
	ldr	x22, [x29, 16]
	ldp	x29, x30, [sp], 48
	ret
.type g4_process_argv, @function
.size g4_process_argv, .-g4_process_argv
/* end function g4_process_argv */

.data
.balign 8
g4_invalid_integer_error:
	.ascii "panic: invalid Integer"
	.byte 10
/* end data */

.text
.balign 16
g4_string_to_integer:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	mov	x1, x0
	mov	x0, #8
	add	x0, x1, x0
	ldr	x0, [x0]
	cmp	x0, #0
	beq	.L350
	mov	x2, #16
	sub	sp, sp, x2
	mov	x3, sp
	mov	x2, #16
	add	x1, x1, x2
	ldrb	w4, [x1]
	cmp	w4, #43
	cset	w2, eq
	cmp	w4, #45
	cset	w5, eq
	orr	w2, w2, w5
	cmp	w2, #0
	bne	.L335
	mov	x2, #0
	str	x2, [x3]
	mov	x3, #0
	mov	x2, #0
	b	.L338
.L335:
	cmp	x0, #1
	beq	.L350
	mov	x2, #1
	str	x2, [x3]
	mov	x3, #1
	mov	x2, #1
.L338:
	cmp	x0, x3
	ble	.L341
	add	x5, x3, x1
	ldrb	w6, [x5]
	cmp	w6, #48
	cset	w5, lt
	cmp	w6, #57
	cset	w6, gt
	orr	w5, w5, w6
	cmp	w5, #0
	bne	.L350
	mov	x5, #1
	add	x3, x3, x5
	b	.L338
.L341:
	mov	x3, #0
.L342:
	cmp	x0, x2
	ble	.L346
	add	x5, x2, x1
	ldrb	w5, [x5]
	mov	w6, #48
	sub	w5, w5, w6
	mov	w5, w5
	mov	x6, #13107
	movk	x6, #0x3333, lsl #16
	movk	x6, #0x3333, lsl #32
	movk	x6, #0x3, lsl #48
	cmp	x3, x6
	cset	w6, gt
	mov	x7, #13107
	movk	x7, #0x3333, lsl #16
	movk	x7, #0x3333, lsl #32
	movk	x7, #0x3, lsl #48
	cmp	x3, x7
	cset	w7, eq
	cmp	x5, #1
	cset	w8, gt
	and	w7, w7, w8
	orr	w6, w6, w7
	cmp	w6, #0
	bne	.L345
	mov	x6, #10
	mul	x3, x3, x6
	add	x3, x3, x5
	mov	x5, #1
	add	x2, x2, x5
	b	.L342
.L345:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.L346:
	cmp	w4, #45
	beq	.L348
	mov	x0, x3
	b	.L349
.L348:
	mov	x0, #0
	sub	x0, x0, x3
.L349:
	mov sp, x29
	ldp	x29, x30, [sp], 16
	ret
.L350:
	mov	x1, #23
	adrp	x0, g4_invalid_integer_error
	add	x0, x0, #:lo12:g4_invalid_integer_error
	bl	g4_fail
	brk	#1000
.type g4_string_to_integer, @function
.size g4_string_to_integer, .-g4_string_to_integer
/* end function g4_string_to_integer */

.text
.balign 16
g4_integer_to_string:
	hint	#34
	stp	x29, x30, [sp, -80]!
	mov	x29, sp
	str	x19, [x29, 72]
	str	x20, [x29, 64]
	str	x21, [x29, 56]
	cmp	x0, #0
	blt	.L353
	mov	x2, x0
	b	.L355
.L353:
	mov	x1, #0
	sub	x1, x1, x0
	mov	x2, x1
.L355:
	mov	x3, #32
	add	x1, x29, #16
	add	x1, x1, x3
	cmp	x2, #0
	beq	.L360
	mov	x20, x1
	mov	x19, x1
	mov	x1, x0
	mov	x0, x2
.L357:
	cmp	x0, #0
	beq	.L359
	mov	x2, #10
	sdiv	x17, x0, x2
	msub	x2, x17, x2, x0
	mov	x3, #48
	add	x2, x2, x3
	mov	x3, #1
	sub	x19, x19, x3
	strb	w2, [x19]
	mov	x2, #10
	sdiv	x0, x0, x2
	b	.L357
.L359:
	mov	x0, x1
	mov	x1, x20
	b	.L361
.L360:
	mov	x3, #31
	add	x2, x29, #16
	add	x19, x2, x3
	mov	w2, #48
	strb	w2, [x19]
.L361:
	cmp	x0, #0
	bge	.L363
	mov	x0, #1
	sub	x19, x19, x0
	mov	w0, #45
	strb	w0, [x19]
.L363:
	mov	x20, x19
	sub	x19, x1, x20
	mov	x0, #9
	add	x0, x19, x0
	bl	g4_string_alloc
	mov	x1, x20
	mov	x2, #8
	add	x2, x0, x2
	str	x19, [x2]
	mov	x2, #16
	add	x20, x0, x2
	mov	x2, x19
	mov	x21, x0
	mov	x0, x20
	bl	memcpy
	mov	x0, x21
	add	x2, x19, x20
	mov	w1, #0
	strb	w1, [x2]
	ldr	x19, [x29, 72]
	ldr	x20, [x29, 64]
	ldr	x21, [x29, 56]
	ldp	x29, x30, [sp], 80
	ret
.type g4_integer_to_string, @function
.size g4_integer_to_string, .-g4_integer_to_string
/* end function g4_integer_to_string */

.data
.balign 8
g4_float_integer_error:
	.ascii "panic: Float cannot be converted to Integer"
	.byte 10
/* end data */

.text
.balign 16
g4_float_to_integer:
	hint	#34
	stp	x29, x30, [sp, -16]!
	mov	x29, sp
	fsub	d1, d0, d0
	fcmpe	d1, d1
	beq	.L367
	mov	x1, #44
	adrp	x0, g4_float_integer_error
	add	x0, x0, #:lo12:g4_float_integer_error
	bl	g4_fail
	brk	#1000
.L367:
	adrp	x0, ".Lfp1"
	add	x0, x0, #:lo12:".Lfp1"
	ldr	d1, [x0]
	fcmpe	d0, d1
	cset	w0, gt
	adrp	x1, ".Lfp0"
	add	x1, x1, #:lo12:".Lfp0"
	ldr	d1, [x1]
	fcmpe	d0, d1
	cset	w1, mi
	orr	w0, w0, w1
	cmp	w0, #0
	bne	.L370
	fcvtzs	x0, d0
	ldp	x29, x30, [sp], 16
	ret
.L370:
	mov	x1, #45
	adrp	x0, g4_integer_range_error
	add	x0, x0, #:lo12:g4_integer_range_error
	bl	g4_fail
	brk	#1000
.type g4_float_to_integer, @function
.size g4_float_to_integer, .-g4_float_to_integer
/* end function g4_float_to_integer */

/* floating point constants */
.section .rodata
.p2align 3
.Lfp0:
	.quad -4377498837804122113 /* -9007199254740991.000000 */

.section .rodata
.p2align 3
.Lfp1:
	.quad 4845873199050653695 /* 9007199254740991.000000 */

.section .note.GNU-stack,"",@progbits
