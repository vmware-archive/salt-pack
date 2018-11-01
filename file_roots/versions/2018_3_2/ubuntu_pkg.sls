{% import "setup/ubuntu/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'ubuntu1804' %}

    - pkg.python-ioflo.1_5_0.ubuntu1804
    - pkg.python-raet.0_6_5.ubuntu1804
    - pkg.python-timelib.0_2_4.ubuntu1804
    - pkg.salt.2018_3_2.ubuntu1804

{% elif buildcfg.build_release == 'ubuntu1604' %}

    - pkg.libsodium.1_0_8.ubuntu1604
    - pkg.python-ioflo.1_5_0.ubuntu1604
    - pkg.python-libcloud.1_5_0.ubuntu1604
    - pkg.python-libnacl.4_1.ubuntu1604
    - pkg.python-raet.0_6_5.ubuntu1604
    - pkg.python-timelib.0_2_4.ubuntu1604
    - pkg.python-tornado.4_2_1.ubuntu1604
    - pkg.salt.2018_3_2.ubuntu1604

{% elif buildcfg.build_release == 'ubuntu1404' %}

    - pkg.libsodium.1_0_3.ubuntu1404
    - pkg.python-backports-ssl_match_hostname.3_4_0_2.ubuntu1404
    - pkg.python-enum34.1_0_4.ubuntu1404
    - pkg.python-future.0_14_3.ubuntu1404  # do we really need this old version?
    - pkg.python-futures.3_0_3.ubuntu1404
    - pkg.python-ioflo.1_3_8.ubuntu1404
    - pkg.python-libcloud.1_5_0.ubuntu1404
    - pkg.python-libnacl.4_1.ubuntu1404
    - pkg.python-msgpack.0_4_6.ubuntu1404
    - pkg.python-raet.0_6_3.ubuntu1404
    - pkg.python-timelib.0_2_4.ubuntu1404
    - pkg.python-tornado.4_2_1.ubuntu1404
    - pkg.salt.2018_3_2.ubuntu1404
    - pkg.zeromq.4_0_5.ubuntu1404

{% endif %}
