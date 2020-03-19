from myhdl import block, instance, delay

@block
def Debugger(period=1, funcs={}, **kwargs):
    """
    Debugger(period=1, funcs={}, **kwargs):
        - returns a debugger instance
        - arguments:
            period: the period at which the debugger must scan the values
                type:               int > 0
                kind of argument:   PARAMETER
                default value:      1
            funcs: a dictionary containing printing functions,
                    each key provided should also be in the kwargs dictionary,
                    but not all keys need to be given.
                    it is used during the printing phase to convert the corresponding key signal to a string.
                    if no function is supplied for a specific key, the default function applied is str().
                type:               dict
                kind of argument:   PARAMETER
                default value:      {}
            kwargs: all the other arguments passed as key=value pairs
                type:               any signal that can be converted to a string.
                                    If not you can still supply a function in the funcs argument.
                kind of argument:   PARAMETER
    Example:
        debugger = Debugger(period=1,                           # the debugger will activate at every time-step
                            funcs={
                                   "cnt":lambda c: str(int(c)), # the cnt column will be converted to int the to str before display
                                   "clk":lambda c: str(int(c)),
                                   "d_o":strbv,                 # the function strbv will be used to format the d_o column
                                  },
                            cnt=Counter,                        # the Counter Signal will be displayed in the cnt column
                            clk=Clock,                          # the Clock Signal will be displayed in the clk column
                            adr=address,                        # the address Signal will be displayed in the adr column
                           )

    """
    assert (period >= 1),"period should be >=1 0"
    assert (isinstance(period, int)),"period should be an Integer >=1 0"

    print("\t".join([f"{k}" for k in kwargs]))

    @instance
    def debug():
        while True:
            print("\t".join([funcs[k](v)
                             if k in funcs
                             else str(v)
                                 for k, v in kwargs.items()
                            ]))
            yield delay(period)

    return debug

