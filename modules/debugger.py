from myhdl import block, always

@block
def Debugger(**kwargs):
    print("\t".join([f"{k}" for k in kwargs]))

    @always(kwargs["clk"])
    def debug():
        print("\t".join([f"{v}" for v in kwargs.values()]))

    return debug

