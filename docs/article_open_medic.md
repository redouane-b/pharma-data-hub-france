Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France. Partie 2 : Open Medic — Données de prescription de l'Assurance Maladie.

Open Medic est la base de données publique de l'Assurance Maladie qui recense l'ensemble des médicaments remboursés dispensés en pharmacie d'officine en France. Publiée annuellement par la CNAM (Caisse Nationale de l'Assurance Maladie) sur le portail Ameli, elle couvre la période 2014-2024 et constitue la principale source de données sur les volumes de prescription en ambulatoire. Là où la BDPM répond à la question « qu'est-ce que ce médicament ? », Open Medic répond à la question « ce médicament est-il prescrit, par qui, à qui et en quelle quantité ? »

La complémentarité avec la BDPM est structurelle. Open Medic apporte trois dimensions que la BDPM ignore entièrement : la classification ATC (indispensable pour segmenter le marché par aire thérapeutique), les volumes de prescription ventilés par spécialité médicale prescriptrice et par territoire, et le profil démographique des patients traités. C'est la base incontournable de toute analyse de marché pharmaceutique en ville.

2. Open Medic — Données de prescription de l'Assurance Maladie

Lien données : https://assurance-maladie.ameli.fr/etudes-et-donnees/open-data-medicaments-open-medic
Format : CSV, séparateur point-virgule, encodage Latin-1 (ISO-8859-1)
Grain : une ligne par combinaison (année × médicament (CIP13) × classe ATC × statut générique × spécialité prescripteur × région bénéficiaire × tranche d'âge × sexe)
Note : les colonnes PSP_DEP (département prescripteur) et EXE_DEP (département exécutant) présentes dans les millésimes antérieurs ont été remplacées par BEN_REG (région de résidence du bénéficiaire) dans le fichier 2024.
Volume : 50 à 200 Mo par année, ~6 à 8 millions de lignes par fichier annuel

Modèle de données :
Source : Documentation Open Medic — Ameli open data

Variables disponibles :
- CIP13 : code de présentation à 13 chiffres — clé de jointure vers la BDPM. Permet de retrouver le nom commercial, le laboratoire titulaire et les conditions de remboursement.
- L_ATC1_ à L_ATC5_ : libellés de la classification ATC aux niveaux 1 (système anatomique) à 5 (substance chimique). Absent de la BDPM, disponible uniquement ici. C'est ce champ qui permet de segmenter le marché par aire thérapeutique.
- PSP_SPE : code de spécialité du prescripteur. Les codes libéraux principaux sont : 1 = Médecine générale, 3 = Pathologie cardio-vasculaire, 5 = Dermatologie, 7 = Gynécologie-obstétrique, 12 = Pédiatrie, 17 = Psychiatrie, etc. Le code 90 regroupe les prescripteurs salariés (principalement hôpitaux publics).
- PSP_DEP / EXE_DEP : département du prescripteur et de la pharmacie exécutante — présents dans les millésimes antérieurs, absents du fichier 2024 qui utilise BEN_REG à la place.
- BEN_REG : région de résidence du bénéficiaire (codes pré-réforme 2016 : 11 = Île-de-France, 32 = Nord-Pas-de-Calais-Picardie, 44 = Alsace-Champagne-Ardenne-Lorraine, etc.).
- AGE : tranche d'âge du patient, en trois classes : 0 (0-19 ans), 20 (20-59 ans), 60 (60 ans et plus) ; 99 = inconnu.
- SEXE : sexe du patient (1 = Masculin, 2 = Féminin, 9 = Inconnu).
- TOP_GEN : statut générique (depuis 2022 — 0 = pas dans une famille de générique, 1 = générique, 4 = princep/original avec générique disponible, 9 = inconnu).
- GEN_NUM : numéro de groupe générique (permet de relier princep et génériques d'une même molécule).
- BOITES : nombre de boîtes dispensées et remboursées.
- NBC : nombre de bénéficiaires distincts (disponible uniquement dans les fichiers de type NB_, absent de la base complète).
- REM : montant total remboursé par l'Assurance Maladie (€).
- BSE : base de remboursement, c'est-à-dire le tarif de référence sur lequel s'applique le taux (peut différer du prix public pour les médicaments génériques).

Fichiers disponibles :
Open_MEDIC_Base_Complete_{année}.csv : base complète avec toutes les dimensions (2014 à 2024).
Les fichiers annuels sont disponibles en téléchargement direct via le portail Ameli open data. Chaque fichier pèse entre 50 Mo (années récentes avec moins d'antibiotiques) et 200 Mo.

Exemples d'utilisation des données :
Le notebook d'analyse associé à cet article explore sept questions concrètes à partir du fichier Open Medic 2024.

Q1 — La prescription est-elle concentrée sur quelques médicaments ?
Sur les 6 741 médicaments distincts (CIP13) présents dans le fichier 2024, seulement 68 codes (1 % du total) concentrent 55,4 % des boîtes dispensées. Les 10 % les plus prescrits (674 codes CIP13) représentent 85,2 % du volume total. Le coefficient de Gini de la distribution des prescriptions par médicament s'établit à 0,884 — une concentration encore plus marquée que celle du parc AMM (Gini de 0,797 calculé dans la Partie 1 sur les spécialités commercialisées). La prescription est un marché de blockbusters.

Sur l'ensemble du marché officinal remboursé, 2 368 millions de boîtes ont été dispensées en 2024 pour un montant total remboursé de 20,8 milliards d'euros selon les statistiques publiées par la CNAM (voir note en Q2 sur les limites de la colonne REM dans le fichier brut). La tête du classement est structurée par deux logiques distinctes : la médecine de premier recours (antalgiques, antibiotiques, anti-inflammatoires) génère des volumes massifs sur des médicaments dont le prix à la boîte est inférieur à 5 €, tandis que les traitements des pathologies chroniques (statines, antihypertenseurs, antidiabétiques) assurent un volume stable et prévisible tout au long de l'année. Le paracétamol — considéré toutes présentations cumulées — écrase le classement par volume, illustrant à lui seul le poids de l'automédication remboursée et des prescriptions post-consultation.

Q2 — Comment les dépenses de remboursement se répartissent-elles par classe thérapeutique ?
La classification ATC, absente de la BDPM, est directement disponible dans Open Medic jusqu'au niveau 5 (substance chimique). L'analyse par niveau 1 (système anatomique) révèle une dissociation fondamentale entre volumes de prescription et montants remboursés : les classes qui prescrivent le plus ne sont pas celles qui coûtent le plus.

En volume, les cinq premières classes sont N (Système nerveux, 36,6 % des boîtes), A (Appareil digestif et métabolisme, 17,6 %), C (Cardiovasculaire, 10,2 %), J (Anti-infectieux à usage systémique, 6,7 %) et R (Système respiratoire, 6,6 %). La domination de la classe N s'explique par le poids des antalgiques non-opioïdes (paracétamol, ibuprofène) et des psychotropes qui génèrent des volumes massifs.

En montant remboursé, dans les données effectivement renseignées du fichier officine 2024, la classe C (Cardiovasculaire) représente 10,2 % des boîtes mais concentre 23,4 % des remboursements — premier poste de dépense observable en ville. La classe N se maintient en deuxième position (21,3 % des remboursements) grâce à ses volumes massifs malgré un prix unitaire faible. Les Anti-infectieux (J) totalisent 10,5 %.

Le ratio coût par boîte révèle l'écart structurel entre les deux logiques de marché. La classe N affiche le coût unitaire le plus bas du classement (0,08 €/boîte) : ses 867 millions de boîtes sont majoritairement composées de médicaments bon marché à prescription courte. La classe C, à l'inverse, atteint 0,32 €/boîte — soit quatre fois plus — car ses traitements chroniques (statines, antihypertenseurs, anticoagulants oraux) sont pris quotidiennement et remboursés à des taux élevés. La classe J (Anti-infectieux) occupe une position intermédiaire à 0,22 €/boîte, reflet d'un marché où les antibiotiques génériques coexistent avec quelques antiviraux plus coûteux.

Un chiffre contre-intuitif retient l'attention : la classe L (Antinéoplasiques et immunomodulants) affiche le deuxième coût unitaire le plus bas (0,09 €/boîte), alors qu'elle concentre les médicaments les plus onéreux du marché — chimiothérapies orales, biothérapies, thérapies ciblées. Cette anomalie s'explique intégralement par la censure statistique : les 35 % de lignes sans REM renseigné touchent précisément les combinaisons analytiques à faible effectif, c'est-à-dire les médicaments rares et coûteux. Les 0,09 € observés ne représentent pas le coût réel de la classe L, mais le coût résiduel des quelques présentations peu onéreuses qui atteignent les seuils d'effectif suffisant pour échapper à la censure. La classe L est structurellement aveugle dans ce fichier.

Note sur la qualité de la donnée monétaire : la colonne REM est absente pour environ 35 % des lignes du fichier brut (censure statistique des effectifs insuffisants, conformément à la politique de protection de la vie privée de la CNAM). Les médicaments onéreux prescrits à peu de patients par combinaison analytique — oncologie, biothérapies, maladies rares — sont structurellement sous-représentés. La classe L (Antinéoplasiques), qui représente selon les statistiques CNAM officielles le premier poste de dépense ambulatoire réelle, n'apparaît qu'à 0,9 % des boîtes et 0,6 % des remboursements observés dans ce fichier. L'analyse volumétrique (BOITES) est fiable et complète ; l'analyse monétaire (REM) doit être interprétée comme un indicateur partiel du marché de ville bas-coût/haut-volume.

Cette limite structurelle est au cœur des enjeux de régulation pharmaceutique. Le levier de la substitution générique, très puissant sur les classes C et A, est quantifié en Q4.

Q3 — La prescription révèle-t-elle des inégalités démographiques ?
Open Medic ventile les prescriptions par tranche d'âge (trois classes : 0-19 ans, 20-59 ans, 60 ans et plus) et par sexe, permettant d'identifier les grandes tendances démographiques de la consommation médicamenteuse. Les résultats confirment une réalité structurelle : la prescription pharmaceutique est massivement concentrée sur les patients les plus âgés.

Les 60 ans et plus concentrent la majorité des boîtes dispensées, alors qu'ils représentent environ un quart de la population française. Cette surreprésentation est la conséquence directe de la polymédication des personnes âgées atteintes de pathologies chroniques multiples : une étude de la HAS estime qu'un tiers des plus de 75 ans prend quotidiennement 8 médicaments ou plus. À l'inverse, la tranche 0-19 ans représente une part modeste du volume total, avec une consommation concentrée sur les anti-infectieux (otites, angines, infections respiratoires pédiatriques) et les antalgiques.

La répartition par sexe révèle une légère surreprésentation féminine : les femmes représentent 54,3 % des boîtes dispensées contre 43,8 % pour les hommes (1,9 % non précisé). Cet écart est particulièrement marqué dans la tranche 20-59 ans — lié à la contraception, aux troubles thyroïdiens (la thyroïdite de Hashimoto touche 8 à 10 fois plus de femmes que d'hommes), et aux pathologies auto-immunes à prédominance féminine — avant de s'atténuer dans la tranche 60 ans et plus, où la prescription cardiovasculaire, légèrement plus masculine, prend le relais.

La carte thermique âge × classe ATC met en évidence des profils thérapeutiques contrastés entre tranches. La classe C (Cardiovasculaire) est quasi absente chez les 0-19 ans et atteint son pic chez les 60 ans et plus : c'est le marqueur de l'entrée dans la dépendance médicamenteuse chronique. La classe J (Anti-infectieux) présente le profil inverse, avec un pic marqué chez les 0-19 ans (infections pédiatriques) qui s'estompe avec l'âge. Seule la classe N (Système nerveux) maintient une présence significative sur toutes les tranches, reflet de l'universalité de la douleur comme motif de consultation.

Q4 — Quelle est la pénétration des génériques par classe thérapeutique ?
Le taux de substitution générique — part des boîtes dispensées en générique parmi les molécules qui disposent d'un équivalent générique — s'établit à 83,3 % en 2024 pour l'ensemble du marché officinal. Ce chiffre global masque des disparités importantes : les Anti-infectieux (J) atteignent 95,0 % de substitution, l'appareil musculo-squelettique (M) 94,1 %, le système respiratoire (R) 90,3 % et le cardiovasculaire (C) 89,4 %. À l'opposé, les antinéoplasiques (L, 50,6 %) et les médicaments du sang (B, 50,0 %) restent proches du seuil médian — reflet du poids des molécules récentes encore sous brevet.

La répartition par statut TOP_GEN éclaire la structure du marché : 44,8 % des boîtes dispensées sont des génériques, 9,0 % sont des princeps dans une famille génériquée (212 millions de boîtes théoriquement substituables), et 46,2 % ne disposent d'aucun générique. Cette dernière catégorie représente la limite structurelle du levier générique : près de la moitié du marché officinal reste hors périmètre de substitution, indépendamment des politiques tarifaires d'incitation.

Q5 — Qui prescrit quoi ? Profil de prescription par spécialité médicale
La médecine générale libérale génère 67,4 % des volumes de prescription en officine (1 596 millions de boîtes sur 2 368 au total). Les prescripteurs salariés — principalement les hôpitaux — contribuent pour 19,3 % du volume officinal avec un coût moyen de 0,16 €/boîte. L'ensemble des spécialités libérales hors médecine générale ne représente que 13,3 % du volume, mais concentre une part disproportionnée de la valeur grâce à un coût unitaire structurellement plus élevé.

La hiérarchie des spécialités libérales par coût moyen par boîte révèle la concentration de la dépense chez les prescripteurs de pathologies chroniques lourdes : radiologie (0,92 €/boîte), ORL (0,82 €/boîte), neurologie (0,83 €/boîte) et cardiologie (0,88 €/boîte) prescrivent des médicaments nettement plus chers que la médecine générale (0,04 €/boîte). La pédiatrie (0,26 €/boîte) et la gynécologie-obstétrique (0,33 €/boîte) se situent à un niveau intermédiaire.

Un groupe résiduel (PSP_SPE = 99, valeur inconnue) représente seulement 0,9 % des boîtes mais 18,7 % des remboursements observés, soit un coût moyen de 2,92 €/boîte — de loin le plus élevé du classement. Ce groupe correspond vraisemblablement aux prescriptions hospitalières de médicaments onéreux dispensés en officine (chimiothérapies orales, biothérapies) et aux praticiens dont la spécialité n'est pas renseignée. Il confirme la conclusion de Q2 : les dépenses pharmaceutiques les plus élevées sont concentrées dans des zones structurellement peu visibles du fichier ouvert officine.

Limites d'Open Medic et ce qui vient ensuite :
Open Medic est une base agrégée. C'est sa principale limite analytique : elle donne des volumes mais pas d'identifiants individuels. Il est impossible de reconstituer qui précisément prescrit quoi, ni de construire un historique de prescription pour un patient donné. Deux conséquences pratiques : on ne peut pas identifier les médecins les plus prescripteurs d'une classe thérapeutique, ni mesurer l'observance ou la persistance de traitement sur un individu.

Trois dimensions essentielles lui échappent entièrement :

Les prescripteurs individuels. Open Medic connaît la spécialité médicale et le département du prescripteur, mais pas son identité. Pour passer des volumes départementaux à une liste nominative de médecins à cibler, il faut croiser avec le RPPS (Répertoire Partagé des Professionnels de Santé), qui recense les noms, spécialités, modes d'exercice et adresses de tous les professionnels de santé actifs en France — objet de la Partie 3.

Le marché hospitalier. Open Medic couvre uniquement les dispensations en pharmacie de ville remboursées par l'Assurance Maladie. Les médicaments administrés en établissement de santé — chimiothérapies intraveineuses, biothérapies injectables, médicaments de la liste en sus — ne figurent pas dans cette base. La cartographie des établissements et l'accès aux données hospitalières passent par FINESS — objet de la Partie 4.

Les liens financiers laboratoires-praticiens. Open Medic ne trace pas les relations entre industriels et prescripteurs : conventions de conseil, contrats d'orateur, invitations à des congrès, avantages en nature. Ces informations sont rendues publiques dans la base Transparence Santé — objet de la Partie 5.
