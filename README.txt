Katja - the folks at Arable marks sent me a bunch of stuff on drop box in response to my request so we can see the data from the sensors.. which maybe I can share with you because this READ ME file that I've copied here is like a foreign language to me...  Does it speak to you?  Ryan hasn't really dealt with this language and stuff.  I'm hoping once a system is set up that we can all access more easily?

I'll share folder with you.

Thank you.

Lisa



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




Do you have conda installed on your Mac? If so, you can try these instructions before/while we meet: https://docs.google.com/document/d/1LYfJvI_4nHXE9SvB-T_Et7mmQsSCQQrrHqEoR6lcVwE/edit?usp=sharing. 


ccber-research@ucsb.edu then the password is greenresearch33  and UCSB is the tenant/company name 

UCSB and CCBER accounts


----------------------------------
Simple script for arable sensors

https://docs.google.com/document/d/12ucWe86dmpKJg_aTPuzMD5WTpVVHQOEvRc1OAAIf9wE/edit?usp=sharing