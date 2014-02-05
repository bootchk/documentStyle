Classes for domains of style property values.

Rationale:
- framework enum classes are not pickleable
-- enums of int (deficiency of PySide pickling)
-- other classes where Qt does not define an enum( graphicsEffect )
- enum names are not i18n.  This provides internationalized names.

Models are sets of named values.
Names are i18n: displayable in spoken language of locale.
Currently, all such sets are displayed by ComboBoxStyleProperty.

See styleWrapper for classes that wrap domain instances.

The API for a Model is:

- has an attribute 'values', a dictionary that maps names to enum values
- has a method default() that returns the default value (of the framework) from the domain