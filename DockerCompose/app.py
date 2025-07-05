import time

import redis # Used for caching - increases performence. 
from flask import Flask

app = Flask(__name__)

# Connect to Local Redis Server - via Docker
r = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    
    while True:
        try:
            return r.incr('hits') # Increment Counter(hits). If the key doesn't exist, Redis creates it and sets it to 1.
        except Exception as e:
            time.sleep(1)
            retries = retries - 1
            if retries == 0:
                raise e
            
@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello! This page has been viewed {count} times.'
                
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


