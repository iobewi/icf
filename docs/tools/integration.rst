===========
Intégration
===========

GitHub Actions (exemple minimal)
--------------------------------
.. code-block:: yaml

   name: ICF CI
   on: [push, pull_request]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Build & test
           run: |
             echo "TODO: ajouter scripts de build/tests"
