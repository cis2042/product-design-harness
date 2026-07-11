#!/usr/bin/env python3
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class UTF8HTTPRequestHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        content_type = super().guess_type(path)
        if content_type.startswith("text/") and "charset=" not in content_type:
            return f"{content_type}; charset=utf-8"
        return content_type


def main():
    parser = argparse.ArgumentParser(description="Serve the UX3 site with UTF-8 text headers.")
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.bind, args.port), UTF8HTTPRequestHandler)
    print(f"Serving on http://{args.bind}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
