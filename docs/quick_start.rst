Quick Start
===========

Run Application
-----------------

    $ blackgate start

* Using Ctrl-C to Stop.
* Send SIGTERM or SIGKILL to process.

    $ blackgate start -c /path/to/config

    $ blackgate start -a your_tornado_application


Configure Upstream
-------------------


    upstreams:
      - name: shop
        url: 'http://shop.intra.example.org/'



Enable Plugin
---------------
