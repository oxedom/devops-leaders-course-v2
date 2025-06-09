#!/bin/bash
set -e

echo "Running tests..."
pytest ci/test_main.py -v

echo "Running black formatter..."
black --check main.py ci/

echo "Running flake8 linter..."
flake8 --config=ci/.flake8 main.py ci/

echo "Running bandit security checks..."
bandit -c ci/.bandit main.py

echo "Running trufflehog secret scanning..."
trufflehog --regex --entropy=False .

echo "All checks passed!" 