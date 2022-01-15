run app: `flask run`

Current status - English translation >95%, Russian >80%

Check downloaded config - is it text/html or what?

Changing lang:
    Accept-Language: en-US,en;q=0.5
    From CLI
    From /ru/ /en/ etc url suffix

Flask with docker:
https://docs.docker.com/language/python/build-images/

waitress doesn't allow to use hop-by-hop headers, so it is working only with flask server, which is more than enough
