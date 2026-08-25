import os
import sys
from os import system, name
import platform
import webbrowser
from pathlib import Path

if not platform.system().startswith("Windows"):
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
    except ImportError or ModuleNotFoundError:
        system("python3 -m pip install pillow --break-system-packages")
    try:
        from termcolor import colored, cprint
    except ImportError or ModuleNotFoundError or NameError:
        system("python3 -m pip install termcolor --break-system-packages")
        from termcolor import colored, cprint
    try:
        import pyfiglet
        import pyfiglet.fonts
    except ImportError:
        system("python3 -m pip install pyfiglet --break-system-packages")
else:
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
    except ImportError or ModuleNotFoundError:
        system("python -m pip install pillow")
    try:
        from termcolor import colored, cprint
    except ImportError or ModuleNotFoundError or NameError:
        system("python -m pip install termcolor")
        from termcolor import colored, cprint
    try:
        import pyfiglet
        import pyfiglet.fonts
    except ImportError:
        system("python -m pip install pyfiglet")

system("cls" if name == "nt" else "clear")
cprint(pyfiglet.figlet_format("IMG TO GPS"), "green")
cprint("made by mt19937 \n \n", "yellow")
cprint("PS: it is reccommended that the image has a jpg format, as finding metadata from others is rare. \n", "cyan")
cprint("Also, images from apps such as Discord or Whatsapp have their metadata wiped, meaning anything downloaded from there will not fetch anything. \n", "cyan")

path = ""

open_googlemaps = False

def user_input():
    global path
    global img
    global open_googlemaps

    try:
        if (getattr(sys, "frozen", False)):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))

        if (platform.system().startswith("Windows")):
            img_folder = Path(os.path.join(base + "\\dist\\", "img"))
        else:
            img_folder = Path(os.path.join(base + "/dist/", "img"))
        files = [file.name for file in img_folder.iterdir() if file.is_file() and file.name != ".DS_Store"]

        if (not files):
            cprint("You have no files in the images folder!", "red")
            cprint("To add some, go to dist > img and add a file. \n", "red")
            exit(0)

        for number, name in enumerate(files, start=1):
            print(f"{number}) {name}")
        print("\n")

        path_input = int(input(f"Select a file (1-{len(files)}): "))
        if (1 <= path_input <= len(files)):
            selected = path_input - 1
        else:
            cprint(f"Number must be from 1-{len(files)}!", "red")
            user_input()

        googlemaps_confirm = input("Open google maps with location if fetched? (Y/n): ")
        if (googlemaps_confirm.lower() == "y"):
            open_googlemaps = True

        path = os.path.join(base + "/dist/", "img", files[selected]) #TODO: make this more flexible

        img = Image.open(path)
    except FileNotFoundError as e:
        cprint(f"file: {e} not found! \n", "red")
        user_input()

user_input()

img_exif = img.getexif()

exif = {
    TAGS[key]: value
    for key, value in img.getexif().items()
    if key in TAGS
}

def get_degrees(value, ref):
    deg, min, sec = value
    decimal = deg + min / 60 + sec / 3600
    if ref.upper() in ["S", "W"]:
        return -decimal
    return decimal

if (exif == {}):
    cprint("No metadata found :(", "red")
elif ("GPSLatitude" in exif and "GPSLongitude" in exif):
    cprint("GPS Latitude and Longitude found! \n", "green")

    lat = get_degrees(exif["GPSLatitude"], exif["GPSLatitudeRef"])
    lon = get_degrees(exif["GPSLongitude"], exif["GPSLongitudeRef"])

    cprint(f"Latitude: {lat}", "light_green")
    cprint(f"Longitude: {lon}", "light_green")

    if (open_googlemaps):
        webbrowser.open(f"https://maps.google.com/?q={lat},{lon}")
else:
    cprint("Couldn't find Latitude and Longitude, here are some other things found: \n", "yellow")
    if ("ImageDescription" in exif):
        print("Description: " + exif["ImageDescription"])
    if ("DateTime" in exif):
        print("Date & Time: " + exif["DateTime"])
    if ("Software" in exif):
        print("Software Output: \n" + exif["Software"])

    if (all(item not in exif for item in ["ImageDescription", "DateTime", "Software"])):
        cprint("Couldn't find Description, DateTime or Software from image! \n", "red")

    if (input("Get all metadata? (Y/n): ").lower() == "y"):
        for id in exif:
            name = TAGS.get(id, id)
            value = exif.get(id)
            print(f"{name:25}: {value}")