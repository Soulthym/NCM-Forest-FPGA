from myhdl import block, Signal, intbv, always, instance, delay, modbv
from debugger import Debugger
from clkdriver import ClkDriver
from counter import Counter
from utils import strbv

@block
def MemController(clk, mem, address, data_o, data_i, write_enable):
    """
    MemController(clk, mem, address, data_o, data_i, write_enable):
        - returns a memory reader
        - arguments:
            clk: the clock driving the reader
                type:               Signal(bool)
                kind of argument:   SENSIBILITY
            mem: the memory you want to access using this controller
                type:               list(intbv) OR list(modbv),
                                    ALL ELEMENTS IN IT MUST BE THE SAME BITSIZE
                kind of argument:   INPUT
            address: the address in the memory you want to access
                type:               Signal(intbv) OR Signal(modbv)
                kind of argument:   INPUT
            data_o: the Signal in which to retrieve the memory content
                type:               Signal(intbv) OR Signal(modbv)
                kind of argument:   OUTPUT
                bitsize:            same as every element in mem
            data_i: the Signal from which to write the memory content
                type:               Signal(intbv) OR Signal(modbv)
                kind of argument:   INPUT
                bitsize:            same as every element in mem
            write_enable: the Signal telling when to write data to the
                          specified address in memory.
                          If writing to the memory, data_o will also
                          be updated as the previous value of the memory cell,
                          until the next clock cycle.
                          Set the bit to 1 OR True if you want to write to the
                          specified address, otherwise set it to 0 OR False.
                type:               Signal(bool)
                kind of argument:   INPUT
    Example:
    mem = [intbv(val, max=10, min=0)
               for val in range(10)]
    address = Signal(modbv(0, max=mem_size, min=0))
    data_o = Signal(intbv(mem[address], min=0, max=10))
    data_i = Signal(intbv(mem[address], min=0, max=10))
    write_enable = Signal(bool(False))
    memController = MemController(clk=clk,                  #clock signal
                              mem=mem,
                              address=address,
                              data_o=data_o,
                              data_i=data_i,
                              write_enable=write_enable,
                             )
    """

    @always(clk.posedge)
    def readwrite():
        if write_enable == True:
            mem[address].next = data_i
        data_o.next = mem[address]
    return readwrite


@block
def TestBench(steps, word_size=3, mem_size=2**3):
    # useful values
    max_val= 2**(word_size - 1)
    min_val= -max_val
    print("\n".join([
        f"{steps=}",
        f"{word_size=}",
        f"{mem_size=}",
        f"{max_val=}",
        f"{min_val=}",
    ]))

    # clock
    clk = Signal(bool(0))
    clkDriver = ClkDriver(clk=clk,
                          period=2)

    # counter
    cnt = Signal(intbv(0, min=0, max=steps+2))
    counter = Counter(clk=clk,
                      cnt=cnt)

    # memory
    mem = [Signal(intbv(0, max=max_val, min=min_val))
               for _ in range(min_val, max_val)]
    address = Signal(modbv(0, max=mem_size, min=0))
    data_o = Signal(intbv(int(mem[address].val), max=max_val, min=min_val))
    data_i = Signal(intbv(int(mem[address].val), max=max_val, min=min_val))
    write_enable = Signal(bool(0))
    memController = MemController(clk=clk,
                              mem=mem,
                              address=address,
                              data_o=data_o,
                              data_i=data_i,
                              write_enable=write_enable,
                             )

    # debugger
    debugger = Debugger(period=1,
                        funcs={"cnt":lambda c: str(int(c)),
                               "clk":lambda c: str(int(c)),
                               "adr":strbv,
                               "d_o":strbv,
                               "d_i":strbv,
                               "w_e":lambda c: str(int(c)),
                               "mem":lambda c: '['+','.join([strbv(cc) for cc in c])+']',
                              },
                        cnt=cnt,
                        clk=clk,
                        adr=address,
                        d_o=data_o,
                        d_i=data_i,
                        w_e=write_enable,
                        mem=mem,
                       )

    @instance
    def tests():
        for index, tested_value in enumerate(range(min_val, max_val)):
            address.next = index
            write_enable.next = True
            data_i.next = tested_value
            yield delay(2)
            assert (int(data_o) == 0), "data_o and previous mem[address] do not match while setting memory values"
            assert (int(data_i) == int(mem[address])), "data_i and mem[address] do not match while setting memory values"
        write_enable.next = False
        for index, tested_value in enumerate(range(min_val, max_val)):
            address.next = index
            yield delay(2)
            assert (int(data_o) == tested_value), "values do not match"

    return clkDriver, counter, debugger, memController, tests


def toHDL(min_val, max_val, mem_size, hdl="VHDL"):
    assert (hdl in ["VHDL","Verilog"]), f"{hdl=} isn't a valid HDL, should take one of the following values: \"VHDL\" or \"Verilog\""
    assert (isinstance(max_val, int)), "{max_val=} should be an int"
    assert (isinstance(min_val, int)), "{min_val=} should be an int"
    assert (isinstance(mem_size, int)), "{mem_size=} should be an int"
    assert (min_val <= max_val), f"{min_val=} > {max_val=}, min_val should be < max_val"
    assert (mem_size > 0), "{mem_size=} should be an int > 0"
    clk = Signal(bool(0))
    mem = [Signal(intbv(0, max=max_val, min=min_val))
               for _ in range(mem_size)]
    address = Signal(modbv(0, max=mem_size, min=0))
    data_o = Signal(intbv(int(mem[address].val), max=max_val, min=min_val))
    data_i = Signal(intbv(int(mem[address].val), max=max_val, min=min_val))
    write_enable = Signal(bool(0))
    memController = MemController(clk=clk,
                              mem=mem,
                              address=address,
                              data_o=data_o,
                              data_i=data_i,
                              write_enable=write_enable,
                             )
    memController.convert(hdl=hdl)


if __name__ == '__main__':
    steps=35
    inst=TestBench(steps)
    inst.run_sim(steps)
    print("simulation ran successfully!")
    toHDL(min_val=-4,
          max_val=4,
          mem_size=3,
          hdl="VHDL"
         )
