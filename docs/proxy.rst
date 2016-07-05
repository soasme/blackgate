Proxy
======

Routing
--------

Blackgate will listen on a port and waiting incoming requests.
When receiving a request, Blackgate will route it to upstream service.
You should tell blackgate how to proxy a request in configurations.

Request Path
-------------

You should configure at least 3 configurations below:

* upstream_url
* request_path_regex
* request_path_sub

Plugins
--------

TODO
