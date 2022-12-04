# Unreleased 

## 🚨 Breaking API Changes 

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
 
## 🐛 Fixes
* Fixed return type for all inputs of ByteString types

## ✨ Added
* Added support for other data types than `bytes` to `Calculator.checksum` and `Calculator.verify`
 
     (`int`, `ByteString`, `BinaryIO`, `Iterable[ByteString]`)

## 📚 Documentation
* Renamed "Latest - Changes" to "Unreleased"
* Added "API" section
* Added "development" section
