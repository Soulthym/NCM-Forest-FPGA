from myhdl import block, instance, delay

@block
def ClkDriver(clk, period=1):
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

