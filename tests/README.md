# Test Scripts

This directory contains test scripts for various components of Penguin Overlord.

## Test Files

### `test_secrets.py`
Tests the secrets management system (Doppler, AWS, Vault integration).

```bash
python tests/test_secrets.py
```

### `test_comic_command.py`
Tests the comic posting functionality.

```bash
python tests/test_comic_command.py
```

### `test_fetcher.py`
Tests the optimized news fetcher with ETag caching.

```bash
python tests/test_fetcher.py
```

### `test_us_legislation.py`
Tests US legislation RSS feed accessibility.

```bash
python tests/test_us_legislation.py
```

## Running All Tests

```bash
# From project root
for test in tests/test_*.py; do
    echo "Running $test..."
    python "$test"
    echo "---"
done
```

## Adding New Tests

1. Create `test_<feature>.py` in this directory
2. Follow the naming convention: `test_<component>.py`
3. Add documentation to this README
4. Use descriptive assertions and error messages
