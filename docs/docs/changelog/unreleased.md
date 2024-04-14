# Unreleased

## 🚨 Breaking Changes

### Update of crc configurations
- **Rename:** The `Crc16.CCITT` configuration to `Crc16.XMODEM`.
- **New Addition:** Introduced `Crc16.KERMIT`, which matches the official configuration for `Crc16.CCITT`.

#### Decision Rationale
It was intentionally decided not to reintroduce `Crc16.CCITT` with the updated configuration. While it could have been added as an alias for `Crc16.KERMIT` or a replacement, omitting `Crc16.CCITT` ensures that client code will break upon update, thereby forcing maintainers to take notice and react accordingly.

#### Migration Guide
Below are solutions to the two common scenarios that need to be addressed due to this change:

1. **If you previously used `Crc16.CCITT` and expected the configuration defined [here](https://reveng.sourceforge.io/crc-catalogue/all.htm#crc.cat.crc-16-kermit):**

      **Solution:** Replace all usages of `Crc16.CCITT` in your code with `Crc16.KERMIT`.

2. **If you depended on or wanted to use the configuration values that `Crc16.CCITT` provided so far:**

      **Solution:** Replace all usages of `Crc16.CCITT` in your code with `Crc16.XMODEM`.

#### Related Issues
- [#148](https://github.com/Nicoretti/crc/issues/148)
- [#145](https://github.com/Nicoretti/crc/issues/145)

## 🔩  Internal
* Update `python-environment` action
* Add classifiers to `pyproject.toml`
