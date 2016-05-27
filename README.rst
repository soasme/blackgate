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

    from gateway.core import Command

    class APIService(Command):

        group_key = 'api.v1'
        command_key = '*'
        host = 'localhost:5000'

        def __init__(self, request):
            self.request = request

        def build_url(self, path):
            path = path[4:]
            return 'http://' + self.host + path

        def run(self):
            conn = self.connection_pool.get_connection(self.host)
            req = dict(
                method=self.request['method'],
                url=self.build_url(self.request['path']),
                data=self.request['data'],
                params=self.request['params'],
                headers=self.request['headers'],
            )
            resp = conn.request(**req)
            return dict(
                status_code=resp.status_code,
                reason=resp.reason,
                headers=dict(resp.headers),
                content=resp.content
            )
