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
Get unlimited access to the best of Medium for less than $1/week.
Become a member

Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — Partie 2/5 : Open Medic.
Redouane
Redouane
5 min read
·
Just now




Open Medic est la base de données publique de l’Assurance Maladie qui recense l’ensemble des médicaments remboursés dispensés en pharmacie d’officine en France. Publiée annuellement par la CNAM (Caisse Nationale de l’Assurance Maladie) sur le portail Ameli, elle couvre la période 2014–2024 et constitue la principale source de données sur les volumes de prescription en ambulatoire.

2. Open Medic — Données de prescription de l’Assurance Maladie
Lien données : URL
Format : CSV, encodage Latin-1 (ISO-8859–1)
Données disponibles :

CIP13 : Code Identification Spécialité pharmaceutique à 13 chiffres — clé de jointure vers la BDPM. Permet de retrouver le nom commercial, le laboratoire titulaire et les conditions de remboursement.
L_ATC1_ à L_ATC5_ : libellés de la classification ATC aux niveaux 1 (système anatomique) à 5 (substance chimique). C’est ce champ qui permet de segmenter le marché par aire thérapeutique.
PSP_SPE : code de spécialité du prescripteur. Les codes libéraux principaux sont : 1 = Médecine générale, 3 = Pathologie cardio-vasculaire, 5 = Dermatologie, 7 = Gynécologie-obstétrique, 12 = Pédiatrie, 17 = Psychiatrie, etc. Le code 90 regroupe les prescripteurs salariés (principalement hôpitaux publics).
BEN_REG : région de résidence du bénéficiaire (codes pré-réforme 2016 : 11 = Île-de-France, 32 = Nord-Pas-de-Calais-Picardie, 44 = Alsace-Champagne-Ardenne-Lorraine, etc.).
AGE: tranche d’âge du patient (0 = 0–19 ans, 20 = 20–59, 60 = 60 ans et +, 99 = Age Inconnu).
SEXE: sexe du patient (1 = Homme, 2 = Femme, 9 = Non précisé).
TOP_GEN : statut générique (depuis 2022: 0 = pas dans une famille de générique, 1 = générique, 4 = princep/original avec générique disponible, 9 = inconnu).
GEN_NUM : numéro de groupe générique (permet de relier princep et génériques d’une même molécule).
BOITES: nombre de boîtes délivrées.
NBC: Nombre de consommants (disponible uniquement dans les bases type NB_)
REM : montant total remboursé par l’Assurance Maladie (€).
BSE : base de remboursement, c’est-à-dire le tarif de référence sur lequel s’applique le taux (peut différer du prix public pour les médicaments génériques).
Exemples d’utilisation des données :
Pour donner des exemples d’utilisation, nous allons essayer de répondre à trois questions concrètes à partir du fichier Open Medic 2024.

1. La prescription est-elle concentrée sur quelques médicaments ?
Sur les 12 646 médicaments distincts (CIP13) présents dans le fichier 2024, 2368 millions de boîtes ont été dispensés. Seulement 126 codes (1 % du total) concentrent 39.8 % des boîtes dispensées. Les 10 % les plus prescrits représentent 79.4 % du volume total. Le coefficient de Gini de la distribution des prescriptions par médicament s’établit à 0.869.

Press enter or click to view image in full size

Source : Git
En utilisant CIP13 comme clé de jointure vers la BDPM, nous pouvons retrouver le nom de la présentation:

Press enter or click to view image in full size

Source : Git
2. Comment les dépenses de remboursement se répartissent-elles par classe thérapeutique ?
La classification ATC permet de segmenter le marché par système anatomique et aire thérapeutique. L’analyse met en évidence une dissociation fondamentale entre volumes (les classes qui prescrivent le plus) et coûts (les classes qui consomment le plus de budget Assurance Maladie).

Press enter or click to view image in full size

Source : Git
En volume, les trois premières classes sont “Système nerveux” avec 36,6 % des boîtes, “Appareil digestif et métabolisme” avec 17,6 % et “Cardiovasculaire” avec 10,2 %. La domination de la première s’explique par le poids des antalgiques non-opioïdes (paracétamol, ibuprofène) et des psychotropes qui génèrent des volumes massifs.

Become a Medium member
En montant remboursé, dans les données effectivement renseignées du fichier officine 2024, la classe C (Cardiovasculaire) représente 10,2 % des boîtes mais concentre 23,4 % des remboursements — premier poste de dépense observable en ville. La classe N se maintient en deuxième position (21,3 % des remboursements) grâce à ses volumes massifs malgré un prix unitaire faible. Les Anti-infectieux (J) totalisent 10,5 %.

3. Quelle est la pénétration des génériques par classe thérapeutique ?
Press enter or click to view image in full size

Source : Git
Le taux de substitution générique — part des boîtes dispensées en générique parmi les molécules qui disposent d’un équivalent générique — s’établit à 83,3 % en 2024 pour l’ensemble du marché officinal. Ce chiffre global masque des disparités importantes : les Anti-infectieux (J) atteignent 95,0 % de substitution, l’appareil musculo-squelettique (M) 94,1 %, le système respiratoire (R) 90,3 % et le cardiovasculaire 89,4 %. À l’opposé, les antinéoplasiques (L, 50,6 %) et les médicaments du sang (B, 50,0 %) restent proches du seuil médian, un reflet du poids des molécules récentes encore sous brevet.

La répartition par statut TOP_GEN éclaire la structure du marché : 44,8 % des boîtes dispensées sont des génériques, 9,0 % sont des princeps dans une famille génériquée (212 millions de boîtes théoriquement substituables), et 46,2 % ne disposent d’aucun générique. Cette dernière catégorie représente la limite structurelle du levier générique : près de la moitié du marché officinal reste hors périmètre de substitution, indépendamment des politiques tarifaires d’incitation.

BONUS. Profil de prescription par spécialité médicale. Qui prescrit quoi ?
Press enter or click to view image in full size

Source : Git
Limites:
Open Medic est une base agrégée. C’est sa principale limite analytique : elle donne des volumes mais pas d’identifiants individuels. Il est impossible de reconstituer qui précisément prescrit quoi, ni de construire un historique de prescription pour un patient donné. Deux conséquences pratiques : on ne peut pas identifier les médecins les plus prescripteurs d’une classe thérapeutique, ni mesurer l’observance ou la persistance de traitement sur un individu.

Les prescripteurs individuels. Open Medic connaît la spécialité médicale et le département du prescripteur, mais pas son identité. Pour passer des volumes départementaux à une liste nominative de médecins à cibler, il faut croiser avec le RPPS (Répertoire Partagé des Professionnels de Santé), qui recense les noms, spécialités, modes d’exercice et adresses de tous les professionnels de santé actifs en France — objet de la Partie 3.

Le marché hospitalier. Open Medic couvre uniquement les dispensations en pharmacie de ville remboursées par l’Assurance Maladie. Les médicaments administrés en établissement de santé — chimiothérapies intraveineuses, biothérapies injectables, médicaments de la liste en sus — ne figurent pas dans cette base. La cartographie des établissements et l’accès aux données hospitalières passent par FINESS — objet de la Partie 4.

Les liens financiers laboratoires-praticiens. Open Medic ne trace pas les relations entre industriels et prescripteurs : conventions de conseil, contrats d’orateur, invitations à des congrès, avantages en nature. Ces informations sont rendues publiques dans la base Transparence Santé — objet de la Partie 5.

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
Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — Partie 1/5 …
Redouane
Redouane

Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — Partie 1/5 …
La France dispose d’un écosystème de données ouvertes particulièrement riche dans le domaine de la santé. Plusieurs bases publiques…
6d ago


Tutoriel : Comment construire un Ego Graph en utilisant l’API Google Suggest
Redouane
Redouane

Tutoriel : Comment construire un Ego Graph en utilisant l’API Google Suggest
Comme l’explique David Foster dans son article, la construction d’un ego graphe peut s’avérer extrêmement utile pour élaborer une “carte”…
Jan 1, 2024
1


See all from Redouane
Recommended from Medium
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


OpenAI Is Totally Cooked
Will Lockett
Will Lockett

OpenAI Is Totally Cooked
What a s**tshow.

5d ago
2.2K
33


Andrej Karpathy Just Built an Entire GPT in 243 Lines of Python
Towards Deep Learning
In

Towards Deep Learning

by

Sumit Pandey

Andrej Karpathy Just Built an Entire GPT in 243 Lines of Python
No PyTorch. No TensorFlow. Just pure Python and basic math.

Feb 15
2.6K
36


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