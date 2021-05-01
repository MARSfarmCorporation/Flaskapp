# Flaskapp

A web application for MARSfarm developed and tested on an Apache2 server, hosted by Amazon EC2 Ubuntu machine.
# Project Structure

Python/Flask application
CouchDB for database
AWS S3 for storage
Entry point: flaskapp.py -> def entry_point()

# Development (MAC OS)
To get started:
IDE: Download VS Code <https://code.visualstudio.com/download>
Version control: Install git and clone from github
Install python (version 3 or higher)
Install a virtual environment management tool IF you have multiple python projects (optional, helps with dependency versioning)
Pip: Standard for python package management - this will already be installed along with pyton or your virtual environment tool
Install dependencies: These are listed in requirements.txt.  Execute `pip install -r requirements.txt` from project root

For testing/deploying to dev & production
SSH: In extensions search for `Remote - SSH` and install.  Once installed a little green button with arrows >< will appear in the
bottom left.  Click it and a panel should appear on top.  Select "open SSH configuration file".  See photo from google docs
for what to enter here: <https://docs.google.com/document/d/1qgiUuNySMmREqbltf8TPbcL64KPHsCeJOnmZ0S5-fhA/edit>.  For more details
navigate here <https://medium.com/@christyjacob4/using-vscode-remotely-on-an-ec2-instance-7822c4032cff>. //jdl am here.....
You need to enter credentials into a file named IdentityFile and then replace the path for the location of your file in your config.
Now click the green button again and select `Connect to Host`.

To deploy, Open window in “Flask-development”.  Edit and save the files you want to change.
Then enter command: ‘sudo service apache2 restart’. Verify changes are correct at `dev.marsfarm.io`.

When you deploy, also push changes via git, always make sure you have deployed those changes to Flask-development & the production environment (aws-ec2). and verify they match the git repo.

# Development (Windows) - todo
