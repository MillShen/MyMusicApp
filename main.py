import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class SoundBoard(Widget):
    filename = 'bees'
    sound = SoundLoader.load('sounds/' + filename + '.wav')
    mup = SoundLoader.load('sounds/mup.wav')
    m = SoundLoader.load('sounds/m.wav')
    mTrue = False
    metro = ObjectProperty(None)
    sig = ObjectProperty(None)
    tbox = ObjectProperty(None)
    slidelabel = ObjectProperty(None)
    sample = ObjectProperty(None)
    loader = ObjectProperty(None)
    lb = ObjectProperty(None)
    rb = ObjectProperty(None)
    slider_val = NumericProperty(3)
    validnames = ["bees", "berniebass", "gamelan", "kick", "m", "mup", "pluck", "quack", "roller", "smooth", "wurlitzer"]
    reasonstolive = {'reason1': None, 'reason2': "Tim Hickey"}

    event = 0
    beat = 1
    timesig = 4

    def __init__(self, **kwargs):
        """Inits the board"""
        super(SoundBoard, self).__init__(**kwargs)

        slide = Slider(min=0.5, max=5, value=3, step=0.05, orientation='vertical', size_hint_y=15)
        slide.fbind('value', self.on_slider_val)

        self.label = Label(text=str(int(self.slider_val*60)) + ' bpm', size_hint_y=1)

        self.ids.slidesection.add_widget(self.label)
        self.ids.slidesection.add_widget(slide)

    def on_slider_val(self, instance, val):
        """Keeps track of the value of a slider and performs a method instead of having to call on a button press"""
        self.label.text = str(int(val*60)) + ' bpm'
        self.slider_val = val

    def playtick(self, dt=0):
        """Logic to play the different metronome beats every nth note"""
        global beat, timesig
        if self.beat == 1:
            self.m.play()
        else:
            self.mup.play()
            self.beat += 1
        if self.beat > self.timesig:
            self.beat = 1

    def metB(self):
        """Starts or stops the metronome based on button push and a logic flip flop"""
        global event
        self.mTrue = not self.mTrue

        if self.mTrue:
            self.metro.background_color = [255, 0, 0, 1]
            event = Clock.schedule_interval(self.playtick, 1 / self.slider_val)
        else:
            self.metro.background_color = [1, 1, 1, 1]
            event.cancel()
            self.beat = 1

    def submit(self):
        """Sends the information in the text box to the metronome"""
        if self.sig.text and self.sig.text.isdigit():
            self.timesig = int(self.sig.text)
            self.tbox.text = str(self.sig.text) + "/4 time"
            self.sig.text = ""
        else:
            self.sig.text = ""

    def initbutton(self):
        """Loads the soundboard with the audio file"""

        if self.sample.text and self.sample.text in self.validnames:
            self.filename = self.sample.text
            self.sample.text = ""
            self.addbuttons()

        elif self.sample.text and self.sample.text not in self.validnames:
            self.loader.text = "Invalid filename"
            self.sample.text = ""

        else:
            self.addbuttons()

    def addbuttons(self):
        """Adds buttons to screen"""
        for i in list(range(1, 26)):
            s = SoundLoader.load('sounds/' + self.filename + '.wav')

            def p(self, n=i):
                s.pitch = 0.5 + 0.06 * n
                s.play()

            self.ids.board.add_widget(Button(on_press=p))

        self.loader.text = self.filename + ".wav is loaded"
        self.rb.disabled = False
        self.lb.disabled = True

    def removebuttons(self):
        """Removes buttons to allow loading again"""
        self.lb.disabled = False
        k = self.ids.board.children
        if k:
            for i in k:
                self.ids.board.remove_widget(i)
            if k:
                self.removebuttons()
        self.rb.disabled = True



class MiniatureSoundBoardApp(App):
    def build(self):
        return SoundBoard()


if __name__ == "__main__":
    MiniatureSoundBoardApp().run()