============
Installation
============

Ajout du composant
------------------
* Ajouter le composant ICF au dossier `components/`
* Ou via **IDF Component Manager** (si publié)

Exemple CMake
-------------
.. code-block:: cmake

   idf_component_register(SRCS "icf.c" INCLUDE_DIRS "include" REQUIRES nvs_flash)
