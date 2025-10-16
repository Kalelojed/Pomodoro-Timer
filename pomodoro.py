import tkinter as tk
from tkinter import *
import customtkinter as ctk
from PIL import *
import pyglet
import math
import pomodoroValues
from pomodoroValues import *
import pygame
import time
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Pomodoro Visual Vars
MainFont = 'MT Qeyemour'
SecondaryFont = 'Clash Grotesk'
MainFontFile = resource_path("assets/MtSerdian-Regular.ttf")
SecondaryFontFile = resource_path("assets/ClashGrotesk-Regular.ttf")
pyglet.options['win32_gdi_font'] = True
pyglet.font.add_file(MainFontFile)
pyglet.font.add_file(SecondaryFontFile)
RingtoneDirectory = 'ringtone.mp3'

#Window Colors
MainBackgroundColor = "#ffdede"
MainTextColor = "#5A1C1C"
SecondaryButtonColor = "#ffacac"
SecondaryButtonHoverColor = "#f39797"
MainButtonColor = "#ff7272"
MainButtonHoverColor = "#ce4a4a"

#Appearance and Theme
ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

#Creating the Window
app = ctk.CTk()
app.title('Pomodoro Timer')
app.geometry('400x300')
app.resizable(False, False)
app.iconbitmap(resource_path('assets/logo.ico'))
pygame.mixer.init()

RingtoneFile = resource_path(RingtoneDirectory)

def playRingtone():
    pygame.mixer.music.load(RingtoneFile)
    pygame.mixer.music.play(loops=0)

def UpdateTimerLabel():
    global SessionDuration
    if SessionDuration >= 3600:
        TimerLabelMinute.configure(text=f"{str(SessionDuration//3600).zfill(2)}:{str((SessionDuration//60)-((SessionDuration//3600)*60)).zfill(2)}:{str(SessionDuration%60).zfill(2)}")
    else:
        TimerLabelMinute.configure(text=f"{str(SessionDuration//60).zfill(2)}:{str(SessionDuration%60).zfill(2)}")

#Functions for Timer
def LoadSession(first:int):
    global SessionType, CurrentSession, FocusDuration, ShortBreakDuration, LongBreakDuration, SessionDuration, FocusDurMinutes, ShortBreakDurMinutes, LongBreakDurMinutes
    previousSessionType = SessionType
    previousSession = CurrentSession
    FocusDuration = int(FocusDurMinutes * 60)
    ShortBreakDuration = int(ShortBreakDurMinutes * 60)
    LongBreakDuration = int(LongBreakDurMinutes * 60)
    FocusOptionLabel.configure(text=str(FocusDurMinutes))
    ShortBreakOptionLabel.configure(text=str(ShortBreakDurMinutes))
    LongBreakOptionLabel.configure(text=str(LongBreakDurMinutes))
    if first == 1:
        CurrentSession = 1
        SessionType = 1
    else:
        if previousSession == CurrentSession:
            if previousSessionType == 1:
                if previousSession % 2 == 0:
                    SessionType = 3
                else:
                    SessionType = 2
            elif previousSessionType == 2 or previousSessionType == 3:
                SessionType = 1
                if previousSession == SessionCount:
                    CurrentSession=1
                else:
                    CurrentSession+=1
    if SessionType == 1:
        SessionDuration = FocusDuration
        SessionTypeLabel.configure(text='🧠 Focus Session')
    elif SessionType == 2:
        SessionDuration = ShortBreakDuration
        SessionTypeLabel.configure(text='☕ Short Break')
    elif SessionType == 3:
        SessionDuration = LongBreakDuration
        SessionTypeLabel.configure(text='☕ Long Break')
    SessionCountLabel.configure(text='Session '+str(CurrentSession)+'/'+str(SessionCount))
    UpdateTimerLabel()

def StartTimer():
    global SessionDuration, playingTimer, PlayingTimer, TimerButton, StopImage
    if SessionDuration > 0 and playingTimer == 1:
        SessionDuration -= 1
        UpdateTimerLabel()
        app.after(1000, StartTimer)
    else:
        if SessionDuration > 0:
            return
        if playingTimer == 1:
            app.after(1000, StartTimer)
        LoadSession(0)
        playRingtone()

#Function for Stopping/Starting the Timer
def StartStopTimer():
    global playingTimer
    PlayingTimer.set(True if PlayingTimer.get() == False else False)
    TimerButton.configure(image= StartImage if PlayingTimer.get() == False else StopImage)
    playingTimer = 1 if PlayingTimer.get() == True else 0
    if playingTimer == 1:
        StartTimer()

def ChangeOptions(option, value):
    global FocusDurMinutes, ShortBreakDurMinutes, LongBreakDurMinutes
    FocusDurMinutes = FocusDurMinutes - 1 if option == 1 and value == 2 else FocusDurMinutes + 1 if option == 1 and value == 1 else FocusDurMinutes
    ShortBreakDurMinutes = ShortBreakDurMinutes - 1 if option == 2 and value == 2 else ShortBreakDurMinutes + 1 if option == 2 and value == 1 else ShortBreakDurMinutes
    LongBreakDurMinutes = LongBreakDurMinutes - 1 if option == 3 and value == 2 else LongBreakDurMinutes + 1 if option == 3 and value == 1 else LongBreakDurMinutes
    FocusDurMinutes = 1 if FocusDurMinutes < 1 else FocusDurMinutes
    ShortBreakDurMinutes = 0 if ShortBreakDurMinutes < 0 else ShortBreakDurMinutes
    LongBreakDurMinutes = 0 if LongBreakDurMinutes < 0 else LongBreakDurMinutes
    FocusOptionLabel.configure(text=str(FocusDurMinutes))
    ShortBreakOptionLabel.configure(text=str(ShortBreakDurMinutes))
    LongBreakOptionLabel.configure(text=str(LongBreakDurMinutes))

def ShowHideOptions():
    ShowOptions.set(True if ShowOptions.get() == False else False)
    if ShowOptions.get() == True:
        OptionsFrame.place(x=5, y=245)
    else:
        OptionsFrame.place_forget()

#Background
BackgroundFrame = ctk.CTkFrame(app, width=300, height=400, corner_radius=0, fg_color=MainBackgroundColor)
BackgroundFrame.pack(fill='both')
BackgroundFrame.pack_propagate(False)

#TimerLabels
TimerLabelMinute = ctk.CTkLabel(BackgroundFrame, text=f"{str(SessionDuration//60).zfill(2)}:{str(SessionDuration%60).zfill(2)}", font=(MainFont, 90, 'bold'), text_color=MainTextColor, fg_color='transparent')
TimerLabelMinute.pack(expand=True)

#Start/Stop Button
PlayingTimer = tk.BooleanVar(value = False)
StartImage = ctk.CTkImage(dark_image=Image.open(resource_path('assets/start.png')), light_image=Image.open(resource_path('assets/start.png')), size=(20, 20))
StopImage = ctk.CTkImage(dark_image=Image.open(resource_path('assets/stop.png')), light_image=Image.open(resource_path('assets/stop.png')))
TimerButton = ctk.CTkButton(BackgroundFrame, image=StartImage, corner_radius=20, text='', fg_color=MainButtonColor, width=50, height=50, hover_color=MainButtonHoverColor, command=StartStopTimer)
TimerButton.place(x=160, y=190)

#Skip Button
SkipImage = ctk.CTkImage(dark_image=Image.open(resource_path('assets/skip.png')), light_image=Image.open(resource_path('assets/skip.png')), size=(20, 22))
SkipButton = ctk.CTkButton(BackgroundFrame, image=SkipImage, corner_radius=20, text='', fg_color=SecondaryButtonColor, width=40, height=50, hover_color=SecondaryButtonHoverColor, command= lambda: LoadSession(0))
SkipButton.place(x=230, y=190)

#Options Button
ShowOptions = tk.BooleanVar(value=False)
OptionsImage = ctk.CTkImage(dark_image=Image.open(resource_path('assets/options.png')), light_image=Image.open(resource_path('assets/options.png')), size=(22, 25))
OptionsButton = ctk.CTkButton(BackgroundFrame, image=OptionsImage, corner_radius=20, text='', fg_color=SecondaryButtonColor, width=40, height=50, hover_color=SecondaryButtonHoverColor, command=ShowHideOptions)
OptionsButton.place(x=90, y=190)

#Session Label
SessionTypeLabel = ctk.CTkButton(BackgroundFrame, text='🧠 Focus Session', font=(SecondaryFont, 15), text_color=MainTextColor, height=25, width=150, corner_radius=12, fg_color='transparent', border_width=2, border_color=MainTextColor, hover_color=MainBackgroundColor)
SessionTypeLabel.place(x=120, y=50)

#SessionCount Label
SessionCountLabel = ctk.CTkButton(BackgroundFrame, text='Session '+str(CurrentSession)+'/'+str(SessionCount), font=(SecondaryFont, 14), text_color=MainTextColor, height=25, width=150, corner_radius=12, fg_color='transparent', hover_color=MainBackgroundColor)
SessionCountLabel.place(x=120, y=80)

#Options GUI
OptionsFrame = ctk.CTkFrame(BackgroundFrame, width=390, height=50, fg_color=MainTextColor)

#Icons
MinusIcon = ctk.CTkImage(dark_image=Image.open(resource_path('assets/minus.png')), light_image=Image.open(resource_path('assets/minus.png')), size=(15, 15))
PlusIcon = ctk.CTkImage(dark_image=Image.open(resource_path('assets/plus.png')), light_image=Image.open(resource_path('assets/plus.png')), size=(15, 15))
#Options - Focus
OptionsFocusFrame = ctk.CTkFrame(OptionsFrame, width=120, height=40, fg_color=MainButtonColor)
OptionsFocusFrame.place(x=5, y=5)
OptionsFocusFrame.pack_propagate(False)
FocusOptionMinus = ctk.CTkButton(OptionsFocusFrame, image=MinusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(1, 2))
FocusOptionMinus.place(x=5, y=5)
FocusOptionPlus = ctk.CTkButton(OptionsFocusFrame, image=PlusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(1, 1))
FocusOptionPlus.place(x=84, y=5)
FocusOptionLabel = ctk.CTkLabel(OptionsFocusFrame, text=str(ShortBreakDurMinutes), text_color=MainBackgroundColor, font=(SecondaryFont, 25))
FocusOptionLabel.pack(expand=True)

#Options - ShortBreak
OptionsShortBreakFrame = ctk.CTkFrame(OptionsFrame, width=120, height=40, fg_color=MainButtonColor)
OptionsShortBreakFrame.place(x=134, y=5)
OptionsShortBreakFrame.pack_propagate(False)
ShortBreakOptionMinus = ctk.CTkButton(OptionsShortBreakFrame, image=MinusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(2, 2))
ShortBreakOptionMinus.place(x=5, y=5)
ShortBreakOptionPlus = ctk.CTkButton(OptionsShortBreakFrame, image=PlusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(2, 1))
ShortBreakOptionPlus.place(x=84, y=5)
ShortBreakOptionLabel = ctk.CTkLabel(OptionsShortBreakFrame, text=str(ShortBreakDurMinutes), text_color=MainBackgroundColor, font=(SecondaryFont, 25))
ShortBreakOptionLabel.pack(expand=True)

#Options - LongBreak
OptionsLongBreakFrame = ctk.CTkFrame(OptionsFrame, width=120, height=40, fg_color=MainButtonColor)
OptionsLongBreakFrame.place(x=264, y=5)
OptionsLongBreakFrame.pack_propagate(False)
LongBreakOptionMinus = ctk.CTkButton(OptionsLongBreakFrame, image=MinusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(3, 2))
LongBreakOptionMinus.place(x=5, y=5)
LongBreakOptionPlus = ctk.CTkButton(OptionsLongBreakFrame, image=PlusIcon, text='', width=30, height=30, fg_color=SecondaryButtonColor, hover_color=SecondaryButtonHoverColor, command=lambda:ChangeOptions(3, 1))
LongBreakOptionPlus.place(x=84, y=5)
LongBreakOptionLabel = ctk.CTkLabel(OptionsLongBreakFrame, text=str(ShortBreakDurMinutes), text_color=MainBackgroundColor, font=(SecondaryFont, 25))
LongBreakOptionLabel.pack(expand=True)
LoadSession(1)

app.mainloop()