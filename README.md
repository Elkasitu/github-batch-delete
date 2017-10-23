# GitHub batch delete

This project takes advantage of Selenium webdriver's abilities to make it
possible to batch-delete repositories.

## Usage
Launch main.py, you'll be prompted for your github credentials, enter them,
you will then be asked by a filter, a filter can be obtained by going to your
GitHub profile then in the repositories tab searching for whichever repos you
may want to delete, then copying the part of the url that is after the '?'.

Example https://github.com/Elkasitu?utf8=✓&tab=repositories&q=&type=&language=c

In this case, 'utf8=✓&tab=repositories&q=&type=&language=c' is the filter

The program will then show you a list of names of the repositories to be deleted
and will ask you for confirmation

## Disclaimer
USE AT YOUR OWN RISK
yadda yadda yadda No warranty at all
yadda yadda yadda I'm not responsible for whatever harm this may cause you

## License
GPLv3 License, read LICENSE for more information
