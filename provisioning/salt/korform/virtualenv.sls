virtualenv:
  pip.installed:
    - require:
      - sls: python

korform-virtualenv:
  virtualenv.managed:
    - name: {{ pillar['korform']['root'] }}
    - requirements: {{ pillar['korform']['root'] }}/requirements.txt
    - user: {{ pillar['korform']['owner'] }}
    - require:
      - pip: virtualenv
