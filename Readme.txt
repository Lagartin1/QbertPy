Pygame Installation¶
Pygame requires Python; if you don't already have it, you can download it from python.org. It's recommended to run the latest python version, because it's usually faster and has better features than the older ones. Bear in mind that pygame has dropped support for python 2.

Pygame still does not run on Python 3.11 as per the github page. The best way to install pygame is with the pip tool (which is what python uses to install packages). Note, this comes with python in recent versions. We use the --user flag to tell it to install into the home directory, rather than globally.

python3 -m pip install -U pygame --user
To see if it works, run one of the included examples:

python3 -m pygame.examples.aliens
If it works, you are ready to go! If not there are more detailed, platform-specific instructions further down the page.