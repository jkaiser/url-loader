#!/bin/python
"""
A simple e2e test. It
    1) creates 100 files
    2) servers them via a simple http server
    3) tries to load them via the loader
    4) checks for output file existence and its content

If the test fails then this script returns with the exit code 1
"""
import os.path
import tempfile
import threading
import http.server
from typing import Tuple, Iterable
from loader.loader import build_loader


class SilentRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    A normal SimpleHYYPRequestHandler prints messages for each http request. The SilentRequestHandler supresses
    those messages.
    """
    def log_message(self, format, *args):
        pass


def create_and_start_server(target_dir) -> Tuple[http.server.ThreadingHTTPServer, threading.Thread]:
    os.chdir(target_dir)    #SimpleHTTPRequestHandler serves the files from the current working directory
    handler = SilentRequestHandler
    server = http.server.ThreadingHTTPServer(("localhost", 8080), handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()
    return server, server_thread


def shutdown(server, server_thread) -> None:
    server.shutdown()
    server.server_close()
    server_thread.join()


def create_served_files(target_dir: str) -> Tuple[Iterable[str], Iterable[str]]:
    file_names = [str(i) for i in range(100)]
    for i in file_names:
        path = os.path.join(target_dir, str(i))
        with open(path, 'w') as f:
            f.write(i)
    full_paths = [os.path.join(target_dir, i) for i in file_names]

    return file_names, full_paths


def create_and_fill_source_url_file(file_names: Iterable[str]) -> tempfile.NamedTemporaryFile:
    url_file = tempfile.NamedTemporaryFile("w")
    urls = ["http://localhost:8080/{}".format(f) for f in file_names]
    for url in urls:
        url_file.write(url + "\n")
    url_file.flush()
    return url_file


def execute_test(url_file_name: str, file_names: Iterable[str], tear_down) -> None:
    target_dir = tempfile.TemporaryDirectory()
    loader = build_loader(url_file_name, target_dir.name)
    load_files(loader, tear_down)

    for n in file_names:
        full_name = os.path.join(target_dir.name, n)
        test_if_file_exists(full_name)
        test_if_content_is_correct(full_name, n, tear_down)
    print("downloaded files are correct")


def load_files(loader, tear_down_test):
    try:
        success = loader.start()
        if success:
            print("loader returned no error")
        else:
            print("test failed because loader returned False")
            tear_down_test()
            exit(1)
    except Exception as e:
        print(e)
        tear_down_test()
        exit(1)


def test_if_content_is_correct(full_name, expected_content, tear_down) -> None:
    with open(full_name) as f:
        data = f.read()
        if data != expected_content:
            print("file {} has invalid content".format(full_name))
            tear_down()
            exit(1)


def test_if_file_exists(name: str) -> None:
    try:
        os.stat(name)
    except Exception as e:
        print("failed to check for existence of file {}. err: {}".format(name, e))
        exit(1)


if __name__ == "__main__":
    source_dir = tempfile.TemporaryDirectory()
    file_names, full_file_names = create_served_files(source_dir.name)
    server, server_thread = create_and_start_server(source_dir.name)

    def tear_down_server():
        shutdown(server, server_thread)

    url_file = create_and_fill_source_url_file(file_names)
    execute_test(url_file.name, file_names, tear_down_server)
    print("test successful")
    tear_down_server()
