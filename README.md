# OptiSolve — Résolution de Problèmes d’Optimisation Linéaire

**OptiSolve** est une application interactive dédiée à la résolution de problèmes d’optimisation linéaire par la **méthode du Simplexe**.

Elle permet de modéliser facilement une fonction objectif et un système de contraintes, puis d’obtenir la solution optimale étape par étape via une interface conviviale.

---

## Objectif de l’application

- Résoudre des problèmes de **maximisation linéaire**
- Implémenter l’algorithme du **Simplexe**
- Visualiser les tableaux d’itérations
- Identifier la solution optimale (unique, multiple ou inexistante)

---

## Fonctionnalités

- Saisie du nombre de variables et contraintes
- Entrée des coefficients de la fonction objectif
- Construction automatique du tableau du simplexe
- Pivotage et itérations automatiques
- Détection des cas :
  - Solution optimale unique
  - Solutions multiples
  - Problème non borné

---

## Interface

Application développée avec **Streamlit** pour offrir :

- Une saisie intuitive
- L’affichage dynamique des tableaux
- La visualisation des étapes de résolution

---

## Structure du projet

```

├── optisolve.py        # Application principale Streamlit
├── formulaire.py       # Module de formulaire complémentaire
├── requirements.txt    # Dépendances Python
└── README.md

````

---

## Lancer l’application

```bash
git clone <repo-url>
cd <repo>
pip install -r requirements.txt
streamlit run optisolve.py
````

---

## 🛠️ Technologies utilisées

* Python
* NumPy
* Pandas
* Streamlit

---

## Auteur

**AKAKPO Codjo Ulrich Expéra**

Projet académique — Optimisation Linéaire & Recherche Opérationnelle.
