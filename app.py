from flask import Flask
import redis
import os
import socket

app = Flask(__name__)

redis_host = os.environ.get("REDIS_HOST", "redis")
cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    return cache.incr("hits")

@app.route("/")
def hello():
    count = get_hit_count()
    hostname = socket.gethostname()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Multi-Container App</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
        }}

        .container {{
          background: rgba(255,255,255,0.1);
          padding: 50px;
          border-radius: 20px;
          text-align: center;
        }}

        .counter {{
          font-size: 64px;
          margin: 30px 0;
          background: rgba(255,255,255,0.2);
          padding: 25px;
          border-radius: 15px;
        }}

        .info {{
          background: rgba(255,255,255,0.15);
          padding: 20px;
          border-radius: 10px;
          margin-top: 20px;
          font-size: 14px;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Multi-Container App</h1>
        <p>This page has been visited:</p>
        <div class="counter">{count}</div>
        <button onclick="location.reload()">Refresh Counter</button>
        <div class="info">
          <p>Web container: {hostname}</p>
          <p>Database: Redis in another container</p>
        </div>
      </div>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)