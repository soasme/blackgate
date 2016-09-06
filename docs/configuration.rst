Configuration
==============

`port`
-------

Integer. Default 9654.

`sentry`
--------

Sentry configurations.

`dsn`
``````

String. Copy from Sentry Dashboard.

Example: 'http://fhoczvkzelftasdzbsxqnpevduvrgcqg:quufimqaxngdimrdumseikfgotqqstvm@sentry.your-inc.com/1'

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
