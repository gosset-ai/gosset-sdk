# Publishing Guide

## Publishing to PyPI

### Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Create PyPI account at https://pypi.org/account/register/

3. Create API token at https://pypi.org/manage/account/token/

### Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/gosset_sdk-0.1.0-py3-none-any.whl` (wheel)
- `dist/gosset-sdk-0.1.0.tar.gz` (source)

### Test the Build

Install locally to test:

```bash
pip install dist/gosset_sdk-0.1.0-py3-none-any.whl
gosset --version
```

### Upload to TestPyPI (Optional)

Test on TestPyPI first:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ gosset-sdk
```

### Upload to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### Verify Publication

```bash
pip install gosset-sdk
gosset --version
```

## Version Management

### Update Version

1. Update version in `pyproject.toml`:
```toml
version = "0.2.0"
```

2. Update version in `gosset_sdk/__init__.py`:
```python
__version__ = "0.2.0"
```

3. Update CHANGELOG (create if needed)

4. Commit and tag:
```bash
git add .
git commit -m "Release v0.2.0"
git tag v0.2.0
git push origin main --tags
```

### Semantic Versioning

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards-compatible)
- **PATCH**: Bug fixes (backwards-compatible)

Examples:
- `0.1.0` → `0.1.1` (bug fix)
- `0.1.1` → `0.2.0` (new features)
- `0.9.9` → `1.0.0` (stable release)

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add PyPI token to GitHub secrets:
1. Go to repository Settings → Secrets → Actions
2. Add `PYPI_API_TOKEN` with your PyPI token

## Pre-release Checklist

Before publishing a new version:

- [ ] All tests pass
- [ ] Documentation is up-to-date
- [ ] CHANGELOG is updated
- [ ] Version numbers are bumped
- [ ] Package builds successfully
- [ ] Test installation works
- [ ] CLI commands work
- [ ] Examples run successfully
- [ ] README has correct installation commands
- [ ] License file is present
- [ ] No sensitive data in code

## Post-release Tasks

After publishing:

1. Create GitHub release with changelog
2. Update documentation site
3. Announce on relevant channels
4. Monitor issue tracker for bug reports
5. Test installation on clean environment

## Troubleshooting

### Build Errors

If build fails:
```bash
# Check setup files
python setup.py check

# Validate package
twine check dist/*
```

### Upload Errors

If upload fails:
- Check PyPI API token is valid
- Verify version number is unique
- Ensure all required fields in pyproject.toml

### Import Errors After Install

If package imports fail:
- Check `__init__.py` has correct exports
- Verify package structure in `setup.py`
- Test with `pip install -e .` first

