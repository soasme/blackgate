BLACKGATE
=========

Usage: Define Command
----------------------

`Command` represents an external operation.
To define a command, you must inherit from `blackgate.Command`.

Example::


    from blackgate import Command

    class GetCurrentUser(Command):

        group_key = 'service.session'
        command_key = 'get_current_user'

        def __init__(self, cookie):
            self.cookie = cookie

        def run(self):
            resp = requests.get('http://session-service/session', headers={'Cookie': self.cookie}, timeout=1)
            return resp.json()['user_id']

        def fallback(self):
            return None

Usage: Synchronous Execution
-----------------------------

You can contruct command with parameters and then execute it::

    get_current_user = GetCurrentUser(cookie='session=78b29404-92c9-49db-b87b-531b5f9cfc56')
    user_id = get_current_user.execute()

Usage: Asynchronous Execution
------------------------------

You can execute a Command asynchronously by using the queue() method, as in the following example::

    @tornado.gen.coroutine
    def some_function():
        get_current_user = GetCurrentUser(cookie='session=78b29404-92c9-49db-b87b-531b5f9cfc56')
        user_id = yield get_current_user.queue()
        print(user_id)

Usage: Fallback
----------------

Usage: Proxy
-------------

Configure Blackgate Component::

    from blackgate import component
    component.add('executor_pool', {'group_key': 'api.v1', 'max_workers': 10})
    component.install()
    app = tornado.web.Application([
      (r'/api/v1/(.*)', HTTPProxy, dict(command=APIV1Command)),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

Route User Request to Inner Service::

    from blackgate import HTTPProxyCommand

    class APIService(HTTPProxyCommand):

        group_key = 'api.v1'

        command_key = 'proxy_v1_traffic'

        def before_request(self):
            path = self.request['path'].replace('/api', '')
            self.request['url'] = 'http://intra.service.com' + path

        def fallback(self):
            return dict(
                status_code=500,
                reason='Internal Server Error',
                headers={},
                content=json.dumps({
                    'code': 500,
                    'message': 'internal server error',
                    'error': {}
                })
            )


ThreadExecutorPool
--------------------

Executor Pool is the place where you can run external network calls.

Each command defines its group_key.
You must register an executor_pool for specific group_key::

    from blackgate import component
    component.add('executor_pool', {'group_key': 'service.session', 'max_workers', 10})
    # ...
    component.install()
