Configuration
==============

`port`
-------

Integer. Default 9654.

`proxies`
----------

List. Default `[]`.

Each item should be an `Proxy` object.

Blackgate will build a final upstream url by there options:

- `upstream_url`
- `request_path_regex`
- `request_path_sub`

Rule: `upstream_url + re.sub(request_path_regex, request_path_sub, path)`.
`path` is coming from user request.

`name`
````````

The name to identify proxy.

Required.

`upstream_url`
```````````````

`upstream_url` is used as base url to build upstream request url.

Required.

`request_path_regex`
`````````````````````

`request_path_regex` is a regex string.

Required.

`request_path_sub`
```````````````````

`request_path_sub` is a regex sub string.

Required.

`pool_max_size`
```````````````````

`pool_max_size` is an integer to limit the amount of user concurrent request.
Default 300.

It is recommend to give a proper `pool_max_size` to protect upstream service.

Formula::

    pool_max_size = request_per_second / response_time_per_request (at peak time)

Optional.
