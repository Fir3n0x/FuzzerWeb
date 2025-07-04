# Fuzzer HTTP

> **Avertissement légal** Utilisez ce script uniquement sur des cibles que vous possédez ou pour lesquelles vous avez une autorisation écrite. L’attaque non autorisée de systèmes informatiques est illégale.

---

## Présentation

Ce script Python réalise un directory/file fuzzing :
il balaie une liste de chemins (wordlist) à la recherche de ressources HTTP potentiellement accessibles sur un domaine donné.

Il gère:
* l’exécution multithread (nombre de threads configurable) ;
* l’affichage temps‑réel de la progression avec code couleur ;
* un filtrage simple pour éviter d’afficher plusieurs fois la même redirection / même page (même code HTTP et même taille de réponse) ;
* l’arrêt propre via Ctrl‑C en affichant les résultats collectés jusqu’alors.

## Prérequis

| Outil / Librairie | Version conseillée |
| ----------------- | ------------------ |
| **Python**        | 3.8+               |
| **requests**      | >=2.31             |
| **termcolor**     | >=2.4              |


Installation rapide:

```bash
python -m venv venv
source venv/bin/activate        # sous Windows : venv\Scripts\activate
pip install requests termcolor
```

(ou)

```bash
pip install -r requirements.txt
```


## Utilisation

```bash
python fuzzer.py <domaine> <chemin_wordlist> <nb_threads>
```

Exemple:

```bash
python fuzzer.py site.com wordlists/common.txt 30
```

## Author

**Corentin Mahieu** – [@Fir3n0x](https://github.com/Fir3n0x)
