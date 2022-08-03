#!/bin/python3

# Packages
import os
import shutil

# Variables
path       = "/home/risiz/Music"    # Path to store the music
file       = "urls.dow"             # File containing urls
block      = []                     # List that will contain the processed datas
counter    = 0                      # Number of music installed
errors     = []                     # Music that failed to install
compleated = []                     # Music that installed without errors

def main():
    # global variables
    global file
    global counter

    # Actual process
    processing(file)

    for music in block:
        install(music)
        counter += 1

    if len(compleated) > 0:
        print("\n\n# Compleated")
        for music in compleated:
            print(f"* {music}")

    if len(errors) != 0:
        print("\n\n# Errors")
        for error in errors:
            print(f"* {error}")
        print("\n100% Compleated with errors!!")
    else:
        print("\n100% Compleated!!")

# Processes the install file and seperated it into chunks for individual music installing
def processing(file):
    # global variables
    global block
    
    # local variables
    segment  = []
    content  = ""
    counter  = 1

    # reading the urls.dow file
    with open(f"{file}", "rt") as urls:
        file = urls.read()

    # first stage of processing
    for word in file:
        if word == ">":
            segment.append(content)
            content = ""
            continue
        content = content + word

    # second stage of processing
    for content in segment:
        item = content.split("\n")
        block.append(item)

    del block[0]

# Installs the music
def install(music):
    # global variable
    global counter

    # local variable
    creator = music[1]
    title   = music[2]
    url     = music[3]
    try:
        ft  = music[4]
    except IndexError:
        ft  = ""
    output  = f"{creator} - {title} (ft. {ft})" if ft != "" else f"{creator} - {title}"
    items   = len(block)
    percent = int((counter / items) * 100)

    if check(creator, output):
        return 0

    # reporing and installing
    print(f'installing: {title}')
    print(f'{percent}% compleated!!\n')
    os.system(f'youtube-dl -x --audio-format mp3 --audio-quality 0 {url} -o "{output}.%(ext)s"')

    # managing the installed music
    manage(creator, output) 

def check(creator, output):
    # global variables(s)
    global path

    # local variables(s)
    creator_dir = f"{path}/{creator}"
    music = f"{path}/{creator}/{output}.mp3"

    # Creating a directory for the creator if it doesn't exist already
    if not os.path.isdir(creator_dir):
        os.mkdir(creator_dir)
        return False

    if os.path.exists(music):
        print(f'Already installed: {output}')
        return True
    else:
        return False

# Puts the music in it's seperate folder
def manage(creator, name):
    # global variable(s)
    global path
    global errors
    global compleated

    # local variable(s)
    destination = f"{path}/{creator}"
    source      = f"./{name}.mp3"

    # Moving the file into it's respective directory
    try:
        shutil.move(source, destination)
        compleated.append(f"Installed: '{name}'.")
    except FileNotFoundError:
        errors.append(f"Couldn't install: '{name}'.")


if __name__ == "__main__":
    main()
