# -*- coding: utf-8 -*-
"""
This tool will uninstall StaSh from pythonista and then download&run getstash.py
"""
import os
import shutil
import tempfile

import requests
import six


def get_stash_dir():
    return os.path.join(os.path.expanduser("~"), "Documents", "site-packages", "stash")


def remove_stash():
    shutil.rmtree(get_stash_dir())


def install_stash(repo="warexify", branch="dev"):
    if not "TMPDIR" in os.environ:
        os.environ["TMPDIR"] = tempfile.gettempdir()
    ns = {"_owner": repo, "_br": branch}
    exec(requests.get("https://bit.ly/get-stash").content, ns, ns)


def parse_gh_target(s):
    if s == "":
        return "warexify", "dev"
    s = s.replace("/", ":")
    if ":" not in s:
        s = "warexify:" + s
    repo, branch = s.split(":")
    return repo, branch


def main():
    ts = six.moves.input("New target (repo:branch, empty for default): ")
    t = parse_gh_target(ts)
    if os.path.exists(get_stash_dir()):
        remove_stash()
    install_stash(*t)


if __name__ == "__main__":
    main()
