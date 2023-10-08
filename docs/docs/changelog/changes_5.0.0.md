# 5.0.0 - 2023-10-08 

🚀 This release is powered by **Gert van Dijk**, thank you for your contribution!

## 🚨 Breaking Changes
* Move from a single-file/module to an ‘src-based layout’ package.

    The layout of the source repository has changed from single file `crc.py` in the
    root into a package where `crc.py` is now a private module `_crc.py` of package
    `crc`.

    ```
    src/
    └── crc/
        ├── _crc.py
        └── __init__.py
    ```

    `__init__.py` re-exports all the public entities from the private module, so that
    typical imports like `from crc import Calculator` remain working as-is.

    The need and choice for this new layout is discussed in [Issue #110][issue-110].

* The shebang line on the main `src/crc/_crc.py` file (formerly `crc.py`) has been
  removed.

    This shouldn't affect anyone installing `crc` as package. Both the entrypoint `crc`
    and the package-level `__main__` remain in place.

    However, in case you were to obtain the `src/crc/_crc.py` file (formerly `crc.py`)
    and mark it as executable afterwards to run it directly, then this change may affect
    you. Running the `main()` function can then still be achieved by either:

    - `python path/to/crc.py`
    - `python -m crc` (if the module is on your `PYTHON_PATH`)

## ✨ Added
* Add `py.typed` marker to indicate the `crc` package ships with type information. The
  type information was added inline since [2.0.0](changes_2.0.0.md), but the marker file
  was missing in the package, so type checkers did not consider the type information.
  This eliminates the use of `ignore_missing_imports` (mypy) or `reportMissingTypeStubs`
  (Pylance/Pyright) in downstream projects.

## 📚 Documentation
* Add contributors page

## 🔩  Internal / Development
* Several improvements to type annotations:
    * Conform to mypy in strict mode.
    * Type information now follows a more modern syntax by implementing recommendations
        from PEPs [563][PEP 563], [585][PEP 585], [604][PEP 604] while maintaining
        support for Python 3.8.
    * Declare all instance variables on classes.
    * Create a Type Alias for a complex Union used repetitively.
* Remove unnecessary parentheses and `start` argument in `range()`.
* Remove unused imports.
* Update lockfile.

[issue-110]: https://github.com/Nicoretti/crc/issues/110
[PEP 563]: https://peps.python.org/pep-0563/
[PEP 585]: https://peps.python.org/pep-0585/
[PEP 604]: https://peps.python.org/pep-0604/
