'''

    What the heck is keep_alive?!

  keep_alive is a module that keeps your bot alive (yeah, online). So, when you close this REPL, your bot will disconnect in 30 minutes. But if this file is missing, this template may not work as intended and it may not EVEN boot lol. 

  You'll need UptimeRobot for 24/7 uptime. Keep in mind that your bot can get ratelimited (What is that? "ratelimit" is that your bot was running too many actions and it got temporarily banned from accessing the Discord API. You may need to reboot the bot).
'''

settings = {
  'website': {
    # This is your website's document. Whenever anyone visits your website, the text that will appear is the `document` variable.
    'document': "I'm alive!"
  },

  'server': {
    # These are the server's settings. You can change the port and the host. We recommend you to leave them as-is, and not changing anything.
    'port': 8080,
    'host': '0.0.0.0'
  },

  'other': {
    # These are other settings. We do not recommend you editing these, or your website may stop working.
    'route': '/',
    'flask_type': ''
  }
}

from flask import Flask
from threading import Thread

app = Flask(str(settings['other']['flask_type']))

@app.route(str(settings['other']['route']))
def home():
  return (str(settings['website']['document']))

def run():
  app.run(host=str(settings['server']['host']),port=int(settings['server']['port']))

def keep_alive():
  t = Thread(target=run)
  t.start()