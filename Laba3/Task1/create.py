from element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + super().getDelay()
        nextEl = self.get_next_element()
        nextEl.inAct()
