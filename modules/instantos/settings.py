#!/usr/bin/env python3

#############################################
## main menu of the instantOS settings app ##
#############################################

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import pathlib
import subprocess
import webbrowser
import os

# won't show icons otherwise
settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True

def getsetting(settingname):
    sprocess = subprocess.Popen(["iconf", "-i", settingname])
    sprocess.communicate()
    if sprocess.returncode == 0:
        return True
    else:
        return False

conky = not getsetting("noconky")
logo = not getsetting("nologo")
theming = not getsetting("notheming")
wifi = getsetting("wifiapplet")
desktop = getsetting("desktop")

class Handler:
    def window_destroy_cb(self, *args):
        Gtk.main_quit()
    def cancelbutton_clicked_cb(self, button):
        Gtk.main_quit()
    def okbutton_clicked_cb(self, button):
        applysettings()
        Gtk.main_quit()
    
    def applybutton_clicked_cb(self, button):
        applysettings()

    def editbutton_clicked_cb(self, button):
        os.system('urxvt -e "nvim" -c ":e ~/.instantautostart" &')

    def themeswitch_state_set_cb(self, button, state):
        global theming
        theming = state
    def wifiswitch_state_set_cb(self, button, state):
        global wifi
        wifi = state
    def logoswitch_state_set_cb(self, button, state):
        global logo
        logo = state
    def conkyswitch_state_set_cb(self, button, state):
        global conky
        conky = state
    def desktopswitch_state_set_cb(self, button, state):
        global desktop
        desktop = state


def applysettings():
    print(wifi)
    if not conky:
        os.system("iconf -i noconky 1")
    else:
        os.system("iconf -i noconky 0")

    if not theming:
        os.system("iconf -i notheming 1")
    else:
        os.system("iconf -i notheming 0")
    if not logo:
        os.system("iconf -i nologo 1")
    else:
        os.system("iconf -i nologo 0")

    if wifi:
        os.system("iconf -i wifiapplet 1")
        os.system("nm-applet &")
    else:
        os.system("pkill nm-applet &")
        os.system("iconf -i wifiapplet 0")

    if desktop:
        os.system("iconf -i desktop 1")
    else:
        os.system("iconf -i desktop 0")


builder = Gtk.Builder()

builder.add_from_file(os.path.dirname(
    os.path.realpath(__file__)) + "/instantos.glade")

builder.connect_signals(Handler())
builder.get_object("desktopswitch").set_active(desktop)
builder.get_object("conkyswitch").set_active(conky)
builder.get_object("wifiswitch").set_active(wifi)
builder.get_object("logoswitch").set_active(logo)
builder.get_object("themeswitch").set_active(logo)

window = builder.get_object('window')
window.show_all()

Gtk.main()
