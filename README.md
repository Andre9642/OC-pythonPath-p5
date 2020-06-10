# OC_py-p5: Utilisez les données publiques de l'OpenFoodFacts

# Installation
1. Install dependencies:
   $ pip install -r requirements.txt

2. Run main.py then choose administration
```
$ py -3.8 main.py
=== Menu principal ===
1 -- Quel aliment souhaitez-vous remplacer ?
2 -- Retrouver mes aliments substitués.
a -- Administration
q -- Quitter
> a
=== Administration ===
cdb  -- Créer la base de donnée
vsdb -- Voir la structure de la base de donnée
uc   -- Mettre à jour les catégories depuis l'API Open Food Facts
up   -- Mettre à jour les produits depuis l'API Open Food Facts
ddb  -- Supprimer la base de donnée
q    -- Quitter
b    -- Go back
>
```
3. Choose -- create database --.
```
> cdb
- Create database... OK
- Select database... OK
- Create table 'categories'... OK
- Create table 'products'... OK
- Create table 'substitute_products'... OK
=== Administration ===
cdb  -- Créer la base de donnée
vsdb -- Voir la structure de la base de donnée
uc   -- Mettre à jour les catégories depuis l'API Open Food Facts
up   -- Mettre à jour les produits depuis l'API Open Food Facts
ddb  -- Supprimer la base de donnée
q    -- Quitter
b    -- Go back
>
```
4. Choose -- update categories --.
```

```
5. Choose -- update products --.
6. Choose -- go back --.