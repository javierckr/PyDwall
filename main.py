#!/usr/bin/env python3

import sys, datetime, os

# Get arguments
import argparse

# Pywal
import pywal

# Use of wildcards for image extension
import glob


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

        # Set the wallpaper.
        pywal.wallpaper.change(image)
        # Reload xrdb, i3 and polybar.
        pywal.reload.env()

    def wall_set(image):
        # Validate image and pick a random image if a
        # directory is given below.
        image = pywal.image.get(image)
        # Set the wallpaper.
        pywal.wallpaper.change(image)

    if args.pywal:
        pywall_set(glob.glob(wdir + "/" + args.style + "/" + str(now) + "*")[0])
        if args.cron:
            cron(args.style + " -p", args.firefox)
        return "Wallpaper changed with pywal 😃"
    else:
        wall_set(glob.glob(wdir + "/" + args.style + "/" + str(now) + "*")[0])
        if args.cron:
            cron(args.style, args.firefox)
        return "Wallpaper changed"


## Creates the cron
def cron(style, firefox):
    f = open("/etc/cron.d/pydwall", "w")
    f.write(
        "\n0 * * * * "
        + os.getenv("SUDO_USER")
        + " /usr/local/bin/pydwall "
        + style
        + " && /usr/local/bin/pywalfox update"
        + "\n "
        if firefox
        else "\n0 * * * * "
        + os.getenv("SUDO_USER")
        + " /usr/local/bin/pydwall "
        + style
        + "\n "
    )
    f.close()
    os.chmod("/etc/cron.d/pydwall", 0o644)


## Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("style", help="Name of the style to apply")
    parser.add_argument(
        "-p", "--pywal", action="store_true", help="Set wallpaper using pywal"
    )
    parser.add_argument(
        "-c",
        "--cron",
        action="store_true",
        help="Change wallpaper every hour. Need sudo!",
    )
    parser.add_argument(
        "-f",
        "--firefox",
        action="store_true",
        help="Only use with -c option, cron also updates pywalfox(pywal for firefox)",
    )
    args = parser.parse_args()
    try:
        print(Dwall(args))
    except IOError as e:
        if e.errno == 13:
            sys.exit("You need root permissions to create a system cron file!")
    except:
        parser.print_usage()
        sys.exit("Style not found ¯\_(ツ)_/¯")


if __name__ == "__main__":
    main()
