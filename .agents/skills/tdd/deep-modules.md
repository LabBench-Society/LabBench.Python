# Deep Modules

From "A Philosophy of Software Design":

**Deep module** = small interface plus substantial implementation.

```text
+-------------------+
|  Small Interface  | <- Few methods, simple params
+-------------------+
|                   |
| Deep              |
| Implementation    | <- Complex logic hidden
|                   |
+-------------------+
```

**Shallow module** = large interface plus little implementation. Avoid this when possible.

```text
+-----------------------------+
|       Large Interface       | <- Many methods, complex params
+-----------------------------+
| Thin Implementation         | <- Just passes through
+-----------------------------+
```

When designing interfaces, ask:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?
