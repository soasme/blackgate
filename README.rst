Blackgate
=========

Blackgate is an API gateway application.  It's stateless and extendable.

Example
--------

Configure Upstream
```````````````````

A minimal Blackgate config looks something like this::

    ---
    proxies:
      - name: github
        upstream_url: 'https://api.github.com'
        request_path_regex: /github/(.*)
        request_path_sub: /\1

Just save it as `blackgate.yml`.

Run Application
```````````````````


Run application::

    $ blackgate -c ./blackgate.yml start


Test Blackgate
```````````````````

Using `curl` to test functionality::

    $ curl http://0.0.0.0:9654/github/repos/soasme/blackgate
    {"id":59739087,"name":"blackgate","full_name":"soasme/blackgate", ...
