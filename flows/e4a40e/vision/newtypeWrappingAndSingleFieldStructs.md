# Newtype wrapping and single-field structs

## 2026-09-03 — a single-field struct is really bad design; never want that pattern to spread

The flow's datom examples used Failure.{ Text } and Sorted.{ Vector<Ordered> }.

> I don't like your failure example because it creates a single-field struct, which would be really bad design, and I would never want that kind of pattern to start spreading. Also, even your first example is a single-field struct, which is a really bad design

-- psyche, STT.
