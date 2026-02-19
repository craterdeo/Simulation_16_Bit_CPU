# Simulation_16_Bit_CPU

A weekend project exploring low-level CPU architecture and instruction set design.  
The goal was to simulate a small 16-bit CPU in Python and understand how registers, memory, and control flow interact in a real processor.

---

## Project Overview

- Implements 16 general-purpose registers (`R0`–`R15`)  
- Uses a 16-bit memory model and program counter  
- Supports arithmetic (`ADD`, `SUB`), logic (`AND`, `OR`), and memory operations (`LOAD`, `STORE`)  
- Control flow instructions include `JMP`, `JZ` (jump if zero), and `JNZ` (jump if not zero)  
- Includes a zero flag to enable conditional execution
- Runs a simple control sequence to find largest fibonacci term a 16 bit CPU can calculate without overflow

This CPU is conceptually **Turing complete**:  

- It supports loops and conditional branching  
- Arbitrary memory read/write allows simulation of a Turing machine tape  
- Programs can compute anything a real CPU can, as long as memory is sufficient  

---
