# Readme for Stage Builder
20 Jan 2024 - Mike Wise

## Installing Dependencies:

### Colored
```
pip install colored
```

### USD

```
git clone https://github.com/PixarAnimationStudios/OpenUSD
```

Open a developer console

```
python OpenUSD\build_scripts\build_usd.py "C:\USD"
```

## To run:

```
python buildstage.py -c BaeDefs.json -s DroneDesign -of out.usda -a a -r Admin
```

## Testing with Pytest
- `pip install pytest`
- pytest style tests are in the subdirectory `tests`
- Note that directory has an empty `__init__.py` in it, this is needed to mark it as a module - don't even think about deleteing it
- To run them all just enter `pytest tests`
- you can add tests by copying to a new test file (one starting with `test_`)
- And then to that file you just add test functions that are named starting with `test_`
- To run tests from the main directory:
      - `pytest tests/test_1.py`
      - `pytest -rP tests/test_1.py` - show captured output of passed tests
      - `pytest -rx tests/test_1.py` - show captured output of failed tests

## Code coverage
- First get the pytests running...
- `pip install coverage`
- `coverage run -m pytest -rP tests/test_1.py`
- `coverage report -m`