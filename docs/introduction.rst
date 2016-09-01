Introduction
==============


What is Blackgate?
-------------------

Blackgate is an API gateway application. It routes traffic to
upstream and then proxy response to downstream.

You can extend the ability of Blackgate by write plugin for it.
There are some builtin plugins in Blackgate. You can find them
in `blackgate.contrib`.

What is not Blackgate?
-----------------------

Blackgate is not a service discovery service. This is mainly
because there are some mature open-source implements already:
consul, etcd, zookeeper, etc.

Blackgate is not a load balancer, which means that you have
to choose your load balancer for your upstream services. Nginx
and HAProxy are two excellent server-side load blancing solutions.

Alternative Solutions
---------------------

Kong is similar to Blackgate. In most case they share the same
concepts. If your team are familiar with Nginx+Lua, this is
probably a better choice. The reason not using Kong is because if 
you want to start a Kong cluster, you have to run a bunch of
dependencies in several nodes, like Nginx, PostgreSQL, etc. 
Blackgate is much simpler in this case. Write config, and Run 
instance. Nothing more. In early stage, we can choose a simpler 
tool like Blackgate to avoid over-engineering.

You might also want to monitor and register services to
your service discovery service. Although it's complicated
, it still turns out to be a mature solution.
