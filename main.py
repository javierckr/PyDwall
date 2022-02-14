#!/usr/bin/env python3

import sys, datetime, os

# Get arguments
import argparse

# Check if binary exists
from shutil import which

# Pywal
import pywal

# Use of wildcards for image extension
import glob


## Prerequisite
def prerequisite(dependencies):
    for dependency in dependencies:
        if not which(dependency):
            return dependency

    return True


## Dwall program namespace
def Dwall(args):
    """Dynamic Wallpaper : Set wallpapers according to current time."""

    ## Wallpaper directory
    wdir = "/usr/share/dynamic-wallpaper/images"
    ## Current hour
    now = datetime.datetime.now().hour


    def pywall_set(image):
        # Validate image and pick a random image if a
        # directory is given below.
        image = pywal.image.get(image)

        # Return a dict with the palette.
        # Set quiet to 'True' to disable notifications.
        colors = pywal.colors.get(image)

        # Apply the palette to all open terminals.
        # Second argument is a boolean for VTE terminals.
        # Set it to true if the terminal you're using is
        # VTE based. (xfce4-terminal, termite, gnome-terminal.)
#        pywal.sequences.send(colors, False)
        pywal.sequences.send(colors)

        # Export all template files.
        pywal.export.every(colors)

        # Export individual template files.
        pywal.export.color(colors, "xresources", os.environ["HOME"] + "/.Xresources")
        pywal.export.color(colors, "shell", os.environ["HOME"] + "/colors.sh")

        # Reload xrdb, i3 and polybar.
        pywal.reload.env()

        # Reload individual programs.
        pywal.reload.i3()
        pywal.reload.polybar()
        pywal.reload.xrdb()

        # Set the wallpaper.
        pywal.wallpaper.change(image)

    if args.pywal:
            pywall_set(glob.glob(wdir + "/" + args.style + "/" + str(now) + "*")[0])
            return "Wallpaper changed with pywal 😃"
    else:
        print("hola")


# print(prerequisite(["feh"]))

## Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("style", help="Name of the style to apply")
    parser.add_argument(
        "-p", "--pywal", action="store_true", help="Set wallpaper using pywal"
    )
    args = parser.parse_args()
    try:
        print(Dwall(args))
    except:
        print("Style not found ¯\_(ツ)_/¯")
        parser.print_usage()


if __name__ == "__main__":
    main()
