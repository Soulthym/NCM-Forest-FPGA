from myhdl import block, always

@block
def Counter(clk, cnt):
    """
    Counter(clk, cnt):
        - returns a counter
        - arguments:
            clk: the clock driving the counter
                type:               Signal(bool)
                kind of argument:   SENSIBILITY
            cnt: the Signal counting the number of clocks
                type:               Signal(intbv) > 0 OR Signal(modbv) > 0
                kind of argument:   OUTPUT
    Example:
    cnt = Signal(modbv(0, min=0, max=100))
    counter = Counter(clk=clk,              # clock Signal
                      cnt=cnt)
    """
    @always(clk)
    def count():
        cnt.next = cnt+1

    return count
