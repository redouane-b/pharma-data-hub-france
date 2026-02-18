# L'open data pharmaceutique en France : un guide complet des sources publiques

## Introduction

La France dispose d'un écosystème de données ouvertes particulièrement riche dans le domaine de la santé. Plusieurs bases publiques couvrent l'intégralité de la chaîne de valeur pharmaceutique : le référentiel des médicaments autorisés, les volumes de prescription, le registre des professionnels de santé, la cartographie des établissements, les liens financiers entre laboratoires et praticiens, et le maillage géographique du territoire.

Cet article propose un tour d'horizon structuré de ces sources. Chaque section présente une base de données, son contenu, son format technique, et sa place dans l'analyse du marché pharmaceutique français.

---

## Glossaire

Avant d'entrer dans le détail des bases, quelques définitions transversales utilisées dans l'ensemble de l'article.

### Le médicament : trois niveaux de lecture

Le système français distingue trois niveaux d'identification d'un médicament :

- **La molécule** (ou DCI — Dénomination Commune Internationale) : la substance active, indépendante de toute marque. Exemple : *metformine*, *paracétamol*. C'est le niveau d'analyse privilégié en pharmacologie et en études de marché.

- **La spécialité** : un produit commercial défini par une molécule, un dosage, une forme pharmaceutique et un laboratoire titulaire. Exemple : *GLUCOPHAGE 850 mg, comprimé pelliculé* (Merck). Identifiée par un **Code CIS** à 8 chiffres. Une même molécule donne lieu à de nombreuses spécialités (princeps et génériques).

- **La présentation** : le conditionnement physique vendu en pharmacie (la boîte). Identifiée par un **Code CIP13** à 13 chiffres — le code-barres scanné au comptoir. Une même spécialité peut avoir plusieurs présentations (boîte de 30, boîte de 90, flacon, etc.).

**En synthèse :** 1 molécule → N spécialités → N présentations.

### L'AMM (Autorisation de Mise sur le Marché)

Autorisation réglementaire obligatoire pour commercialiser un médicament en France. Délivrée après évaluation du rapport bénéfice/risque par l'ANSM (procédure nationale) ou l'EMA (procédure européenne). Une AMM peut être active, suspendue ou retirée.

### Le titulaire

Le laboratoire pharmaceutique qui détient l'AMM. C'est l'entité commerciale et réglementaire responsable du médicament : Sanofi, Pfizer, Servier, Mylan/Viatris, etc.

### La classification ATC

Le système ATC (Anatomical Therapeutic Chemical) est la classification internationale des médicaments, structurée en 5 niveaux hiérarchiques :
- Niveau 1 : système anatomique (A = appareil digestif, C = cardiovasculaire, N = système nerveux)
- Niveau 5 : substance chimique (A10BA02 = metformine)

C'est le langage standard de l'analyse pharma pour segmenter les marchés par aire thérapeutique.

### Market Access

Ensemble des activités visant à obtenir et maintenir l'accès au marché d'un médicament : dépôt du dossier réglementaire, évaluation par la HAS, négociation du prix avec le CEPS, inscription au remboursement. En France, cette fonction est stratégique car les prix sont administrés (fixés par négociation avec l'État, non libres).

### Ville vs. Hôpital

Le marché pharmaceutique français se divise en deux circuits distincts :
- **Ville** : médicaments prescrits par les médecins libéraux et dispensés en pharmacie d'officine.
- **Hôpital** : médicaments prescrits et administrés dans les établissements de santé.

Ces deux circuits ont des acteurs, des mécanismes de prix et des stratégies commerciales différents.

---

## 1. BDPM — Base de Données Publique des Médicaments

### Présentation

La BDPM est le référentiel officiel de l'ensemble des médicaments ayant obtenu une AMM en France. Elle est maintenue par l'ANSM et constitue la source de référence pour identifier un médicament, connaître sa composition, son prix, son taux de remboursement, son évaluation par la HAS et ses conditions de prescription.

| Propriété | Valeur |
|-----------|--------|
| Éditeur | ANSM |
| URL | base-donnees-publique.medicaments.gouv.fr |
| Format | Fichiers TXT, séparateur tabulation, pas d'en-tête |
| Encodage | UTF-8 |
| Volume | ~4 Mo au total (8 fichiers) |
| Mise à jour | Régulière |
| Licence | Accès libre |

La BDPM se compose de 8 fichiers liés entre eux par le **Code CIS**. Chaque fichier couvre une facette du médicament.

### 1.1 Fichier des spécialités (`CIS_bdpm.txt`)

Fichier central. Chaque ligne correspond à une spécialité pharmaceutique autorisée (ou dont la commercialisation a cessé depuis moins de deux ans).

| Champ | Description |
|-------|------------|
| Code CIS | Identifiant unique de la spécialité (8 chiffres). Clé de jointure principale de la BDPM. |
| Dénomination | Nom complet du médicament : marque, dosage et forme pharmaceutique. |
| Forme pharmaceutique | Comprimé, gélule, solution injectable, pommade, patch, collyre, etc. |
| Voies d'administration | Orale, intraveineuse, cutanée, inhalée, sous-cutanée, etc. Plusieurs valeurs possibles, séparées par « ; ». |
| Statut administratif de l'AMM | Autorisation active, suspendue ou retirée. |
| Type de procédure d'AMM | Nationale, européenne centralisée, décentralisée, reconnaissance mutuelle. |
| État de commercialisation | Indique si le médicament est effectivement commercialisé. Un médicament peut avoir une AMM active sans être disponible (rupture de stock, arrêt volontaire). |
| Date d'AMM | Date d'obtention de l'autorisation (format JJ/MM/AAAA). |
| Titulaire(s) | Laboratoire(s) détenteur(s) de l'AMM. Plusieurs valeurs possibles séparées par « ; ». |
| Surveillance renforcée | Oui/Non. Indique si le médicament fait l'objet d'une surveillance additionnelle (triangle noir ▼). |

**Remarque sur la voie d'administration :** ce champ a une portée analytique importante. Un médicament injectable intraveineux relève quasi systématiquement du circuit hospitalier (prescription spécialisée, administration par du personnel soignant). Un comprimé oral relève du circuit de ville (prescription libérale, dispensation en officine). Cette distinction conditionne la stratégie commerciale, les cibles de visite médicale et le circuit de distribution.

### 1.2 Fichier des présentations (`CIS_CIP_bdpm.txt`)

Décrit les conditionnements (boîtes) disponibles pour chaque spécialité. C'est le fichier qui porte les informations économiques : prix et remboursement.

| Champ | Description |
|-------|------------|
| Code CIS | Lien vers la spécialité. |
| Code CIP7 | Ancien identifiant de présentation à 7 chiffres (obsolète mais encore référencé). |
| Code CIP13 | Identifiant actuel à 13 chiffres. **Clé de jointure vers les données de prescription Open Medic.** |
| Libellé de la présentation | Description du conditionnement : « plaquette(s) thermoformée(s) de 30 comprimé(s) ». |
| Agrément aux collectivités | Oui, Non ou Inconnu. Indique si le médicament peut être acheté par les établissements de santé (hôpitaux, cliniques). |
| Taux de remboursement | Pourcentage pris en charge par l'Assurance Maladie. Valeurs possibles : 100%, 65%, 30%, 15%. |
| Prix du médicament en euro | Prix fabricant hors taxes. |
| Prix public en euro | Prix TTC incluant les marges de distribution. |
| Honoraires de dispensation | Rémunération du pharmacien pour l'acte de dispensation. |
| Indications ouvrant droit au remboursement | Texte précisant les indications spécifiques lorsqu'un même médicament a plusieurs taux de remboursement selon l'indication. |

#### Le système de remboursement français

Le taux de remboursement est directement lié à l'évaluation du SMR (voir section 1.4) :

| Taux | SMR correspondant | Signification |
|------|-------------------|---------------|
| 100% | Important (en ALD) | Affections de longue durée : cancer, diabète, maladies psychiatriques graves. Prise en charge intégrale. |
| 65% | Important | Service médical rendu jugé important. Catégorie standard des médicaments considérés comme nécessaires. |
| 30% | Modéré | Bénéfice médical reconnu mais limité. Reste à charge significatif pour le patient. |
| 15% | Faible | Bénéfice médical faible. Souvent un stade intermédiaire avant un déremboursement. |
| Non remboursé | Insuffisant | Médicament non pris en charge. Les volumes de prescription chutent significativement. |

**Prix administrés :** en France, les médicaments remboursés ont un prix fixé par négociation entre le laboratoire et le CEPS (Comité Économique des Produits de Santé). Le prix dépend directement de l'ASMR obtenue (voir section 1.5) : un médicament avec une ASMR I-III justifie un prix supérieur au comparateur ; une ASMR V impose un prix inférieur ou égal à l'existant.

### 1.3 Fichier des compositions (`CIS_COMPO_bdpm.txt`)

Contient la composition qualitative et quantitative en substances actives de chaque spécialité.

| Champ | Description |
|-------|------------|
| Code CIS | Lien vers la spécialité. |
| Désignation de l'élément pharmaceutique | Composant du médicament (comprimé, noyau, enrobage, etc.). |
| Code de la substance | Identifiant numérique de la substance. |
| Dénomination de la substance | Nom de la molécule en DCI : METFORMINE, PARACETAMOL, INSULINE GLARGINE. |
| Dosage | Quantité de substance active : 500 mg, 100 UI/ml. |
| Référence du dosage | Unité de référence : « pour un comprimé », « pour 1 ml ». |
| Nature du composant | **SA** (Substance Active) : le principe actif déclaré. **ST** (Fraction Thérapeutique) : la partie réellement active lorsque la substance est un sel ou un complexe. Exemple : dans le fumarate ferreux, la SA est le fumarate ferreux, la ST est le fer élémentaire. |

Ce fichier est indispensable pour passer d'une analyse par marque à une analyse par molécule. L'analyse de marché en pharmacie s'effectue au niveau de la substance active (ou de la classe ATC), pas au niveau de la marque commerciale. C'est en agrégeant toutes les spécialités contenant la même DCI que l'on obtient la taille réelle d'un marché moléculaire.

### 1.4 Fichier des avis SMR (`CIS_HAS_SMR_bdpm.txt`)

Le SMR (Service Médical Rendu) est l'évaluation par la Commission de la Transparence de la HAS du service médical apporté par un médicament. Il prend en compte la gravité de la pathologie, l'efficacité et les effets indésirables, la place dans la stratégie thérapeutique et l'existence d'alternatives.

| Champ | Description |
|-------|------------|
| Code CIS | Lien vers la spécialité. |
| Code de dossier HAS | Identifiant du dossier d'évaluation. Clé de jointure vers le fichier des liens CT. |
| Motif d'évaluation | Inscription, renouvellement d'inscription, réévaluation, extension d'indication. |
| Date de l'avis | Date de la décision de la Commission de la Transparence (format AAAAMMJJ). |
| Valeur du SMR | Important, Modéré, Faible, Insuffisant. |
| Libellé du SMR | Texte décrivant le niveau de SMR attribué. |

Le SMR détermine le taux de remboursement (voir section 1.2). Il est réévalué périodiquement (tous les 5 ans) ou à l'occasion de nouvelles données cliniques. Un médicament peut voir son SMR rétrogradé si de meilleures alternatives apparaissent sur le marché.

Un SMR « Insuffisant » entraîne le non-remboursement, ce qui se traduit dans la pratique par une chute des prescriptions — la majorité des patients et des prescripteurs s'orientant vers des alternatives prises en charge par la collectivité.

### 1.5 Fichier des avis ASMR (`CIS_HAS_ASMR_bdpm.txt`)

L'ASMR (Amélioration du Service Médical Rendu) évalue le progrès thérapeutique apporté par un médicament **par rapport aux traitements existants**. C'est l'évaluation qui détermine le prix.

| Champ | Description |
|-------|------------|
| Code CIS | Lien vers la spécialité. |
| Code de dossier HAS | Identifiant du dossier. |
| Motif d'évaluation | Inscription, réévaluation, etc. |
| Date de l'avis | Date de la décision (format AAAAMMJJ). |
| Valeur de l'ASMR | I (majeure) à V (inexistante). |
| Libellé de l'ASMR | Texte décrivant le niveau d'amélioration. |

Les cinq niveaux d'ASMR :

| Niveau | Signification | Conséquence sur le prix |
|--------|--------------|------------------------|
| I — Majeure | Progrès thérapeutique majeur. Cas exceptionnels (quelques attributions par décennie). | Prix libre, très élevé. |
| II — Importante | Amélioration importante en efficacité ou en réduction des effets indésirables. | Prix supérieur au comparateur. |
| III — Modérée | Amélioration modérée sur un critère clinique pertinent. | Prix supérieur au comparateur, dans une moindre mesure. |
| IV — Mineure | Amélioration mineure (commodité d'emploi, tolérance). | Faible marge de négociation tarifaire. |
| V — Inexistante | Absence d'amélioration par rapport à l'existant. Cas le plus fréquent. | Prix inférieur ou égal au comparateur. |

L'ASMR est le déterminant central de la négociation tarifaire avec le CEPS. L'écart de prix autorisé entre une ASMR III et une ASMR V peut représenter, sur la durée de vie commerciale d'un produit, des différences de revenus de plusieurs centaines de millions d'euros. C'est ce qui justifie l'investissement des laboratoires dans des essais cliniques comparatifs visant à démontrer la supériorité de leur produit.

### 1.6 Fichier des liens vers les avis CT (`HAS_LiensPageCT_bdpm.txt`)

Fichier de référence associant chaque code de dossier HAS à l'URL de l'avis complet de la Commission de la Transparence. Permet d'accéder au raisonnement détaillé ayant conduit à l'attribution d'un SMR ou d'un ASMR.

| Champ | Description |
|-------|------------|
| Code de dossier HAS | Clé de jointure vers les fichiers SMR et ASMR. |
| Lien vers la page d'avis CT | URL de l'avis complet sur le site de la HAS. |

### 1.7 Fichier des groupes génériques (`CIS_GENER_bdpm.txt`)

Cartographie le répertoire des génériques : quels médicaments sont interchangeables.

| Champ | Description |
|-------|------------|
| Identifiant du groupe générique | Regroupe l'ensemble des spécialités bioéquivalentes. |
| Libellé du groupe | Nom du groupe : DCI + dosage + forme. |
| Code CIS | Lien vers la spécialité membre du groupe. |
| Type de générique | 0 = princeps, 1 = générique, 2 = générique par complémentarité posologique, 4 = générique substituable. |

#### Princeps, génériques et substitution

Le **princeps** est le médicament original, développé par un laboratoire innovant et protégé par un brevet (~20 ans à compter du dépôt, soit environ 10-12 ans de commercialisation effective après les phases de développement clinique).

À l'expiration du brevet, les **génériques** entrent sur le marché. Ils contiennent la même substance active, au même dosage, sous la même forme pharmaceutique, et ont démontré leur bioéquivalence avec le princeps. Ils sont commercialisés à un prix inférieur (environ 60% du prix du princeps initialement, avec des baisses successives).

En France, le pharmacien est habilité — et financièrement incité — à **substituer** un princeps par un générique (type 4 : substituable), sauf mention contraire du prescripteur (« non substituable » sur l'ordonnance). Ce mécanisme entraîne une érosion rapide des parts de marché du princeps après la perte du brevet (« patent cliff »), avec une perte de 50 à 80% des volumes en quelques mois.

Ce fichier permet d'identifier, pour chaque molécule, le stade du cycle de vie : marché sous brevet (princeps seul) ou marché générique (concurrence ouverte).

### 1.8 Fichier des conditions de prescription et de délivrance (`CIS_CPD_bdpm.txt`)

Définit le cadre réglementaire de prescription de chaque médicament.

| Champ | Description |
|-------|------------|
| Code CIS | Lien vers la spécialité. |
| Condition de prescription ou de délivrance | Texte décrivant la condition applicable. |

Les principales conditions :

| Condition | Description |
|-----------|------------|
| Liste I | Médicament sur ordonnance, non renouvelable sans nouvelle prescription. |
| Liste II | Médicament sur ordonnance, renouvelable. |
| Stupéfiants | Ordonnance sécurisée obligatoire. Durée de prescription limitée (7 à 28 jours). |
| Prescription hospitalière | Prescription réservée aux médecins hospitaliers. |
| Prescription initiale hospitalière | Première prescription hospitalière, renouvellement possible en ville. |
| Prescription réservée aux spécialistes | Prescription limitée à certaines spécialités médicales (ex : oncologues, endocrinologues). |
| Médicament d'exception | Ordonnance spéciale à 4 volets, prescription restreinte à des indications précises. |

Ces conditions définissent l'univers des prescripteurs potentiels. Un médicament en prescription hospitalière n'a aucun prescripteur en médecine de ville ; un médicament réservé aux spécialistes restreint la cible aux praticiens de la spécialité concernée. Cette information est structurante pour la segmentation et le ciblage commercial.

### Relations entre les fichiers

Le **Code CIS** est la clé de jointure centrale. Tous les fichiers s'y rattachent, à l'exception du fichier des liens CT qui se lie aux fichiers SMR et ASMR par le **Code de dossier HAS**.

```
CIS_bdpm.txt
 ├── CIS_CIP_bdpm.txt        (Code CIS)
 ├── CIS_COMPO_bdpm.txt       (Code CIS)
 ├── CIS_HAS_SMR_bdpm.txt     (Code CIS)
 │    └── HAS_LiensPageCT     (Code de dossier HAS)
 ├── CIS_HAS_ASMR_bdpm.txt    (Code CIS)
 │    └── HAS_LiensPageCT     (Code de dossier HAS)
 ├── CIS_GENER_bdpm.txt        (Code CIS)
 └── CIS_CPD_bdpm.txt          (Code CIS)
```

### Limites de la BDPM

La BDPM est un référentiel produit. Elle ne contient pas :

- **Les volumes de prescription** — couverts par Open Medic (section suivante).
- **La classification ATC** — absente de la BDPM standard, disponible dans Open Medic et dans des référentiels complémentaires.
- **Les données de pharmacovigilance** — disponibles sur data.ansm.sante.fr.
- **Les liens financiers laboratoires-praticiens** — couverts par Transparence Santé.

---

## 2. Open Medic — Données de prescription

*Section à venir.*

---

## 3. RPPS — Annuaire des professionnels de santé

*Section à venir.*

---

## 4. FINESS — Répertoire des établissements de santé

*Section à venir.*

---

## 5. INSEE COG — Référentiel géographique

*Section à venir.*

---

## 6. Transparence Santé — Liens d'intérêts laboratoires-praticiens

*Section à venir.*

---

## 7. data.ansm — Pharmacovigilance

*Section à venir.*
