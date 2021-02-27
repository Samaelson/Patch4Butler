#!/usr/bin/python
import sys
import os

search_gcode_string = '.gcode'

def find_append_to_file(filename, find, insert):
    """Find and append text in a file."""
    with open(filename, 'r+') as file:
        lines = file.read()

        index = repr(lines).find(find) - 1
        if index < 0:
            raise ValueError("The text was not found in the file!")

        len_found = len(find) - 1
        old_lines = lines[index + len_found:]

        file.seek(index)
        file.write(insert)
        file.write(old_lines)
# end find_append_to_file


def printInfo():
    print ('Applies additional skirt addon to gcode file.\n')
    print ('Syntax:')
    print ('  GcodeSkirtMultiplier_v002.py Source [Offset] [Skirt Hight]')
    print ('\n    Source        Gcode file to be patched')
    print ('    Offset        Value for offset where skirt addon starts\n')
    print ('    Skirt Hight   Hight of the skirt in mm\n')
    return;

def main(argv):

    # check if argvx is set correctly
    # try to retrieve source file name
    try:
        sourcefile = str(argv[1])
    except IndexError:
        print ('ERROR: Syntax error argument 1\n')
        printInfo()
        sys.exit()
    	
    # check if argv1 syntax is correction
    if sourcefile == '/?':
        printInfo()
        sys.exit()
    elif sourcefile.find(search_gcode_string, 0) == -1:
        print ('ERROR: Syntax error argument 1\n')
        printInfo()
        sys.exit()	
	
	# check if file exists and is not empty
    try:
        if os.stat(sourcefile).st_size == 0:
            print ('ERROR: Source file empty\n')
            printInfo()
            sys.exit()
    except (OSError, IOError) as e:
        print ('ERROR: Open source file failed\n')
        printInfo()
        sys.exit()	

    print ('Patch process step #1: Engage after wipe tower first layer...')

    with open(sourcefile, "r") as in_file:
        buf = in_file.readlines()

    with open(sourcefile, "w") as out_file:
        for line in buf:
            if line == "; CP WIPE TOWER FIRST LAYER BRIM START\n":
                line = line + "V1 ;engage filament\nM300\n"
            out_file.write(line)

    print ('Done!\nPatch process step #2: Disengage for toolchange unload...')
	
    with open(sourcefile, "r") as in_file:
        buf = in_file.readlines()

    with open(sourcefile, "w") as out_file:
        for line in buf:
            if line == "; CP TOOLCHANGE UNLOAD\n":
                line = line + "V0 ;disengage filament\nM300\nM300\n"
            out_file.write(line)

    print ('Done!\nPatch process step #3: Engage right after toolchange unload...')

    with open(sourcefile, "r") as in_file:
        buf = in_file.readlines()

    with open(sourcefile, "w") as out_file:
        for line in buf:
            if line == "; CP TOOLCHANGE WIPE\n":
                line = line + "V1 ;engage filament\nM300\n"
            out_file.write(line)

    print ('Done!\nPatch process step #4: Disengage after print...')

    with open(sourcefile, "r") as in_file:
        buf = in_file.readlines()

    with open(sourcefile, "w") as out_file:
        for line in buf:
            if line == "; Filament-specific end gcode\n":
                line = line + "V0 ;disengage filament\nM300\nM300\n"
            out_file.write(line)

    print ('Done!\nPatch process finished!\n')


if __name__ == "__main__":
    main(sys.argv)