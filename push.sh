#!/usr/bin/sh

python bookmarks.py ~/.config/chromium/Default/Bookmarks bookmarks_ubuntu_hiptf.html
git add .
git add -u
git commit -am "update"
git push origin master
