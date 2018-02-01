{% import "setup/amazon/map.jinja" as buildcfg %}

include:
    - pkg.libsodium.0_4_5.amzn
    - pkg.python-cherrypy.3_2_2.amzn
    - pkg.python-enum34.1_0.amzn
    - pkg.python-gnupg.0_3_8.amzn
    - pkg.python-impacket.0_9_14.amzn
    - pkg.python-ioflo.1_3_8.amzn
    - pkg.python-libcloud.2_0_0.amzn
    - pkg.python-libnacl.1_4_3.amzn
    - pkg.python-msgpack.0_4_6.amzn
    - pkg.python-psutil.5_2_2.amzn
    - pkg.python-pyzmq.14_5_0.amzn
    - pkg.python-raet.0_6_3.amzn
    - pkg.salt.2017_7_3.amzn
    - pkg.python-timelib.0_2_4.amzn
    - pkg.python-tornado.4_2_1.amzn
    - pkg.winexe.1_1.amzn
    - pkg.zeromq.4_0_5.amzn
