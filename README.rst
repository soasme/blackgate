Blackgate
=========

Blackgate is an API gateway application.  It's stateless and extendable.

Install via pip
---------------

Run::

    $ pip install blackgate==0.2.3

Or::

    $ git clone git@github.com:soasme/blackgate.git
    $ cd blackgate
    $ python setup.py install

Install via docker
-------------------

Run::

    $ docker pull blackgate:v0.2.3


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


Or via docker::

    $ docker run -it --rm --name blackgate \
        -p 9654:9654 \
        -v blackgate.yml:/etc/blackgate.yml blackgate:v0.2.3

Test Blackgate
```````````````````

Using `curl` to test functionality::

    $ curl http://127.0.0.1:9654/github/repos/soasme/blackgate
    {"id":59739087,"name":"blackgate","full_name":"soasme/blackgate", ...
