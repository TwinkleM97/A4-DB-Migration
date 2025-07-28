# PROG8850 - Assignment 4: Database Migration with Flyway and GitHub Actions

This project demonstrates advanced database migration using Flyway with both local and CI/CD workflows using GitHub Actions. It includes a reproducible MySQL environment using Docker, schema versioning through Flyway, and unit test validation for database operations.

---

### Prerequisites

- Docker
- Python 3.12+
- Ansible
- GitHub Codespaces (optional)
- `act` (for running GitHub Actions locally)

---

## Setup Instructions

### Step 1: Spin up MySQL and Adminer

We use a Docker Compose file (`mysql-adminer.yml`) to set up:
- MySQL container (exposed on port **3307**)
- Adminer UI for DB inspection (on port **8080**)

```bash
ansible-playbook up.yml
```

You can then access:
- Adminer: [http://localhost:8080](http://localhost:8080)
- MySQL CLI:
```bash
mysql -u root -h 127.0.0.1 -P 3307 -p
```

**Screenshot Proof:**  
![Ansible Setup](screenshots/6_ansible_up_success.png)

---

## Local Testing with ACT

To simulate GitHub Actions locally:

```bash
bin/act
```

If it fails (Codespaces), use:

```bash
bin/act -P ubuntu-latest=--self-hosted
```

The action installs the MySQL client and runs:

```yaml
- name: Deploy to Database
  env:
    DB_HOST: ${{ secrets.DB_HOST || '127.0.0.1' }}
    DB_USER: ${{ secrets.DB_ADMIN_USER || 'root' }}
    DB_PASSWORD: ${{ secrets.DB_PASSWORD  || 'Secret5555'}}
    DB_NAME: ${{ secrets.DB_NAME || 'mysql' }}
  run: mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < schema_changes.sql
```

**Screenshot Proof:**  
![ACT Local CI](screenshots/2_act_local_ci_success.png)

---

## GitHub Actions Workflow (`.github/workflows/mysql_actions.yml`)

When pushed to GitHub, the CI pipeline:

1. Spins up a MySQL Docker container
2. Installs `mysql-client`
3. Applies schema changes
4. Runs unit tests

**Screenshot Proof:**  
![GitHub CI Success](screenshots/1_github_actions_success.png)

---

## Flyway Migration

Migrations are stored in the `migrations/` folder. To run them:

```bash
docker run --rm \
  --network flyway-net \
  -v "$PWD/migrations:/flyway/sql" \
  redgate/flyway \
  -user=subuser \
  -password=subpass \
  -url=jdbc:mysql://my-mysql:3306/subscriptions?allowPublicKeyRetrieval=true\&useSSL=false \
  migrate
```

To inspect what Flyway ran:

```sql
SELECT * FROM flyway_schema_history;
```

**Screenshot Proof:**  
![Flyway Migration](screenshots/3_flyway_info.png)

---

## Unit Tests (tests/test_db.py)

This test file connects to the `subscriptions` DB and verifies:
- Insert
- Update
- Delete

```bash
python3 tests/test_db.py
```

**Screenshot Proof:**  
![Unit Tests Passed](screenshots/5_unit_tests_local_pass.png)

---

## Teardown

```bash
ansible-playbook down.yml
```

---

## File Overview

| File                   | Purpose                                                  |
|------------------------|----------------------------------------------------------|
| `mysql-adminer.yml`    | Local setup for MySQL + Adminer via Docker               |
| `mysql_actions.yml`    | GitHub Actions CI pipeline using MySQL service container |
| `migrations/`          | SQL migration files used by Flyway                       |
| `tests/test_db.py`     | Unit tests for verifying DB functionality                |
| `up.yml / down.yml`    | Ansible scripts to automate Docker stack lifecycle       |

---

## Summary

This repo demonstrates how to:
- Apply Flyway migrations to a MySQL DB
- Validate schema changes via CI/CD
- Run tests both locally and on GitHub Actions
- Inspect data via Adminer UI

This project ensures that DB migrations are version-controlled, reproducible, and testable across environments.

