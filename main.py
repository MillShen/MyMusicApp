import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class SoundBoard(Widget):
    filename = 'quack'
    sound = SoundLoader.load('sounds/' + filename + '.wav')
    mup = SoundLoader.load('sounds/mup.wav')
    m = SoundLoader.load('sounds/m.wav')
    mTrue = False
    slider = ObjectProperty(None)
    metro = ObjectProperty(None)
    event = None
    cevent = None
    beat = 1
    timesig = 4

    def __init__(self, **kwargs):
        super(SoundBoard, self).__init__(**kwargs)
        for i in range(1, 26):
            self.ids.board.add_widget(Button(id="b" + str(i), on_press=lambda instance: self.call(i, SoundLoader.load('sounds/quack.wav'))))

    def playtick(self, dt=0):
        global beat
        if self.beat==1:
            self.m.play()
        else:
            self.mup.play()
        self.beat+=1
        if self.beat>self.timesig:
            self.beat=1

    def metB(self):
        global event
        self.mTrue = not self.mTrue
        if self.mTrue:
            #self.metro.background_color = [255, 0, 0, 1]  #temporary: need to make buttons colored
            event = Clock.schedule_interval(self.playtick, 1 / self.slider.value*1.2)
        else:
            self.metro.background_color = [1, 1, 1, 1]
            event.cancel()

    def call(self, t, s):
        s.pitch = 0.5 + 0.06*t
        s.play()


class MiniatureSoundBoardApp(App):
    def build(self):
        return SoundBoard()

if __name__ == "__main__":
    MiniatureSoundBoardApp().run()
