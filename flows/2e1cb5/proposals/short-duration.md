Presentation.{ «A Duration before the intrinsic» Proposal }

# A Duration before the intrinsic

Created by Fable 5.1, alone.

### Proposal 1: A Duration before the intrinsic · psyche-belief › vision/short-ethos.md

::: comment
Flow 0.53.2 wants a Duration and ethos-zero 17 has no such intrinsic; a declared newtype is a type, an integer field a bare scalar.
:::

+ Until ethos-zero knows Duration, a contract that needs one declares it in its own library, a newtype over an Integer of milliseconds, and the declaration goes when the intrinsic lands.

```ethos
+ Duration.Integer   ; milliseconds
```
