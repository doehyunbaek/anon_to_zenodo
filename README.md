anon-to-zenodo
==============

Command-line utility to create an (optionally anonymous) Zenodo deposition by zipping a directory and uploading via pre-configured credentials.

Usage
-----

Run (development checkout):

```
python -m anon_to_zenodo --title "My Dataset" --description "Short abstract" \
	--creator "Doe, Jane" --creator "Smith, John" \
	--dir . --license CC0-1.0
```

Key options:

* --creator: Repeat for each creator in form "Family, Given".
* --sandbox: Use Zenodo sandbox (for anonymous uploads/testing).
* --no-publish: Leave deposition as draft.
* --json: Emit full JSON response instead of just the HTML link.

Show full help:

```
python -m anon_to_zenodo --help
```

Version:

```
python -m anon_to_zenodo --version
```

Exit status 0 indicates success; non-zero indicates a failure before uploading.

License
-------
SPDX-License-Identifier: CC0-1.0
