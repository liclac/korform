korform
=======

Korform is a piece of software for managing member rosters in organizations such as choirs, sports teams, etc. Because mailing around Excel spreadsheets becomes very messy, very quickly.

It started out as an internal tool for the Gothenburg Cathedral's choir, and the name just means "choir form", because it was originally just a form for specifying if you can show up to different planned events or not.

This is version 3, and is still under active development.

Development Setup
-----------------

You need [Vagrant](https://vagrantup.com/) and [VirtualBox](https://virtualbox.org/) (VMware [Fusion](https://www.vmware.com/products/fusion) for Mac/[Workstation](https://www.vmware.com/products/workstation) for Windows and Linux also supported).

1. Clone the sources, and open a terminal in the cloned directory.
1. Run `vagrant up`, grab a coffee while Vagrant sets everything up.
1. Run `vagrant ssh` to get a shell inside the virtual machine.
1. Run `cd /vagrant`, this places you in the shared folder for the sources.
1. Run `virtualenv .` to create an isolated environment for Python packages.
1. Run `. bin/activate` to activate it.  
   You must do this again before running any `./manage.py` commands, if you close and reopen your shell.
1. Run `pip install -r requirements.txt` to install needed packages.
1. Run `./manage.py bower install` to install Bower packages.
1. Run `./manage.py migrate` to run database migrations.
1. Run `./manage.py runserver_plus 0.0.0.0:8000` to run the development server.
1. Open "localhost:8080" in a browser of your choice!
