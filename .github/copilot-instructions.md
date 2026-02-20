# Copilot Instructions for Nand2Tetris CSC345 Coursework

## Project Overview
This repository contains coursework for **Nand2Tetris**, an educational computer science curriculum spanning from logic gates to high-level applications. The project teaches how computers are built from first principles.

- **CSC345 folder**: Python hello world starter program
- **06 folder**: Hack assembly language programs (Project 6 - Assembler projects)

## Key Codebase Patterns

### Hack Assembly Language
All `.asm` files use **Hack assembly**, a minimalist ISA designed for educational purposes. Key characteristics:
- **A-instruction**: `@value` - sets the A register (address/value)
- **C-instruction**: `dest=comp;jump` - computation and conditional jumps
- **Symbols**: Labels `(LABEL)` and variables auto-allocate from RAM[16] onward
- **Memory layout**: RAM[0-15] are R0-R15 registers; RAM[16384-24575] is SCREEN; RAM[24576] is KEYBOARD

### Program Structure Patterns
Programs follow these conventions:
1. **Header comment**: Attribution to Nand2Tetris, file location in projects structure
2. **Algorithm comment**: Plain English explanation of what the program computes
3. **Usage notes**: Input (which registers to populate) and output (which register holds result)
4. **Symbol-less variants** (e.g., `MaxL.asm`): Tests assembler without symbol table support; uses hardcoded addresses

### Common Program Types in This Collection
- **Math operations** (`Add.asm`): Basic arithmetic on register values
- **Conditionals** (`Max.asm`): Compares R0 and R1, stores max in R2 using `D;JGT` jumps
- **Screen drawing** (`Rect.asm`): Manipulates SCREEN memory to render graphics; uses `@SCREEN` base address and 32-pixel row stride
- **Complex programs** (`Pong.asm`): Compiler-generated code from Jack → VM → Hack pipeline; dense, function-like structure with stack management

## Critical Developer Workflows

### Understanding Hack Programs
1. **Trace execution**: Follow D register state through A/C instructions; jumps always check D register condition
2. **Memory reasoning**: Track which registers are inputs/outputs; verify SCREEN address calculations use 32-word rows
3. **Debugging symbol-less versions**: Map numeric addresses to their symbol equivalents in the symbol version to verify correctness

### Testing Conventions
- Programs are meant to run on the Hack VM simulator (part of Nand2Tetris tools)
- Pre-populate input registers before execution; check output registers after completion
- Infinite loop `(END) @END 0;JMP` is standard to halt program cleanly

## Cross-Program Patterns to Recognize

| Pattern | Example | Use Case |
|---------|---------|----------|
| Value to register | `@2 D=A @R0 M=D` | Loading immediate values into memory |
| Conditional branch | `D;JGT` / `D;JLE` | If-then logic; Max.asm demonstrates comparison pattern |
| Loop with decrement | `MD=M-1 @LOOP D;JGT` | Rect.asm uses this for iteration without a loop counter variable |
| Address arithmetic | `D=D+A` then `@addr M=D` | Rect.asm adds row stride (32) to traverse screen rows |

## Important Context for Large Programs
- **Pong.asm** (~28k lines): This is **compiler output**, not hand-written code—it's the Hack assembly result of compiling Jack source through the VM translator. Use it as a reference for understanding compiler-generated patterns, not as a model for writing code.
- Expect stack-based calling conventions (function prologue/epilogue), local variable slots on stack, and indirect addressing via pointer registers.

## When Helping with Code
- **Syntax**: Strictly follow `dest=comp;jump` structure; whitespace is flexible but comments use `//`
- **Naming**: Use SCREAMING_SNAKE_CASE for symbolic labels/variables to match project conventions
- **Logic**: Verify D register is set before conditional jumps; confirm all loops have termination conditions
- **Assembly vs. Symbol**: When symbol-less version exists, ensure hardcoded addresses match the symbolic version's computed layout
