from myhdl import block, instance, delay

@block
def ClkDriver(clk, period=2):
    """
    ClkDriver(clk, period):
        - returns a clock driver
        - arguments:
            clk: the clock you want to drive
                type:               Signal(bool)
                kind of argument:   INPUT
            period: the period of the clock
                type:               int > 0
                kind of argument:   PARAMETTER
                default value:      2
        This class produces un-synthetizable code and ought to be used only in simulation!
    Example:
        clk = Signal(bool(0))
        clkDriver = ClkDriver(clk=clk,
                              period=2)
        # this will cause the clk Signal to go from True to False and vice-versa every simulation step.
        # It can go down to a period of 1, but then you would not be able to see one of the states of the clock.
    """
    assert (period >= 1),"period should be >=1 0"
    assert (isinstance(period, int)),"period should be an Integer >=1 0"
    lowTime = int(period/2)
    highTime = period - lowTime

    @instance
    def driveClk():
        while True:
            clk.next = True
            yield delay(lowTime)
            clk.next = False
            yield delay(highTime)
    return driveClk

