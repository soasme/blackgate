CLI
====

Command: blackgate
------------------

    $ blackgate [blackgate_options] <command> [command_options]

blackgate_options
-------------------

1. `-c /path/to/blackgate.yml`

Blackgate configuration file.

Blackgate by default search configuration file from files listed below by order.

* `./blackgate.yml`
* `~/.blackgate.yml`
* `/usr/local/etc/blackgate/blackgate.yml`
* `/etc/blackgate/blackgate.yml`

Blackgate will fail to start without loading a yaml config file.

This file contains configuration for upstream services, plugins, etc.

command: start
---------------

Starts a Blackgate instance::

    $ blackgate start


command: stop
--------------

Terminates a Blackgate instance::

    $ blackgate stop

Note: Blackgate will shutdown instance gracefully.


command: restart
----------------

Restart a Blackgate instance::

    $ blackgate restart

Note: If Blackgate was not running before executing this command, it will start
a Blackgate instance directly.


command: reload
----------------

Reload Blackgate configuration::

    $ blackgate reload


command: status
---------------

Output the status of Blackgate::

    $ blackgate status
