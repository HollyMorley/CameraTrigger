from termcolor import colored
# import colorama
import os
os.system('color')
# colorama.init()

class GetFileInfo():
    def __init__(self):
        # print(colored("********************************************************\nEnter the following details to set up experiment for recording...\n********************************************************",
        #       'red', attrs=['bold']))
        print(colored("*******************************************************************                              ", 'grey', 'on_white'))
        print(colored("Enter the following details to set up the experiment for recording...                            ", 'grey', 'on_white'))
        print(colored("(WARNING: be careful with spelling)                                                              ", 'grey', 'on_white'))
        print(colored("*******************************************************************                              ", 'grey', 'on_white'))

    def get_mouseID(self):
        self.mouseID = input(colored("Mouse ID number \n(e.g. FAA-1034968):", 'cyan'))
        return self.mouseID

    def get_mousename(self):
        self.mousename = input(colored("Mouse name \n(e.g. None, L, R, LR):", 'green'))
        return self.mousename

    def get_expname(self):
        self.expname = input(colored("Experiment name \n(e.g. Test, Training; ApaChar; ApaPer; ApaVmt):", 'yellow'))
        return self.expname

