# Unreleased

## 🐞 Bug Fix
* Adjusted the SAE-J1850 configuration to match the specification
    
    🚨️ For users which do rely on the previously misconfigured `SAEJ1850` settings a configuration named `SAE_J1850_ZERO` was added.

##  Breaking Changes
* Remove Python 3.7 support

## 🔩  Internal / Development
* Add `python 3.12` to test matrix
* Re-lock dev dependencies

