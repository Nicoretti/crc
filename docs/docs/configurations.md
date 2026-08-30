---
icon: material/table-large
---

# Configurations

All CRC configurations which ship with the library, grouped by width.
Every configuration can be passed directly to a [`Calculator`](api/calculator.md):

```python
from crc import Calculator, Crc8

calculator = Calculator(Crc8.CCITT)
```

## Crc8 
=== "CCITT"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x00**
     - *Init Value:* **0x00**
     - *Rev Input:* **False**
     - *Polynomial:* **0x07**
     - *Rev Output:* **False**

    </div>
=== "SAEJ1850"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0xFF**
     - *Init Value:* **0xFF**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1D**
     - *Rev Output:* **False**

    </div>
=== "SAEJ1850_ZERO"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x00**
     - *Init Value:* **0x00**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1D**
     - *Rev Output:* **False**

    </div>
=== "AUTOSAR"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0xFF**
     - *Init Value:* **0xFF**
     - *Rev Input:* **False**
     - *Polynomial:* **0x2F**
     - *Rev Output:* **False**

    </div>
=== "BLUETOOTH"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x00**
     - *Init Value:* **0x00**
     - *Rev Input:* **True**
     - *Polynomial:* **0xA7**
     - *Rev Output:* **True**

    </div>
=== "MAXIM_DOW"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x00**
     - *Init Value:* **0x00**
     - *Rev Input:* **True**
     - *Polynomial:* **0x31**
     - *Rev Output:* **True**

    </div>
=== "ITU"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x55**
     - *Init Value:* **0x00**
     - *Rev Input:* **False**
     - *Polynomial:* **0x07**
     - *Rev Output:* **False**

    </div>
=== "ROHC"

    <div class="grid cards" markdown>

     - *Width:* **8**
     - *Final Xor:* **0x00**
     - *Init Value:* **0xFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0x07**
     - *Rev Output:* **True**

    </div>

## Crc16 
=== "XMODEM"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0x0000**
     - *Init Value:* **0x0000**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1021**
     - *Rev Output:* **False**

    </div>
=== "GSM"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0x0000**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1021**
     - *Rev Output:* **False**

    </div>
=== "PROFIBUS"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0xFFFF**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1DCF**
     - *Rev Output:* **False**

    </div>
=== "MODBUS"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0x0000**
     - *Init Value:* **0xFFFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0x8005**
     - *Rev Output:* **True**

    </div>
=== "IBM_3740"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0x0000**
     - *Init Value:* **0xFFFF**
     - *Rev Input:* **False**
     - *Polynomial:* **0x1021**
     - *Rev Output:* **False**

    </div>
=== "KERMIT"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0x0000**
     - *Init Value:* **0x0000**
     - *Rev Input:* **True**
     - *Polynomial:* **0x1021**
     - *Rev Output:* **True**

    </div>
=== "IBM"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0x0000**
     - *Init Value:* **0x0000**
     - *Rev Input:* **True**
     - *Polynomial:* **0x8005**
     - *Rev Output:* **True**

    </div>
=== "MAXIM"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0x0000**
     - *Rev Input:* **True**
     - *Polynomial:* **0x8005**
     - *Rev Output:* **True**

    </div>
=== "USB"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0xFFFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0x8005**
     - *Rev Output:* **True**

    </div>
=== "X25"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0xFFFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0x1021**
     - *Rev Output:* **True**

    </div>
=== "DNP"

    <div class="grid cards" markdown>

     - *Width:* **16**
     - *Final Xor:* **0xFFFF**
     - *Init Value:* **0x0000**
     - *Rev Input:* **True**
     - *Polynomial:* **0x3D65**
     - *Rev Output:* **True**

    </div>

## Crc32 
=== "CRC32"

    <div class="grid cards" markdown>

     - *Width:* **32**
     - *Final Xor:* **0xFFFFFFFF**
     - *Init Value:* **0xFFFFFFFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0x04C11DB7**
     - *Rev Output:* **True**

    </div>
=== "AUTOSAR"

    <div class="grid cards" markdown>

     - *Width:* **32**
     - *Final Xor:* **0xFFFFFFFF**
     - *Init Value:* **0xFFFFFFFF**
     - *Rev Input:* **True**
     - *Polynomial:* **0xF4ACFB13**
     - *Rev Output:* **True**

    </div>
=== "BZIP2"

    <div class="grid cards" markdown>

     - *Width:* **32**
     - *Final Xor:* **0xFFFFFFFF**
     - *Init Value:* **0xFFFFFFFF**
     - *Rev Input:* **False**
     - *Polynomial:* **0x04C11DB7**
     - *Rev Output:* **False**

    </div>
=== "POSIX"

    <div class="grid cards" markdown>

     - *Width:* **32**
     - *Final Xor:* **0xFFFFFFFF**
     - *Init Value:* **0x00000000**
     - *Rev Input:* **False**
     - *Polynomial:* **0x04C11DB7**
     - *Rev Output:* **False**

    </div>

## Crc64 
=== "CRC64"

    <div class="grid cards" markdown>

     - *Width:* **64**
     - *Final Xor:* **0x0000000000000000**
     - *Init Value:* **0x0000000000000000**
     - *Rev Input:* **False**
     - *Polynomial:* **0x42F0E1EBA9EA3693**
     - *Rev Output:* **False**

    </div>

