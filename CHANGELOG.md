## 3.4.0

* Allow `HistorySession` instances to be used as decorators, expose `history.session`
  as a convenience method that automatically calls `get_backend`
* Unit tests for `HISTORY_MIDDLEWARE_IGNORE`


## 3.3.0

* [sqlite] Better handling of nested JSON within update trigger `changes`
* Added a `session` CLI subcommand (`manage.py triggers session`) to output the SQL for
  starting a history session (does not work for sqlite, which uses user-defined
  functions for history sessions).


## 3.2.0

* Added `history.contrib.migrate` and `history.contrib.loaddata` apps that provide
  wrappers of Django management commands that run within history sessions


## 3.1.1

* Included missing `admin_history.html` template in distribution


## 3.1.0

* Added a `HISTORY_FILTER` setting for excluding models/fields from history, and exclude
  `BinaryField`s from history by default
* Added a `HISTORY_SNAPSHOTS` setting to allow disabling full object snapshots
* Store JSONField values in `snapshot` and `changes` as actual JSON on SQLite


## 3.0.1

* Fixed support for older versions of Postgres without `CREATE OR REPLACE TRIGGER`
* Included README in PyPI


## 3.0.0

* Store all history in a single table, using `ContentType`s
* Record a JSON snapshot and changes (when appropriate) for each historical entry
* Introduce a session-based API for better grouping of historical changes
* Allow customization of object history using a swappable model
* Added SQLite support
