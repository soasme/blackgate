BLACKGATE
=========

Usage
-----

Route User Request to Inner Service::

    from gateway.core import pools, Command

    class APIService(Command):

        group_key = 'api.v1'
        host = 'x:5000'

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

Add HTTPProxy Handler to tornado.web.Application::


    pools.register_pool('api.v1')
    urls = [
        (r'/api/v1/(.*)', HTTPProxy, dict(service=APIService)),
    ]
    app = tornado.web.Application(urls)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
