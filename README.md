# Flaskapp

A web application for MARSfarm developed and tested on an Apache2 server, hosted by Amazon EC2 Ubuntu machine.
# Project Structure

Python/Flask application
CouchDB for database
AWS S3 for storage
Entry point: flaskapp.py -> def entry_point()

# Development
To get started:
IDE: Download VS Code <https://code.visualstudio.com/download>
Version control: Install git and clone from github
Install python (version 3 or higher)
Install a virtual environment management tool IF you have multiple python projects (optional, helps with dependency versioning)
Pip package management tool: Standard for python package management - this will already be installed along with python or your virtual environment tool.
Install dependencies: These are listed in requirements.txt.  Execute `pip install -r requirements.txt` from project root if using pip

For testing/deploying to dev & production
Install putty (certificate management tool)
Get credentials in the form of ppk file from Peter, and you will use putty to convert to an Amazon pem file.
For access to aws EC2, use putty from command line to run: puttygen key.ppk -O private-openssh -o key.pem
A pem file should be generated in the path you specified with this command with name key.pem (you can name it anything you like)
You need to replace the path in IdentityFile with the path to your local pem file in the config which you'll create locally. Use the config_template included in this project to create your config.

Now SSH in:
SSH: In extensions search for `Remote - SSH` and install.  Once installed a little green button with arrows >< will appear in the
bottom left.  Click it and a panel should appear on top.  Select "open SSH configuration file" and select your config file.

Now click the green button again and select `Connect to Host`. Choose your host (develop or production)

To deploy, Open window in “Flask-development”.  Edit and save the files you want to change.
Then enter command: ‘sudo service apache2 restart’. Verify changes are correct at `dev.marsfarm.io`.

When you deploy, also push changes via git, always make sure you have deployed those changes to Flask-development & the production environment (aws-ec2). and verify they match the git repo.
