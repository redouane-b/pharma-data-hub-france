Sidebar menu
Search

Get app
Write
Notifications

Redouane
Home
Library
Profile
Stories
Stats
Following
Joseph Rocca
Joseph Rocca
Find writers and publications to follow.

See suggestions
Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — Partie 1/5 : Base de Données Publique des Médicaments.
Redouane
Redouane
6 min read
·
6 days ago




La France dispose d’un écosystème de données ouvertes particulièrement riche dans le domaine de la santé. Plusieurs bases publiques couvrent l’intégralité de la chaîne de valeur pharmaceutique : le référentiel des médicaments autorisés, les volumes de prescription, le registre des professionnels de santé, la cartographie des établissements, les liens financiers entre laboratoires et praticiens, et le maillage géographique du territoire. Cette série se propose d’explorer ces bases de données publiques.

Glossaire:
Avant d’entrer dans le détail des bases, quelques définitions transversales utilisées dans l’ensemble de l’article.

Le médicament : trois niveaux de lecture
Le système français distingue trois niveaux d’identification d’un médicament:
- La molécule (ou DCI — Dénomination Commune Internationale) : la substance active, indépendante de toute marque. C’est le niveau d’analyse privilégié en pharmacologie et en études de marché.
Exemple : paracétamol.
- La spécialité : un produit commercial défini par une molécule, un dosage, une forme pharmaceutique et un laboratoire titulaire. Identifiée par un Code CIS à 8 chiffres. Une même molécule donne lieu à de nombreuses spécialités (princeps et génériques).
Exemple : GLUCOPHAGE 850 mg, comprimé pelliculé.
- La présentation : le conditionnement physique vendu en pharmacie (la boîte). Identifiée par un Code CIP13 à 13 chiffres — le code-barres scanné au comptoir. Une même spécialité peut avoir plusieurs présentations (boîte de 30, boîte de 90, flacon, etc.).

En synthèse : 1 molécule → N spécialités → N présentations.

L’AMM (Autorisation de Mise sur le Marché)
Autorisation réglementaire obligatoire pour commercialiser un médicament en France. Délivrée après évaluation du rapport bénéfice/risque par l’ANSM (procédure nationale) ou l’EMA (procédure européenne). Une AMM peut être active, suspendue ou retirée.

Le titulaire
Le laboratoire pharmaceutique qui détient l’AMM. C’est l’entité commerciale et réglementaire responsable du médicament : Sanofi, Pfizer, Servier, Viatris, etc.

La classification ATC
Le système ATC (Anatomical Therapeutic Chemical) est la classification internationale des médicaments, structurée en 5 niveaux hiérarchiques :
- Niveau 1 : système anatomique (A = appareil digestif, C = cardiovasculaire, N = système nerveux)
- Niveau 5 : substance chimique (A10BA02 = metformine)
C’est le langage standard de l’analyse pharma pour segmenter les marchés par aire thérapeutique.

Market Access
Ensemble des activités visant à obtenir et maintenir l’accès au marché d’un médicament : dépôt du dossier réglementaire, évaluation par la HAS (Haute Autorité de santé) , négociation du prix avec le CEPS(Comité économique des produits de santé), inscription au remboursement. En France, cette fonction est stratégique car les prix sont administrés (fixés par négociation avec l’État, non libres).

Ville vs. Hôpital
Le marché pharmaceutique français se divise en deux circuits distincts :
- Ville : médicaments prescrits par les médecins libéraux et dispensés en pharmacie d’officine.
- Hôpital : médicaments prescrits et administrés dans les établissements de santé.
Ces deux circuits ont des acteurs, des mécanismes de prix et des stratégies commerciales différents.

1. BDPM- Base de Données Publique des Médicaments
La BDPM est le référentiel officiel de l’ensemble des médicaments ayant obtenu une AMM (Autorisation de Mise sur le Marché) en France. Elle est maintenue par l’ANSM (Agence nationale de sécurité du médicament et des produits de santé) et constitue la source de référence pour identifier un médicament, connaître sa composition, son prix, son taux de remboursement, son évaluation par la HAS et ses conditions de prescription.

Join The Writer's Circle event
Lien données : URL
Format : Fichiers TXT, séparateur tabulation, pas d’en-tête
Modèle de données :

Press enter or click to view image in full size

Source : Documentation BDPM URL
Fichiers disponibles :
CIS_bdpm.txt: Liste des médicaments commercialisés ou en arrêt de commercialisation depuis moins de deux ans.
CIS_CIP_bdpm.txt: Décrit les conditionnements (boîtes) disponibles pour chaque spécialité. Porte les informations économiques : prix et remboursement.
CIS_COMPO_bdpm.txt: Contient la composition qualitative et quantitative en substances actives de chaque spécialité.
CIS_HAS_SMR_bdpm.txt: Avis de la Commission de la Transparence sur le Service Médical Rendu.
CIS_HAS_ASMR_bdpm.txt: Avis sur l’Amélioration du Service Médical Rendu (déterminant tarifaire).
HAS_LiensPageCT_bdpm.txt : Liens vers les avis complets de la Commission de la Transparence.
CIS_GENER_bdpm.txt : Répertoire des groupes génériques.
CIS_CPD_bdpm.txt : Conditions de prescription et de délivrance.
Exemples d’utilisation des données:
Pour donner des exemples d’utilisation, nous allons essayer de répondre à trois questions :

1. Comment se distribuent les prix et le remboursement ?
Press enter or click to view image in full size

Source: GitHub
Sur 20 894 présentations répertoriées dans la BDPM, 13 179 sont remboursées (63,1 %), les 36,9 % restantes étant non remboursées ou sans indication. Parmi les présentations remboursées, le taux 65 % domine très largement : il couvre 80,1 % du marché officinal remboursé, contre seulement 8,8 % pour le taux 100 % et 8,4 % pour le 30 %.

L’analyse des prix publics TTC révèle une corrélation forte entre taux de remboursement et niveau de prix : la médiane est de 161,24 € pour les médicaments à 100 %, contre 8,77 € à 65 %, 5,45 € à 30 % et 3,96 € à 15 %. Loin d’être contre-intuitive, cette relation est la conséquence directe de la politique française d’accès aux soins : le taux 100 % est réservé aux affections de longue durée (ALD) — pathologies chroniques lourdes comme le cancer, le diabète de type 1, ou les maladies cardiovasculaires sévères — dont les traitements sont structurellement plus coûteux.

2. Innovateurs ou génériqueurs : qui sont les grands laboratoires ?
Press enter or click to view image in full size

Source: GitHub
Sur l’ensemble du parc AMM (15 822 spécialités), 42,6 % sont des génériques, 8,6 % des princeps et 48,8 % des médicaments hors répertoire générique — souvent des produits sous protection de brevet ou des spécialités sans équivalent générique enregistré. Le répertoire des génériques permet de cartographier précisément le positionnement de chaque laboratoire. La fracture entre génériqueurs et innovateurs est nette : KRKA (96,8 % de génériques), Zydus France (96,4 %), Evolupharm (94,8 %), Cristers (90,5 %) et Biogaran (90,3 %) consacrent la quasi-totalité de leur portefeuille à la substitution. À l’opposé, Sanofi Winthrop Industrie, Boiron et Weleda n’ont aucun générique en portefeuille — leurs spécialités sont soit des princeps, soit des produits hors répertoire (homéopathie, produits de spécialité). Pfizer affiche 12,1 % de génériques, reflet d’acquisitions passées, mais garde 57,6 % de son portefeuille hors répertoire.

3. Quelques laboratoires dominent-ils le marché ?
Press enter or click to view image in full size

Source: GitHub
Le marché pharmaceutique français présente une concentration extrême, mesurée par un coefficient de Gini de 0,797 sur l’ensemble des 609 laboratoires titulaires de 13 568 spécialités commercialisées. Les 6 premiers laboratoires (1 % du total) détiennent à eux seuls 29,9 % des spécialités. Les 30 premiers (5 %) en contrôlent 60,1 %. À l’autre bout du spectre, la moitié des laboratoires se partagent à peine 4,1 % du parc. La longue traîne est massive : seuls 45 laboratoires ont plus de 50 références, et 22 dépassent 100 spécialités. Boiron (868 spécialités, 6,4 % du marché commercialisé) tient la première place — une anomalie structurelle due à l’enregistrement systématique de dilutions homéopathiques — devant Viatris Santé (762, 5,6 %), Biogaran (718, 5,3 %) et Arrow Génériques (651, 4,8 %).

Limites:
La BDPM est un référentiel produit. Elle répond à la question “qu’est-ce que ce médicament ?” mais ne dit rien sur son usage réel ni sur les acteurs qui le prescrivent ou le vendent. Quatre dimensions essentielles de l’analyse pharmaceutique lui échappent entièrement :

Les volumes de prescription. Ces données sont dans Open Medic, la base de l’Assurance Maladie — objet de la Partie 2.
La classification ATC. La BDPM ne contient pas le code ATC des médicaments. Segmenter le marché par aire thérapeutique (cardiovasculaire, neurologie, oncologie…) nécessite de passer par Open Medic.
Les prescripteurs. La BDPM connaît le titulaire de l’AMM, pas les médecins qui prescrivent. Identifier et cibler les prescripteurs nécessite le RPPS (Répertoire Partagé des Professionnels de Santé) — objet de la Partie 3.
Les établissements de santé. Pour analyser le marché hospitalier, il faut cartographier les hôpitaux, cliniques et centres spécialisés. C’est le rôle de FINESS — objet de la Partie 4.
Les liens financiers laboratoires-praticiens. La BDPM ne trace pas les relations entre industriels et professionnels de santé (contrats d’orateur, conventions de conseil, avantages). Ces données sont dans Transparence Santé — objet de la Partie 5.
Open Data
Pharmaceutical
Data Science
Medical
Database




Redouane
Written by Redouane
1 follower
·
2 following
Data Enthusiast

Edit profile
No responses yet

Redouane
Redouane
﻿

Cancel
Respond
More from Redouane
Redouane
Redouane

Tutoriel : Comment construire un Ego Graph en utilisant l’API Google Suggest
Comme l’explique David Foster dans son article, la construction d’un ego graphe peut s’avérer extrêmement utile pour élaborer une “carte”…
Jan 1, 2024
1


Tutoriel : Comment construire un Ego Graph en utilisant l’API Google Suggest
See all from Redouane
Recommended from Medium
From Lat/Lon to Hexagons and Neighbourhoods: Learning H3 with Madrid
Cristina Varas Menadas
Cristina Varas Menadas

From Lat/Lon to Hexagons and Neighbourhoods: Learning H3 with Madrid
How a bird-sighting anomaly project turned into a reusable H3 geospatial demo.

Nov 19, 2025
12


6 brain images
Write A Catalyst
In

Write A Catalyst

by

Dr. Patricia Schmidt

As a Neuroscientist, I Quit These 5 Morning Habits That Destroy Your Brain
Most people do #1 within 10 minutes of waking (and it sabotages your entire day)

Jan 14
33K
614


Apple App Store, Amazon Box, LinkedIn Logo, and TikTok logo all crushing a blog with sledgehammers
GitBit
In

GitBit

by

John Gruber

Websites Are Dead. Go Here Instead.
I finally did it. I launched a blog. Then I realized the hard truth.

Feb 10
5.5K
218


I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.
Level Up Coding
In

Level Up Coding

by

Teja Kusireddy

I Stopped Using ChatGPT for 30 Days. What Happened to My Brain Was Terrifying.
91% of you will abandon 2026 resolutions by January 10th. Here’s how to be in the 9% who actually win.

Dec 28, 2025
8.5K
321


Why the Smartest People in Tech Are Quietly Panicking Right Now
Activated Thinker
In

Activated Thinker

by

Shane Collins

Why the Smartest People in Tech Are Quietly Panicking Right Now
The water is rising fast, and your free version of ChatGPT is hiding the terrifying, exhilarating truth

Feb 13
11K
480


cover image
AI Advances
In

AI Advances

by

Jose Crespo, PhD

Anthropic is Killing Bitcoin
The AI-native currency already exists — hiding in plain sight, outperforming crypto by six orders of magnitude.

Feb 17
2.7K
120


See more recommendations
Help

Status

About

Careers

Press

Blog

Privacy

Rules

Terms

Text to speech