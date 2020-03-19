from myhdl import block, Signal, intbv, always, instance, delay, modbv
from debugger import Debugger
from clkdriver import ClkDriver
from counter import Counter
from utils import strbv

@block
def MemController(clk, mem, address, data_o):
    """
    MemController(clk, mem, address, data_o):
        - returns a memory reader
        - arguments:
            clk: the clock driving the reader
                type:               Signal(bool)
                kind of argument:   SENSIBILITY
            mem: the memory you want to access using this controller
                type:               list(intbv) OR list(modbv)
                kind of argument:   INPUT
            address: the address in the memory you want to access
                type:               Signal(intbv) OR Signal(modbv)
                kind of argument:   INPUT
            data_o: the Signal in which to retrieve the memory content
                type:               Signal(intbv) OR Signal(modbv)
                kind of argument:   OUTPUT
    Example:
    mem = [intbv(val, max=10, min=0)
               for val in range(10)]
    address = Signal(modbv(0, max=mem_size, min=0))
    data_o = Signal(intbv(mem[address], min=0, max=10))
    memReader = MemController(clk=clk,                  #clock signal
                              mem=mem,
                              address=address,
                              data_o=data_o,
                             )
    """

    @always(clk.posedge)
    def readMem():
        data_o.next = mem[address]
    return readMem


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
    mem = [intbv(val, max=max_val, min=min_val)
               for val in range(min_val, max_val)]
    print(mem)
    address = Signal(modbv(0, max=mem_size, min=0))
    data_o = Signal(intbv(mem[address], max=max_val, min=min_val))
    memReader = MemController(clk=clk,
                              mem=mem,
                              address=address,
                              data_o=data_o,
                             )

    # debugger
    debugger = Debugger(period=1,
                        funcs={"cnt":lambda c: str(int(c)),
                               "clk":lambda c: str(int(c)),
                               "adr":strbv,
                               "d_o":strbv,
                              },
                        cnt=cnt,
                        clk=clk,
                        adr=address,
                        d_o=data_o,
                       )

    @instance
    def tests():
        for index, tested_value in enumerate(range(min_val, max_val)):
            address.next = index
            yield delay(2)
            assert (int(mem[index]) == tested_value), "values do not match"

    return clkDriver, counter, debugger, memReader, tests


if __name__ == '__main__':
    steps=16
    inst=TestBench(steps)
    inst.run_sim(steps)
    print("simulation ran successfully!")
    help(MemController)
