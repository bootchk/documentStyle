Classes for domains of style property values.

Where:
- framework enum classes are not pickleable
-- enums of int (deficiency of PySide pickling)
-- other classes where Qt does not define an enum( graphicsEffect )

Models are sets of named values.
Currently, all such sets are displayed by ComboBoxStyleProperty.

See styleWrapper for classes that wrap domain instances.