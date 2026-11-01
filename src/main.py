#!/usr/bin/env python3
import curses
import sys
import time
from curses.textpad import Textbox
from enum import Enum


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Member:
    def __init__(self):
        self.first_name: str = None
        self.last_name: str = None
        self.email: str = None

    def set_first_name(self, value):
        self.first_name = value

    def set_last_name(self, value):
        self.last_name = value

    def set_email(self, value):
        self.email = value

    def csv(self) -> str:
        """
        returns the user information out to a csv formatted
        string.
        """
        return f"{
            self.first_name.lower().capitalize()},{
            self.last_name.lower().capitalize()},{
            self.email}\n"


def write_to_file(member: Member):
    try:
        with open("./members.csv", 'r') as file:
            file.close()
    except FileNotFoundError:
        with open("./members.csv", 'w') as file:
            file.write("first name,last name,luc email\n")
        file.close()

    with open("./members.csv", 'a') as file:
        file.write(member.csv())
        file.close()


def verify_email(email: str) -> (bool, str):
    """
    Ensures that the user put in a valid LUC email.
    returns a string and an error message.
    """
    valid = (True, "")
    email_split: list[str] = email.split('@', 1)
    # if the user didn't put the @ sign
    if email_split.__len__() < 2:
        msg = "Missing a field: @luc.edu"
        return (False, msg)
    if email_split[0].lower == '':
        msg = "Missing a field: please enter your LUC username"
        return (False, msg)

    # user put in a bad email
    if email_split[1].lower() != "luc.edu":
        msg = "This email is not a valid luc.edu email."
        valid = (False, msg)

    return valid


class WindowDetails:
    def __init__(self, screen):
        self.max_x = screen.getmaxyx()[1]
        self.max_y = screen.getmaxyx()[0]

    def center_x(self) -> int:
        return self.max_x // 2

    def center_y(self) -> int:
        return self.max_y // 2


def get_longest_string(strlist: list[str]) -> (int, int):
    """
    gets the longest string in a list and
    returns the index and length in the format:
    -> (idx, len)
    """
    largest = 0
    index = 0
    for i, string in enumerate(strlist):
        len = string.__len__()
        if len > largest:
            largest = len
            index = i

    return (index, largest)


class Fields(Enum):
    FIRST = "What is your first name?: "
    LAST = "What is your last name?: "
    EMAIL = "What is your student email? (case sensitive): "


def draw_logo(screen, window: WindowDetails):

    # print 7968 logo in the top right.
    padding_content = [
        "░██████████    ██████        ████      ██████░",
        "░██      ██  ██      ██    ██        ██      ██░",
        "         ██  ██      ██  ██          ██      ██░",
        "       ██      ████████  ████████      ██████░",
        "    ░██              ██  ██      ██  ██      ██░",
        "    ░██            ██    ██      ██  ██      ██░",
        "    ░██        ████        ██████      ██████░",
    ]
    longest = get_longest_string(padding_content)
    for i, string in enumerate(padding_content):
        screen.addstr(5+i, window.max_x-longest[1]-20, string)
    screen.refresh()


def main() -> bool:
    """
    Main curses function.
    """
    screen = curses.initscr()
    window = WindowDetails(screen)
    curses.cbreak()
    curses.noecho()
    screen.keypad(True)
    screen.clear()

    draw_logo(screen, window)
    # get user information
    init_y = window.center_y() - [member.value for member in Fields].__len__()
    member = Member()
    # title
    title = "========= 7968 Membership Form ========="
    screen.addstr(init_y, window.center_x() - title.__len__(), title)
    # move down a line
    init_y += 1

    count = 0
    while count < 3:
        field = [member.value for member in Fields]
        string_x_coord = window.center_x()-title.__len__()-10
        # print the asked field
        screen.addstr(init_y, string_x_coord, field[count])
        screen.refresh()

        # create the text input field
        box_location = (init_y, string_x_coord+len(field[count]))
        win = curses.newwin(1, window.max_x // 2,
                            box_location[0], box_location[1])
        box = Textbox(win)
        # catch bad input
        badinput: bool = False
        try:
            box.edit()

        except KeyboardInterrupt:
            curses.nocbreak()
            curses.echo()
            curses.endwin()
            eprint("saved to file members.csv")
            exit(0)

        input_field = box.gather().strip()
        if input_field == "":
            screen.addstr(
                box_location[0], box_location[1], "please enter a value")
            screen.refresh()
            time.sleep(0.5)
            badinput = True

        match count:
            case 0:  # first name
                member.set_first_name(input_field)
            case 1:  # last name
                member.set_last_name(input_field)
            case 2:  # email
                input_field.replace(" ", '')
                verification_result = verify_email(input_field)
                # for email, verify the
                if verification_result[0]:
                    member.set_email(input_field)
                else:
                    msg = verification_result[1]
                    screen.addstr(
                        init_y+1, window.center_x(), msg)
                    badinput = True

        if not badinput:
            count += 1
            init_y += 1

    screen.move(init_y, window.center_x())
    screen.clrtoeol()
    screen.addstr(init_y, window.center_x()-len(title),
                  "is the information above correct? [y/n]")
    screen.refresh()
    try:
        if screen.getkey().lower() == "y":
            write_to_file(member)
            screen.move(init_y, window.center_x())
            screen.clrtoeol()
            msg = "Thank you for joining! " +\
                "We will send you an email later tonight!"
            screen.addstr(init_y, string_x_coord,
                          msg)
            screen.refresh()
            time.sleep(3)

    except KeyboardInterrupt:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        exit(0)
    return True


if __name__ == "__main__":
    # start curses:
    try:
        while True:
            main()

        curses.nocbreak()
        curses.echo()
        curses.endwin()
        eprint("saved to file members.csv")

    except Exception as e:
        eprint(f"code experienced an error:\n{e}")
        exit(1)
