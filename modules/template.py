from myhdl import block, Signal, intbv, always, instance, delay, modbv, instances
from debugger import Debugger
from clkdriver import ClkDriver
from counter import Counter
from utils import strbv

@block
def Template(clk, *args):
    """
    Template(clk, *args):
        - returns a <FILL HERE>
        - arguments:
            clk: the clock driving the reader
                type:               Signal(bool)
                kind of argument:   SENSIBILITY
            *args: <DESCRIPTION>
                type:               <TYPE>
                kind of arguments:  <SENSIBILITY,INPUT,OUTPUT,PARAMETER>
                [bitsize]:            <N/A>
    Example:
    # declare args before
    template = Template(clk)
    """

    @always(clk.posedge)
    def process():
        pass
    return instances()


@block
def TestBench(steps, *args):
    # useful values
    # clock
    clk = Signal(bool(0))
    clkDriver = ClkDriver(clk=clk,
                          period=2)

    # counter
    cnt = Signal(intbv(0, min=0, max=steps+2))
    counter = Counter(clk=clk,
                      cnt=cnt)

    # Template
    template = Template(clk=clk)

    # debugger
    debugger = Debugger(period=1,
                        funcs={"cnt":lambda c: str(int(c)),
                               "clk":lambda c: str(int(c)),
                              },
                        cnt=cnt,
                        clk=clk,
                       )

    @instance
    def tests():
        for i in range(steps):
            yield delay(1)

    return instances()


def toHDL(hdl="VHDL"):
    clk = Signal(bool(0))
    template = Template(clk=clk)
    template.convert(hdl=hdl, path='./vhdl-output/')


if __name__ == '__main__':
    steps=35
    inst=TestBench(steps)
    inst.run_sim(steps)
    print("simulation ran successfully!")
    toHDL(hdl="VHDL")
