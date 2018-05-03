import sys, tty, termios, time


# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch




# Instructions for when the user has an interface
print("w/s: acceleration")
print("a/d: steering")
print("l: lights")
print("x: exit")

# Infinite loop that will not end until the user presses the
# exit key
while True:
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()
    cmd = ''
    if(char == "w"):
       cmd += 'w'
    if(char == "a"):
       cmd += 'a'

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        print("Program Ended")
        break

    print(cmd)
  
    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""

