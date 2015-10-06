vagrant_db_user:
  postgres_user.present:
    - name: vagrant
    - login: true
    - superuser: true

db_user_is_superuser:
  postgres_user.present:
    - name: "{{ pillar['korform']['db_username'] }}"
    - password: "{{ pillar['korform']['db_password'] }}"
    - login: true
    - superuser: true
    - require:
      - sls: postgres
      - sls: korform.database
