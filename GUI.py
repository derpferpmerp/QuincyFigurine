import numpy as np
import PySimpleGUI as sg
from colour import Color

from comms import create as generate


sg.theme("Black")


def border(elem, CLR="white"):
    return sg.Column([[elem]], background_color=CLR)


class Font:
    def __init__(self, fontName, fontSize=12):
        self.fontSize = str(fontSize)
        self.fontString = fontName
        self.bold = self.BOLD()
        self.italic = self.ITALIC()
        self.underline = self.UNDERLINE()

    def BOLD(self): return (self.fontString + " bold", self.fontSize)

    def ITALIC(self): return (self.fontString + " italic", self.fontSize)

    def UNDERLINE(self): return (self.fontString + " underline", self.fontSize)

    def CUSTOM(self, STR): return (self.fontString + " " + STR, self.fontSize)

    def __call__(self, method=None):
        if method == "bold":
            return self.BOLD()
        elif method == "italic":
            return self.ITALIC()
        elif method == "underline":
            return self.UNDERLINE()
        elif method == None:
            return self.fontString
        else:
            return self.CUSTOM(method)

def recursivelyAdd(lyout, DCT, SLIDER_KEYS={}):
    for k, v in list(DCT.items()):
        SLIDER_KEYS[f"_RIGHT_{k}"] = f"-{k} SLIDER-"
        lyout.append([
            sg.Text(k, auto_size_text=True),
            sg.Slider(
                range=v[0],
                enable_events=True,
                default_value=v[1],
                key=f"-{k} SLIDER-",
                orientation="h",
                size=(20, 10),
                disable_number_display=True,
            ),
            sg.Text(
                str(v[0][1]), key=f"_RIGHT_{k}", font=SLIDER_TEXT(
                "bold",
                ), auto_size_text=True,
            ),
        ])
    return lyout, SLIDER_KEYS

def addTitle(lyout, text, qsize=(10, 1), nunder=30):
    lyout.append([
        [sg.Text("_"*nunder)],
        [
            sg.Text(
                text, size=qsize,
                justification="center", font=TITLE_OBJECT("bold"),
            ),
        ],
        [sg.Text("\u00AF"*nunder)],
    ])
    return lyout

FONT_OBJECT = Font("Helvitica", fontSize=12)
TITLE_OBJECT = Font("Helvitica", fontSize=20)
SLIDER_TEXT = Font("Helvitica", fontSize=8)
BOLD_TITLE = FONT_OBJECT("bold")

presets = {
    "Starting Round": ((1, 300), 1),
    "Final Round": ((1, 300), 5),
    "Sellback Percent": ((0, 100), 95),
    "Rounding Digits": ((0, 5), 0)
}

layout = []
layout = addTitle(layout, "Figurine Profit Calculator", qsize=(30, 1), nunder=55)
layout, SLIDER_KEYS = recursivelyAdd(layout, presets)
layout += [
    [
        sg.Text("Game Mode", auto_size_text=True),
        sg.Combo(
            ["Easy", "Medium", "Hard", "Impoppable"],
            default_value="Medium",
            size=(20, 10),
            enable_events=True,
            readonly=True,
            key='-Game Mode-'
        )
    ]
]

layout.append([sg.Button("Run Calculator")])
window = sg.Window(
    title="Figurine Calculator",
    layout=layout,
    margins=(100, 50),
    element_justification="center",
)

DATA = {
    "GAME_MODE": "Medium",
    "STARTING_ROUND": 1,
    "FINAL_ROUND": 5,
    "SELLBACK_PERCENT": 0.95,
    "ROUNDING_DIGITS": 0
}


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: break
    elif event == "Run Calculator":
        total_profit = generate(DATA)
        
    elif event == "-Starting Round SLIDER-":
        MIN = values["-Starting Round SLIDER-"]
        DATA["STARTING_ROUND"] = int(MIN)
        window["-Final Round SLIDER-"].Update(range=(MIN + 1, max(300, MIN + 50)))
    elif event == "-Final Round SLIDER-":
        final_round = values["-Final Round SLIDER-"]
        DATA["FINAL_ROUND"] = int(final_round)
    elif event == "-Sellback Percent SLIDER-":
        value = int(values["-Sellback Percent SLIDER-"])
        DATA["SELLBACK_PERCENT"] = value/100
    elif event == "-Rounding Digits SLIDER-":
        value = int(values["-Rounding Digits SLIDER-"])
        DATA["ROUNDING_DIGITS"] = value
    elif event == "-Game Mode-":
        DATA["GAME_MODE"] = values["-Game Mode-"]
    for UTEXT, SLID in list(SLIDER_KEYS.items()):
        if window.Element(UTEXT) == None or values == None or values[SLID] == None:
            continue
        window.Element(UTEXT).Update(int(values[SLID]))

window.close()