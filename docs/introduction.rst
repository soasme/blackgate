Introduction
==============


What is Blackgate?
-------------------

Blackgate is an API gateway application. It routes traffic to
upstream services.

You can extend the ability of Blackgate by write plugin for it.
There are some builtin plugins in Blackgate. You can find them
in `blackgate.contrib`.

What is not Blackgate?
-----------------------

Blackgate is not a service discovery service. This is mainly
because there are some mature open-source implement already:
consul, etcd, zookeeper, etc.

Blackgate is not a load balancer, which means that you have
to choose your load balancer for your upstream services. Nginx
and HAProxy are two excellent server-side load blancing solutions.

Alternative Solution
---------------------

Kong is similar to Blackgate. In most case they share the same
concepts. If your team are familiar with Nginx+Lua, this is
probably a better choice.

You might also want to monitor and register services to
your service discovery service. Although it's a complicated
solution, it still turns out to be a mature one.