#  Copyright (c) 2025 AshokShau
#  Licensed under the GNU AGPL v3.0: https://www.gnu.org/licenses/agpl-3.0.html
#  Part of the TgMusicBot project. All rights reserved where applicable.

from TgMusic import client
from TgMusic.core._config import config
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


# ========== Health Check Server ==========
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")


def run_health_server():
    server = HTTPServer(('0.0.0.0', config.RENDER_PORT), HealthHandler)
    client.logger.info(f"🌐 Health server started on port {config.RENDER_PORT}")
    server.serve_forever()


def main() -> None:
    # Start health check server in a separate thread
    threading.Thread(target=run_health_server, daemon=True).start()

    # Start bot
    client.logger.info("Starting TgMusicBot...")
    client.run()


if __name__ == "__main__":
    main()

