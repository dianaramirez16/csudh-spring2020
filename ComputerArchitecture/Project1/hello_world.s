.data
min:            .word 0
max:            .word 0
avg:            .float 0

count_query:    .asciiz "Number of elements: "
val_query:      .asciiz "Next item: "

output:         .asciiz "Array Details"
output_max:     .asciiz "Array Maximum: "
output_min:     .asciiz "Array Minimum: "
output_avg:     .asciiz "Array Average: "

item_sep:       .asciiz ", "
tab_line:       .asciiz "\t"
new_line:       .asciiz "\n"

.text

.globl main

main:
# ASK HOW MANY ELEMENTS IN ARRAY
li      $v0, 4
la      $a0, count_query
syscall

# GET INT
li      $v0, 5
syscall
move    $t0, $v0

# ALLOCATE SPACE
li      $v0, 9
sll     $a0, $t0, 2
syscall
move    $t7, $v0               # address of array memory

# GET VALUES FROM USER
move    $t1, $t7               # array index address
li      $t2, 0                 # counter

query_loop:
# CONDITION TO TERMINATE LOOP
slt     $t6, $t2, $t0
beq     $t6, $0,  end_query

li      $v0, 4
la      $a0, val_query
syscall
li      $v0, 5
syscall
sw      $v0, ($t1)

addiu	$t1, $t1, 4             # advance $t1 by 4
addiu   $t2, $t2, 1             # i++

j       query_loop
end_query:

li      $v0, 4
la      $a0, new_line
syscall
la      $a0, output
syscall
la      $a0, new_line
syscall
la      $a0, tab_line
syscall

# PRINT ARRAY
# FIND MIN, MAX, AVG
move    $t1, $t7               # array index address
li      $t2, 0                 # counter
li      $t5, 0                 # sum
print_loop:
# CONDITION TO TERMINATE LOOP
slt     $t6, $t2, $t0
beq     $t6, $0,  end_print

lw      $t3, ($t1)
li      $v0, 1
addu    $a0, $0, $t3
syscall

la      $t4, min
slt     $t6, $t3, $t4
movn    $t4, $t3, $t6
sw      $t4, min

la      $t4, max
slt     $t6, $t3, $t4
movz    $t4, $t3, $t6
sw      $t4, max

add     $t5, $t5, $t3

addiu   $t4, $t2, 1
slt     $t6, $t4, $t0
beq     $t6, $0,  last_item

li      $v0, 4
la      $a0, item_sep
syscall

last_item:

addiu	$t1, $t1, 4             # advance $t1 by 4
addiu   $t2, $t2, 1             # i++

j       print_loop
end_print:

# PRINT MINIMUM
li      $v0, 4
la      $a0, new_line
syscall
la      $a0, tab_line
syscall
la      $a0, output_min
syscall

li      $v0, 1
la      $a0, min
syscall

# PRINT MAXIMUM
li      $v0, 4
la      $a0, new_line
syscall
la      $a0, tab_line
syscall
la      $a0, output_max
syscall

li      $v0, 1
la      $a0, max
syscall

# PRINT AVERAGE
div     $t5, $t0
sw      $t5, avg

li      $v0, 4
la      $a0, new_line
syscall
la      $a0, tab_line
syscall
la      $a0, output_avg
syscall

li      $v0, 2
la      $f12, avg
syscall


# SORT ARRAY


# CALL EXIT
li	$v0, 10
syscall