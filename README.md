# gemini-demo-1

Minimal but usable interactive Gemini client in < 100 LOC of Python 3

## Rationale

One of the original design criteria for the Gemini protocol was that
"a basic but usable (not ultra-spartan) client should fit comfortably
within 50 or so lines of code in a modern high-level language.
Certainly not more than 100".  This client was written to gauge how
close to (or far from!) that goal the initial rough specification is.

## Capabilities

This crude but functional client:

* Has a minimal interactive interface for "Gemini maps"
* Will print plain text in any encoding if it is properly declared in
  the server's response header
* Will handle binary files using programs specified in `/etc/mailcap`
  (so you can, e.g. view images)
* Will follow redirects
* Will report errors
* Does NOT DO ANY validation of TLS certificates

It's a *snug* fit in 100 lines, but it's possible.  A 50 LOC client
would need to be much simpler.

## Usage

Run the script and you'll get a prompt.  Type a Gemini URL (the scheme
is implied, so simply entering e.g. `gemini.conman.org` will work) to
visit a Gemini location.

If a Gemini menu is visited, you'll see numeric indices for links, ala
VF-1 or AV-98.  Type a number to visit that link.

There is very crude history: you can type `b` to go "back".

Type `q` to quit.
