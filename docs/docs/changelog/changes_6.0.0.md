---
icon: material/tag-outline
---

# 6.0.0 - 2023-12-02 

## :material-alert-decagram: Breaking Changes

* Remove Python 3.7 support
* Changed SAE1850J configuration (see Bug fixes)
 
## :material-bug: Bug Fix
* Adjusted the SAE-J1850 configuration to match the specification
    
    :material-alert-decagram: For users which do rely on the previously misconfigured `SAEJ1850` settings a configuration named `SAEJ1850_ZERO` was added.


## :material-cog: Internal / Development
* Add `python 3.12` to test matrix
* Re-lock dev dependencies

