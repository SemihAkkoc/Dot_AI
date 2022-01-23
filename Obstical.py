class Obstical:
    def __init__(self, main_window, state=0):
        self.main_window = main_window
        self.state = state
        self.color = 'black'
        self.thickness = 20
        self.obsticals = []
        self.construct()

    def construct(self):
        if self.state == 0:
            # without any obsticals
            pass

        elif self.state == 1:
            # two holes in the corners like this ->   ---
            self.obsticals.append(self.main_window.create_rectangle(200, 300, 600, 300+self.thickness, fill=self.color))
        
        elif self.state == 2:
            # two paralel lines top of each other -> ---- \n\t----
            self.obsticals.append(self.main_window.create_rectangle(0, 150, 550, 150+self.thickness, fill=self.color))
            self.obsticals.append(self.main_window.create_rectangle(250, 350, 800, 350+self.thickness, fill=self.color))
       
        elif self.state == 3:
            # just a hole in the right side like this -> ----- --- 
            self.obsticals.append(self.main_window.create_rectangle(0, 300, 500, 300+self.thickness, fill=self.color))
            self.obsticals.append(self.main_window.create_rectangle(600, 300, 800, 300+self.thickness, fill=self.color))

        else:
            # just a hole in the right side like this -> -- -- -- 
            self.obsticals.append(self.main_window.create_rectangle(0, 300, 200, 300+self.thickness, fill=self.color))
            self.obsticals.append(self.main_window.create_rectangle(300, 300, 500, 300+self.thickness, fill=self.color))
            self.obsticals.append(self.main_window.create_rectangle(600, 300, 800, 300+self.thickness, fill=self.color))
