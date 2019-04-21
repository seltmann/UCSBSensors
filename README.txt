README

Quickstart if you already have python in your system

To start: you must "pip install arable" to install the arable python client

Put "physics.py" in a suitable place in your path to access these helpful functions

The notebook .ipynb can be opened in the Jupyter environment.  

Arable uses homebrew Python version 2.7


=====================
How I setup my system on OSX
Use your Terminal: drag /Applications/Utilities/Terminal over to your sidebar
Install Sublime text: http://www.sublimetext.com/

Make some changes to your environment:
In the terminal type "open .bashrc" and add the following text, then save and close.

alias ipy="jupyter notebook"

# set SublimeText as default editor
export EDITOR='subl -w'

In the terminal type ". .bashrc"

In the terminal type "subl .bash_profile" and add the following text, then save and close.

#source .bashrc
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

In the terminal type ". .bash_profile"

Install Homebrew: https://brew.sh/

Install python:

>brew install python@2

Install Jupiter:

>brew install jupyter

Find a suitable folder and copy the ipynb over to it.
>mkdir lib 
Add physics.py to /lib
>ipynb  

A new window should open in your browser!  Update your username, password, and tenant and start playing with data!

----------------------------------
Simple script for arable sensors

https://docs.google.com/document/d/12ucWe86dmpKJg_aTPuzMD5WTpVVHQOEvRc1OAAIf9wE/edit?usp=sharing
