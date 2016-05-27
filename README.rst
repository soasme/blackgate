BLACKGATE
=========

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
