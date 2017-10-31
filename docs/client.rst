================
Client reference
================




.. py:module:: codebase

.. autoclass:: Client
   :members:

   Note that most methods return a generator of results. API requests are lazy, so a request isn't made until the first result is accessed, and if the results are paginated then additional requests are made only when you access results from subsequent pages.

   Most of the Codebase API methods return 20 results per page. Some API methods (such as the API to get all the projects associated with an account) are not paginated and return all results in one page.

.. autoclass:: BaseClient
   :members:
