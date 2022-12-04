# Release Notes

## Unreleased 

### 🚨 Breaking API Changes 

** Renamed **

*Functions & Methods:*

* Renamed keyword argument `expected_checksum` of method `Calculator.verify` to `expected`

    === "Old API"

        ```python
        def verify(self, data: bytes, expected_checksum: int ) -> bool:
            ...
        ```
      
    === "New API"
      
        ```python
        def verify(self, data: Union[int, ByteString, BinaryIO, Iterable[ByteString]], expected: int ) -> bool:
            ...
        ```
 
### 🐛 Fixes
* Fixed return type for all inputs of ByteString types

### ✨ Added
* Added support for other data types than `bytes` to `Calculator.checksum` and `Calculator.verify`
 
     (`int`, `ByteString`, `BinaryIO`, `Iterable[ByteString]`)

### 📚 Documentation
* Renamed "Latest - Changes" to "Unreleased"
 

## 2.0.0 - 2022-11-27

### 🚨 Breaking API Changes 

** Renamed **

*Classes:*

* `AbstractCrcRegister` -> `AbstractRegister`
* `CrcRegisterBase` -> `BasicRegister`
* `CrcRegister` -> `Register`
* `TableBasedCrcRegister` -> `TableBasedRegister`
* `CrcCalculator` -> `Calculator`


*Functions & Methods:*

* `CrcCalculator.calculate_checksum` -> `Calculator.checksum`
* `CrcCalculator.verify_checksum` -> `Calculator.verify`
* \[public\] `argument_parser()` -> \[private\] `_argument_parser()`

*Arguments:*

* `CrcCalculator(configuration, table_based=False)` -> `Calculator(configuration, optimized=False)`

** Removed **

* Removed `CRC_TYPES` mapping
* Removed `checksum` function/cli-entry-point

### 🗑 Removed
* Removed checksum subcommand from CLI
* Removed `CRC_TYPES` mapping

### ✨ Added
* Added typing support
* Added Documentation [see here](https://nicoretti.github.io/crc)

### 🔧 Refactorings
* Fixed various linter warnings
