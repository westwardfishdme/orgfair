# 7968 Org Fair Membership Form
This repository hosts the python script used to get user information
using python-curses.
![image of sample](./images/orgfair.png)

## Features
- Includes an auto-checker for the email field to ensure that users input valid **luc.edu** emails.
- Automatically formats text in the csv to be a capitalized name for easy exports to emails.
- saves all information to `members.csv`

## Potentially Planned Features
There is no CLI implementation yet, but some future additions may include:
- SMTP integration to automatically send out emails from the exported .csv file.
- Better SIGWINCH handling; screen must remain statically sized for duration of runtime.


