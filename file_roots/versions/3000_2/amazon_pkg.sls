{% import "setup/amazon/map.jinja" as buildcfg %}

include:
    - pkg.libsodium.0_4_5.amzn
    - pkg.python-backports_abc.0_5.amzn
    - pkg.python-cherrypy.3_2_2.amzn
    - pkg.python-enum34.1_0.amzn
    - pkg.python-gnupg.0_3_8.amzn
    - pkg.python-ipaddress.1_0_18.amzn
    - pkg.python-libcloud.2_0_0.amzn
    - pkg.python-msgpack.0_6_2.amzn
    - pkg.python-psutil.5_2_2.amzn
    - pkg.python-pyzmq.14_5_0.amzn
    - pkg.python-singledispatch.3_4_0_3.amzn
    - pkg.salt.3000_2.amzn
    - pkg.winexe.1_1.amzn
    - pkg.zeromq.4_0_5.amzn
