#follow to install pytience
#https://pypi.org/project/pytience/

#follow this to install pytorch
#https://pytorch.org/get-started/locally/

# Use subprocess to interact: https://docs.python.org/3/library/subprocess.html

import subprocess

def main():
    pipe = [0,1]
    game = subprocess.Popen(["klondike"])
    """
    https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
    """
    communicate("help")


   

    


if __name__ == "__main__":
    main()