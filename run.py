import os
from app import create_app
import sys

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')
#session['logged_in']= False

if __name__ == '__main__':
	#session['logged_in']= False
	if sys.version_info.major < 3:
	    reload(sys)
	sys.setdefaultencoding('utf8')
	app.run()