{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1604' %}

    - pkg.libsodium.1_0_8.ubuntu1604
    - pkg.python-ioflo.1_5_0.ubuntu1604
    - pkg.python-libnacl.4_1.ubuntu1604
    - pkg.python-raet.0_6_5.ubuntu1604
    - pkg.python-timelib.0_2_4.ubuntu1604
    - pkg.python-tornado.4_2_1.ubuntu1604
    - pkg.salt.2016_3_1.ubuntu1604

{% elif buildcfg.build_release == 'ubuntu1404' %}

    - pkg.libsodium.1_0_3.ubuntu1404
    - pkg.python-enum34.1_0_4.ubuntu1404
    - pkg.python-future.0_14_3.ubuntu1404  # do we really need this old version?
    - pkg.python-futures.3_0_3.ubuntu1404
    - pkg.python-ioflo.1_3_8.ubuntu1404
    - pkg.python-libcloud.0_15_1.ubuntu1404    ## - universe then main 12.04.5 - do we need 0.18.0
    - pkg.python-libnacl.4_1.ubuntu1404
    - pkg.python-raet.0_6_3.ubuntu1404
    - pkg.python-timelib.0_2_4.ubuntu1404
    - pkg.python-tornado.4_2_1.ubuntu1404
    - pkg.salt.2016_3_1.ubuntu1404
    - pkg.zeromq.4_0_5.ubuntu1404

{% elif buildcfg.build_release == 'ubuntu1204' %}

    - pkg.libsodium.1_0_3.ubuntu1204
    - pkg.python-backports-ssl_match_hostname.3_4_0_2.ubuntu1204
    - pkg.python-croniter.0_3_4.ubuntu1204
    - pkg.python-crypto.2_6_1.ubuntu1204
    - pkg.python-enum34.1_0_4.ubuntu1204
    - pkg.python-future.0_14_3.ubuntu1204  # do we really need this old version?
    - pkg.python-futures.3_0_3.ubuntu1204
    - pkg.python-ioflo.1_3_8.ubuntu1204
    - pkg.python-libcloud.0_14_1.ubuntu1204
    - pkg.python-libnacl.4_1.ubuntu1204
    - pkg.python-msgpack.0_3_0.ubuntu1204   ## - not found on ubuntu1204
    - pkg.python-mako.0_7_0.ubuntu1204      ## - not found on ubuntu1204
    - pkg.python-pyzmq.14_0_1.ubuntu1204
    - pkg.python-raet.0_6_3.ubuntu1204
    - pkg.python-requests.2_0_0.ubuntu1204
    - pkg.python-timelib.0_2_4.ubuntu1204
    - pkg.python-tornado.4_2_1.ubuntu1204
    - pkg.python-urllib3.1_7_1.ubuntu1204
    - pkg.salt.2016_3_1.ubuntu1204
    - pkg.zeromq.4_0_5.ubuntu1204

{% endif %}
