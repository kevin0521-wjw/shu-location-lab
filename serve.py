#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LOCATION LAB 本地静态服务器（只用标准库，零依赖）。

用法：
    python serve.py            # 默认 127.0.0.1:8080
    python serve.py 9000       # 指定端口
    python serve.py 9000 0.0.0.0   # 指定监听地址（手机同局域网可访问）

比 `python -m http.server` 多做的两件事：
  1. 补上 .json / .webmanifest 的 MIME，避免个别浏览器当纯文本处理；
  2. 全部响应加 no-store，改完 index.html 刷新即生效，不会被缓存骗。
"""
from __future__ import annotations

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    # 补 MIME：Windows 注册表里 .json 有时被映射成 text/plain
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".json": "application/json; charset=utf-8",
        ".webmanifest": "application/manifest+json",
        ".svg": "image/svg+xml",
    }

    def end_headers(self):
        # 开发期禁缓存：改一版刷一下就能看到
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):  # 只打印路径，日志别太吵
        sys.stderr.write("  %s\n" % (fmt % args))


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"

    # 保证在仓库根目录起服务，双击脚本也行
    os.chdir(ROOT)

    httpd = ThreadingHTTPServer((host, port), partial(Handler, directory=ROOT))
    shown = "127.0.0.1" if host in ("0.0.0.0", "::") else host
    print("LOCATION LAB  →  http://%s:%d/" % (shown, port))
    print("根目录：%s" % ROOT)
    print("Ctrl+C 停止")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
