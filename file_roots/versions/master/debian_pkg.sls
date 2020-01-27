{% import "setup/debian/map.jinja" as buildcfg %}

include:
{% if buildcfg.build_release == 'debian9' %}

    - pkg.python-jinja2.2_9_4.debian9
    - pkg.salt.master.debian9

{% elif buildcfg.build_release == 'debian8' %}

{% if buildcfg.build_arch == 'armhf' %}

    - pkg.libsodium.1_0_3.debian8
    - pkg.python-future.0_14_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-libcloud.1_5_0.debian8
    - pkg.python-pyzmq.14_4_0.debian8
    - pkg.python-systemd.231.debian8
    - pkg.python-tornado.4_2_1.debian8
    - pkg.salt.master.debian8

{% else %}
    - pkg.libsodium.1_0_3.debian8
    - pkg.python-futures.3_0_3.debian8
    - pkg.python-jinja2.2_9_4.debian8       ## jessie 2.7.3-1, jessie-backports 2.8-1~bpo8+1
    - pkg.python-libcloud.1_5_0.debian8     ## jessie 0.15.1-1
    - pkg.python-systemd.231.debian8        ## jessie backports 233-1~bpo8+1
    - pkg.python-tornado.4_2_1.debian8      ## jessie 3.2.2-1.1, jessie-backports 4.4.3-1~bpo8+1
    - pkg.python-urllib3.1_10_4.debian8     ## jessie 1.9.1-3, jessie-backports 1.16-1~bpo8+1
    - pkg.salt.master.debian8

{% endif %}

{% endif %}
