from Algorithm.element import Element

class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        super().outAct()
        self.tnext[0] = self.tcurr + super().getDelay()
        next_element = self.get_next_element()
        next_element.inAct()
