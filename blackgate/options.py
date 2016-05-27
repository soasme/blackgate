# -*- coding: utf-8 -*-

from tornado.options import define

define('executor_pools', default='', multiple=True,
       help='A list of executor_pools, separated by comma.')
