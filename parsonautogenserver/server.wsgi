#server.wsgi
import sys
import logging

activate_sh = "/home/ubuntu/parsons-autogen/parsonautogenserver/venv/bin/activate_this.py"
with open(activate_sh) as instream:
	exec(instream.read(), dict(__file__=activate_sh))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/parsonautogenserver/')

from server import app as application
