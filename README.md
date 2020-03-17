# NCM-Forest-FPGA
An FPGA implementation of the NCM-Forest algorithm, using the myhdl python package.

## What's in this repo? 
Under the `tests-and-ideas/` folder, you'll find various python implementations of useful algorithms used in this project, these are not necessarily `myhdl` modules and do not necessarily satisfy the same dependencies.  
Under the `doc/` folder, you'll find documentation for the different modules (TODO).  
Under the `modules/` folder, you'll find all the HDL modules. Their test benches are in the `if __name__ == "__main__"` blocks.  
**_/!\\_ DISCLAIMER _/!\\_**, you will only find functionning modules on here, the ones needing debugging are handled in another private and local repository.
Tests are performed automatically on modules that need test benches to allow their upload to this repository, basic ones are exempt from it (like the `clkdriver.py` and `debugger.py` modules).

## Dependencies
So far, only one dependency is needed `myhdl 0.11` for python 3.  
Code is tested under the `default` branch of python `3.8.2`.  
