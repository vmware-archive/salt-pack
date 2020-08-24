{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'debian9' %}

    - pkg.python-jinja2.2_9_4.debian9
    - pkg.python-msgpack.0_6_2.debian9
    - pkg.salt.3000_4.debian9

{% elif buildcfg.build_release == 'debian8' %}

{% if buildcfg.build_arch == 'armhf' %}

    - pkg.libsodium.1_0_3.debian8
    - pkg.python-backports-abc.0_5.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-libcloud.1_5_0.debian8
    - pkg.python-msgpack.0_5_6.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-setuptools.33_1_1.debian8
    - pkg.python-systemd.231.debian8
    - pkg.salt.3000_4.debian8

{% else %}
    - pkg.libsodium.1_0_3.debian8
    - pkg.python-backports-abc.0_5.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-jinja2.2_9_4.debian8       ## jessie 2.7.3-1, jessie-backports 2.8-1~bpo8+1
    - pkg.python-libcloud.1_5_0.debian8     ## jessie 0.15.1-1
    - pkg.python-msgpack.0_5_6.debian8
    - pkg.python-setuptools.10_2_1.debian8
    - pkg.python-systemd.231.debian8        ## jessie backports 233-1~bpo8+1
    - pkg.python-urllib3.1_10_4.debian8     ## jessie 1.9.1-3, jessie-backports 1.16-1~bpo8+1
    - pkg.salt.3000_4.debian8

{% endif %}

{% endif %}
