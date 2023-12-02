# 6.0.0 - 2023-12-02 

## 🚨️ Breaking Changes

* Remove Python 3.7 support
* Changed SAE1850J configuration (see Bug fixes)
 
## 🐞 Bug Fix
* Adjusted the SAE-J1850 configuration to match the specification
    
    🚨️ For users which do rely on the previously misconfigured `SAEJ1850` settings a configuration named `SAE_J1850_ZERO` was added.


## 🔩  Internal / Development
* Add `python 3.12` to test matrix
* Re-lock dev dependencies

