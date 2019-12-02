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
    event2 = None
    cevent = None

    def __init__(self, **kwargs):
        super(SoundBoard, self).__init__(**kwargs)
        for i in range(1, 26):
            self.ids.board.add_widget(Button(id="b" + str(i), on_press=lambda instance: self.call(i, SoundLoader.load('sounds/quack.wav'))))

    def m_play(self, dt):
        self.m.play()

    def mup_play(self, dt=0):
        self.mup.play()

    def metB(self):
        global event, event2, cevent
        self.mTrue = not self.mTrue
        if self.mTrue:
            self.metro.background_color = [255, 0, 0, 1]
            self.mup_play()
            # event = Clock.schedule_interval(self.mup_play, 1 / self.slider.value * 4)
            event2 = Clock.schedule_interval(self.m_play, 1 / self.slider.value)
        else:
            self.metro.background_color = [1, 1, 1, 1]
            # event.cancel()
            event2.cancel()

    def call(self, t, s):
        s.pitch = 0.5 + 0.06*t
        s.play()

    def met(self, dt):
        global event, event2


class MiniatureSoundBoardApp(App):
    def build(self):
        return SoundBoard()


if __name__ == "__main__":
    MiniatureSoundBoardApp().run()
