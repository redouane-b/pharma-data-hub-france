Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — Partie 3/5 : RPPS.

Le RPPS (Répertoire Partagé des Professionnels de Santé) est la base nationale de référence de l'ensemble des professionnels intervenant dans le système de santé français. Maintenu par l'ANS (Agence du Numérique en Santé) et diffusé en open data sur data.gouv.fr, il recense les médecins, pharmaciens, infirmiers, chirurgiens-dentistes, sages-femmes et tous les autres professionnels de santé actifs en France — avec leur spécialité, leur mode d'exercice et leur localisation géographique. Là où Open Medic répond à la question « ce médicament est-il prescrit, par qui et en quelle quantité ? », le RPPS répond à la question « qui sont ces prescripteurs, où sont-ils et quelle est leur spécialité ? »

Le RPPS est un référentiel **opposable** : les données enregistrées sont fiables car elles proviennent des autorités d'enregistrement (les ordres professionnels, le service de santé des armées, les agences régionales de santé, les employeurs). Chaque professionnel se voit attribuer un **numéro RPPS à 11 chiffres**, pérenne et non signifiant, qu'il conserve toute sa carrière. Ce numéro est la clé de jointure principale vers Transparence Santé et Open Medic.

Historique : RPPS vs ADELI

Avant le RPPS, les professionnels de santé sans Ordre étaient enregistrés dans le répertoire **ADELI** (Automatisation des Listes), géré par les agences régionales de santé (ARS). ADELI a progressivement été remplacé par le RPPS depuis 2012 selon le calendrier suivant :

| Année | Professions basculées vers le RPPS |
|-------|-----------------------------------|
| 2012 | Médecins, chirurgiens-dentistes, pharmaciens, sages-femmes |
| 2017 | Masseurs-kinésithérapeutes |
| 2018 | Pédicures-podologues |
| 2022 | Infirmières |
| Octobre 2024 | Dernières professions ADELI — ADELI est désormais décommissionné |

ADELI présentait des fragilités structurelles : les professionnels n'étaient pas incités à se désinscrire lors de la cessation d'activité (inscription gratuite, contrairement au RPPS), ce qui tendait à **surestimer** les effectifs actifs. À l'inverse, les nouveaux professionnels débutant par une activité salariée tardaient parfois à s'enregistrer, **sous-estimant** la part des plus jeunes. Pour limiter ce biais, seuls les effectifs de moins de 62 ans étaient retenus dans les fichiers ADELI.

**Cas particuliers post-bascule :** Pour les kinésithérapeutes, un recalage des effectifs salariés a été nécessaire à partir des données de la SAE (enquête statistique annuelle des établissements de santé). Pour les infirmières, la qualité insuffisante des données RPPS a conduit la DREES à construire des statistiques à partir de la Base Tous Salariés (BTS) et du SNDS plutôt que du RPPS. Les aides-soignantes ne font pas partie du périmètre RPPS.

Champ couvert

Le RPPS couvre l'ensemble des professionnels ayant déclaré **au moins une activité en cours** (libérale ou salariée, remplaçante ou non) en France métropolitaine et dans les DROM. Sont exclus : les bénévoles, les étudiants / internes / docteurs juniors, et les professionnels exerçant exclusivement pour les Services de santé des Armées (SSA).

3. RPPS / ADELI — Démographie des professionnels de santé (DREES)
Lien données : https://www.data.gouv.fr/fr/datasets/la-demographie-des-professionnels-de-sante-depuis-2012
Producteur : DREES / OSAM | Licence : Licence Ouverte v2.0 (Etalab) | Mise à jour : annuelle
Format : Excel (.xlsx), une ligne par combinaison de dimensions (territoire × mode d'exercice × tranche d'âge × sexe)
Grain : statistiques agrégées — pas de données individuelles nominatives
Périmètre : France entière et DROM, depuis 2012, selon la source disponible par profession (RPPS, ADELI, BTS ou SNDS)

Structure : un fichier Excel par profession ou groupe de professions. Chaque fichier contient plusieurs onglets :

| Onglet | Contenu | Professions |
|--------|---------|-------------|
| `Effectifs` | Actifs occupés au 1er janvier, déclinés par territoire, mode d'exercice, tranche d'âge, sexe | Toutes |
| `Ages moyens` | Âge moyen selon les mêmes dimensions | Toutes |
| `Densités` | Pour 100 000 habitants selon les mêmes dimensions | Toutes |
| `Effectifs par spécialités` | Effectifs détaillés par spécialité exercée | Médecins uniquement |
| `Effectifs par lieu diplôme` | Région du diplôme vs région d'activité | Médecins uniquement |
| `Nombre d'activités` | Nombre d'activités en cours au 1er janvier | Médecins uniquement |

Données disponibles :

territoire / region / departement : niveau géographique — France entière, région (code + libellé) ou département (code + libellé). Clé de jointure vers le COG INSEE pour les taux pour 100 000 habitants.
exercice : mode d'exercice — `1-Libéral`, `2-Salarié`, `3-Mixte` ou `0-Ensemble`. La distinction libéral/salarié est structurante pour l'analyse de marché : les médecins libéraux génèrent des prescriptions directement remboursées par la CNAM (visibles dans Open Medic), les salariés sont agrégés sous PSP_SPE = 90.
tranche_age : tranche d'âge quinquennale ou décennale (ex. `03-30-34 ans`, `07-50-54 ans`) ou `00-Ensemble`.
sexe : `1-Hommes`, `2-Femmes` ou `0-Ensemble`.
effectif_YYYY : effectifs d'actifs occupés au 1er janvier de l'année YYYY (une colonne par année disponible).
am_YYYY : âge moyen des actifs au 1er janvier de l'année YYYY.
densite_YYYY : nombre d'actifs pour 100 000 habitants au 1er janvier de l'année YYYY.
specialites / specialites_agregees : spécialité médicale exercée et regroupement par grande famille (médecins uniquement).
secteur_activite : secteur d'exercice principal (autres professions, principalement via ADELI).

Exemples d'utilisation des données :
Pour donner des exemples d'utilisation, nous allons essayer de répondre à trois questions concrètes à partir des fichiers DREES.

1. Combien y a-t-il de professionnels de santé en France et comment se répartissent-ils par profession ?
Les fichiers DREES recensent plusieurs centaines de milliers de professionnels actifs, répartis entre une vingtaine de professions. Les infirmiers constituent le groupe le plus nombreux, devant les médecins et les masseurs-kinésithérapeutes. L'effectif total est obtenu en agrégeant la ligne `0-Ensemble` (territoire = France entière, exercice = Ensemble, tranche_age = Ensemble, sexe = Ensemble) de chaque fichier pour la dernière année disponible.

Press enter or click to view image in full size

Source : Git

2. Comment les médecins se répartissent-ils par spécialité ?
Le fichier `Médecins RPPS 2012-2025.xlsx` fournit les effectifs par spécialité depuis 2012. La médecine générale représente environ 45 % des médecins actifs, confirmant son rôle de pivot du système ambulatoire. Parmi les spécialités, les plus représentées sont la psychiatrie, la cardiologie, la pédiatrie, la dermatologie et la gynécologie-obstétrique — soit exactement les spécialités dont les volumes de prescription sont les plus visibles dans Open Medic. La colonne `specialites` dans l'onglet `Effectifs par spécialités` offre une granularité fine permettant de cartographier précisément le vivier de prescripteurs pour chaque spécialité.

Press enter or click to view image in full size

Source : Git

3. Comment se répartit le territoire médical en France ?
La France présente des inégalités de densité médicale marquées entre régions et départements. Les grandes métropoles (Paris, Lyon, Marseille, Bordeaux, Toulouse) concentrent les effectifs les plus élevés, à la fois parce que la population y est dense et parce que les structures hospitalières et universitaires y attirent les spécialistes. À l'opposé, les zones rurales et périurbaines de faible densité — les « déserts médicaux » — présentent des déficits structurels en médecins généralistes, avec des délais de rendez-vous et des taux de renoncement aux soins significativement plus élevés.

La colonne `densite_YYYY` dans les fichiers DREES donne directement le nombre d'actifs pour 100 000 habitants par région et département, sans nécessiter de croisement externe avec les données de population INSEE.

Press enter or click to view image in full size

Source : Git

Traitement DREES des données RPPS

La DREES (Direction de la recherche, des études, de l'évaluation et des statistiques) produit chaque année un bilan démographique à partir d'une extraction du RPPS au 1er janvier sur le site de l'ANS. Les données utilisées sont en accès restreint (plus complètes que l'open data public, incluant notamment l'âge des professionnels).

Le traitement DREES suit six étapes :

1. **Définition des communes d'activité** — à partir du code commune INSEE s'il est renseigné, sinon par le code postal ou le libellé de commune.
2. **Fusion des tables** — activités, coordonnées des structures, profil du professionnel (état civil, conditions d'exercice, autorisations), diplômes obtenus en France ou à l'étranger.
3. **Sélection des activités en cours** — filtrées par date de début/fin ; exclusion des étudiants/internes, des activités SSA et des activités bénévoles.
4. **Construction de la table par professionnel** — agrégation des activités par RPPS. Il n'existe pas de notion d'activité principale dans le RPPS : les 5 activités les plus récentes sont conservées par professionnel. En 2025, les professionnels exercent en moyenne 1,4 activités (plus de 75 % n'en exercent qu'une seule).
5. **Création de variables synthétiques** — mode d'exercice (libéral / salarié / mixte) et spécialités médicales à partir des savoir-faire déclarés.
6. **Sélection du champ** — France métropolitaine et DROM uniquement.

Note : En 2024, l'extraction a été réalisée au 30 septembre. La DREES a reconstruit l'activité au 1er janvier en utilisant les dates de début et de fin d'activité.

Limites:
Les données DREES sont des statistiques agrégées — elles ne permettent pas d'identifier des professionnels individuels. Quatre limites importantes conditionnent leur utilisation analytique.

Des données agrégées sans identifiants individuels. Les fichiers DREES ne contiennent pas de numéro RPPS individuel ni de nom. Pour obtenir une liste nominative de prescripteurs (ciblage SFE, études terrain), il faut se tourner vers l'annuaire ANS (données open data en accès libre sur data.gouv.fr ou annuaire.sante.fr), qui conserve les données individuelles au format TXT pipe-séparé.

L'absence de données d'activité prescriptrice. Les effectifs DREES indiquent qu'un médecin est actif et connaissent sa spécialité et son mode d'exercice, mais pas le volume ou la nature de ses prescriptions. Pour passer du dénombrement à l'activité prescriptrice réelle, le croisement avec Open Medic (volume par spécialité) ou avec Transparence Santé (avantages reçus par praticien) est indispensable.

Hétérogénéité des sources selon les professions. Les effectifs de chaque profession proviennent de sources différentes (RPPS, ADELI, BTS, SNDS) dont les périmètres et les dates de référence ne sont pas parfaitement harmonisés. Les comparaisons inter-professions doivent tenir compte de ces hétérogénéités, notamment pour les années de transition ADELI → RPPS.

Les infirmières et aides-soignantes hors périmètre RPPS. Malgré la bascule au RPPS en 2022, la qualité insuffisante des données infirmières conduit la DREES à produire leurs statistiques à partir de sources alternatives (BTS pour les salariées, SNDS pour les libérales). Les aides-soignantes ne font pas partie du périmètre RPPS. Ces deux professions disposent donc de séries temporelles plus courtes et avec moins de dimensions de ventilation.

Ce qui vient ensuite :
Le RPPS donne la liste des prescripteurs ; FINESS donne la liste des établissements dans lesquels ils travaillent. Pour cartographier les hôpitaux, cliniques et centres spécialisés, et comprendre le marché hospitalier dans lequel prescriptions et achats de médicaments sont réalisés sans passer par la pharmacie d'officine, il faut FINESS — objet de la Partie 4.
