{% set amzn_salt_mock_cfg = '/etc/mock/amzn-salt-x86_64.cfg' %}
{% set src_amzn_salt_mock_cfg = 'salt://setup/amazon/amzn/amzn-salt-x86_64.cfg' %}

include:
  - setup.amazon


build_salt_mock_prefs_rm:
  file.absent:
    - name: {{amzn_salt_mock_cfg}}


build_salt_mock_prefs_file:
  file.managed:
    - name: {{amzn_salt_mock_cfg}}
    - source: {{src_amzn_salt_mock_cfg}}
    - dir_mode: 755
    - mode: 644
    - makedirs: True
    - group: mock
    - skip_verify: True

