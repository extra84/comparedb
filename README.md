This scripts compares two IBM Notes Databases and displays documents not found in one of them
Only presence of documents is checked, not their content

Usage : 

`python comparedb.py SourceServer path\to\database.nsf TargetServer`

Use "" for local

This script requires an installed Notes client and pywin32 python extension.

Result is unpredictable if target server contains multiple replicas with the same ReplicaID
