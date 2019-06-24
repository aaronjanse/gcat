#!/usr/bin/env python3

import cgi
import socket
import ssl
import urllib.parse

menu = []
hist = []

def absolutise_url(base, relative):
    # Absolutise relative links
    if "://" not in relative:
        # Python's URL tools somehow only work with known schemes?
        base = base.replace("gemini://","http://")
        relative = urllib.parse.urljoin(base, relative)
        relative = relative.replace("http://", "gemini://")
    return relative

while True:
    # Get input
    cmd = input("> ").strip()
    # Handle things other than requests
    if cmd.lower() == "q":
        print("Bye!")
        break
    # Get URL, from menu, history or direct entry
    if cmd.isnumeric():
        url = menu[int(cmd)-1]
    elif cmd.lower() == "b":
        # Yes, twice
        url = hist.pop()
        url = hist.pop()
    else:
        url = cmd
        if not "://" in url:
            url = "gemini://" + url
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme != "gemini":
        print("Sorry, Gemini links only.")
        continue
    # Do the Gemini transaction, following redirects
    while True:
        try:
            s = socket.create_connection((parsed_url.netloc, 1965))
            context = ssl.SSLContext()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname = parsed_url.netloc)
            s.sendall((parsed_url.path + '\r\n').encode("UTF-8"))
        except:
            print("Network error!")
            continue
        # Get header and check for redirects
        fp = s.makefile("rb")
        header = fp.readline()
        header = header.decode("UTF-8").strip()
        status, mime = header.split("\t")
        # If this isn't a redirect, we're done
        if not status.startswith("3"):
            break
        # Follow the redirect
        url = absolutise_url(url, mime)
        parsed_url = urllib.parse.urlparse(url)
    # Fail if transaction was not successful
    if not status.startswith("2"):
        print("Error %s: %s" % (status, mime))
        continue
    # Text only!
    if not mime.startswith("text/"):
        print("Sorry, plain text only.")
        continue
    else:
        mime, mime_opts = cgi.parse_header(mime)
        body = fp.read()
        body = body.decode(mime_opts.get("charset","UTF-8"))
    # Handle a Gemini map
    if mime == "text/gemini":
        menu = []
        for line in body.splitlines():
            if line.startswith("\t") and line.count("\t") == 2:
                _, text, link_url = line.split("\t")
                link_url = absolutise_url(url, link_url)
                menu.append(link_url)
                print("[%d] %s" % (len(menu), text))
            else:
                print(line)
    # Handle any other plain text
    else:
        print(body)
    hist.append(url)
