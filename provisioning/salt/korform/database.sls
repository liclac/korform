db_user:
  postgres_user.present:
    - name: "{{ pillar['korform']['db_username'] }}"
    - password: "{{ pillar['korform']['db_password'] }}"
    - login: true
    - require:
      - sls: postgres

db:
  postgres_database.present:
    - name: korform
    - owner: "{{ pillar['korform']['db_username'] }}"
    - require:
      - sls: postgres
