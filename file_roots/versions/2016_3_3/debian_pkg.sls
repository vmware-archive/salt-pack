{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_arch == 'armhf' %}

    - pkg.libsodium.1_0_3.debian8
    - pkg.openpgm.5_2_122.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-ioflo.1_3_8.debian8
    - pkg.python-libnacl.4_1.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-raet.0_6_3.debian8
    - pkg.python-timelib.0_2_4.debian8
    - pkg.python-tornado.4_2_1.debian8
    - pkg.salt.2016_3_3.debian8
    - pkg.zeromq.4_0_5.debian8

{% else %}
    - pkg.bsdmainutils.9_0_6.debian8
    - pkg.libsodium.1_0_3.debian8
    - pkg.openpgm.5_2_122.debian8
    - pkg.python-cherrypy.2_3_0.debian8
    - pkg.python-croniter.0_3_4.debian8
    - pkg.python-crypto.2_6_1.debian8
    - pkg.python-enum34.1_0_4.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-ioflo.1_3_8.debian8
    - pkg.python-jinja2.2_7_3.debian8
    - pkg.python-libcloud.0_20_0.debian8
    - pkg.python-libnacl.4_1.debian8
    - pkg.python-msgpack.0_4_2.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-raet.0_6_3.debian8
    - pkg.python-requests.2_7_0.debian8
    - pkg.python-systemd.231.debian8
    - pkg.python-timelib.0_2_4.debian8
    - pkg.python-tornado.4_2_1.debian8
    - pkg.python-urllib3.1_10_4.debian8
    - pkg.python-yaml.3_11.debian8
    - pkg.salt.2016_3_3.debian8
    - pkg.zeromq.4_0_5.debian8

{% endif %}
