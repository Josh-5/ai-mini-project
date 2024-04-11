#follow to install pytience
#https://pypi.org/project/pytience/
# Here's another option to run the solitaire game

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess
import os

def main():
    inpipe = os.open("input.txt", os.O_RDONLY | os.O_CREAT)
    outpipe = os.open("output.txt", os.O_WRONLY | os.O_CREAT)
    print(inpipe)
    print(outpipe)
    game = subprocess.Popen(["klondike"], stdin=inpipe, stdout=outpipe)
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
    """

    os.close(inpipe)
    os.close(outpipe)


if __name__ == "__main__":
    main()