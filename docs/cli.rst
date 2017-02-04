=====================
The command-line tool
=====================

Commands
========

Activity
--------

The activity command gets recent activity either for an account or for a project. By default it returns the first 20 events, but this can be increased with the ``--limit`` option.

Results are printed to standard out in CSV or JSON format. The default is to use CSV format.

Usage::

    python -m codebase activity <project> [--format=csv|json] [--limit=n]

