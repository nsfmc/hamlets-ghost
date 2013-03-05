#Hamlet's Ghost

Hamlet's ghost provides the young dane with some useful information, but young hamlet must verify this before he can go around making wild accusations.

more seriously, this takes in some text from stdin and parses whatever spotify urls it finds and then tries to corroborate spotify's sketchy metadata with discogs' data. the information this yields is mostly correct, but it's still likely to not be totally correct, so again: stage a play to be *really sure.*

## setup

to get this going, set up a virtual env and install the reqs

    virtualenv env
    . ./env/bin/activate
    pip install requests discogs_client

then, on a mac

    pbpaste | python ghost.py | pbcopy
