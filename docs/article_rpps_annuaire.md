Pharma Open Data: Guide des sources publiques de données pharmaceutiques en France — RPPS Annuaire Santé (données individuelles).

Le RPPS (Répertoire Partagé des Professionnels de Santé) est la base nationale de référence de l'ensemble des professionnels intervenant dans le système de santé français. Maintenu par l'ANS (Agence du Numérique en Santé) et diffusé en open data sur data.gouv.fr et annuaire.sante.fr, il recense les médecins, pharmaciens, infirmiers, chirurgiens-dentistes, sages-femmes et tous les autres professionnels de santé actifs en France — avec leur spécialité, leur mode d'exercice et leur localisation géographique. Là où les tableaux DREES répondent à la question « combien y a-t-il de professionnels de santé, où et comment évolue leur nombre ? », le fichier individuel ANS répond à la question « qui sont ces prescripteurs nominativement, où sont-ils et quelle est leur spécialité ? »

Le RPPS est un référentiel **opposable** : les données enregistrées sont fiables car elles proviennent des autorités d'enregistrement (les ordres professionnels, le service de santé des armées, les agences régionales de santé, les employeurs). Chaque professionnel se voit attribuer un **numéro RPPS à 11 chiffres**, pérenne et non signifiant, qu'il conserve toute sa carrière. Ce numéro est la clé de jointure principale vers Transparence Santé et Open Medic.

RPPS Annuaire Santé — Extraction individuelle (ANS)
Lien données : https://www.data.gouv.fr/fr/datasets/annuaire-sante-extractions-des-donnees-en-libre-acces-des-professionnels-intervenant-dans-le-systeme-de-sante-rpps
Lien direct ANS : https://annuaire.sante.fr (onglet « EXTRACTIONS EN LIBRE ACCES »)
Producteur : Agence du Numérique en Santé (ANS) | Licence : Etalab | Mise à jour : hebdomadaire
Format : TXT, séparateur pipe (|), encodage UTF-8 — les champs ne sont pas protégés par des guillemets.
Grain : une ligne par activité — un professionnel peut avoir plusieurs lignes s'il exerce dans plusieurs structures ou avec plusieurs modes d'exercice.
Périmètre : tous les professionnels autorisés à exercer (y compris les étudiants autorisés à exercer en tant que remplaçant ou adjoint), toutes professions RPPS et anciennement ADELI.

Structure des fichiers (extraction PS_LibreAcces) :

| Fichier | Contenu | Volume approx. |
|---------|---------|---------------|
| `PS_LibreAcces_Personne_activite.txt` | Identité, exercice professionnel, structure d'exercice | ~760 Mo |
| `PS_LibreAcces_SavoirFaire.txt` | Savoir-faire et qualifications complémentaires | ~49 Mo |
| `PS_LibreAcces_Dipl_AutExerc.txt` | Diplômes et autorisations d'exercice | ~30 Mo |

Le fichier `PS_LibreAcces_Personne_activite.txt` est le fichier principal : il contient environ **1,1 million de lignes** (une par activité). Les deux autres fichiers se joignent sur le numéro RPPS pour enrichir les profils avec les spécialités (savoir-faire) et les diplômes.

Note : L'ancienne extraction monotable `ExtractionMonotable_CAT18_ToutePopulation` (périmètre RPPS seul, colonnes réduites) est progressivement abandonnée au profit de l'extraction `PS_LibreAcces`.

Données disponibles :

Identifiant PP (Numéro RPPS) : identifiant national à 11 chiffres — clé de jointure vers Transparence Santé (liens financiers laboratoires-praticiens) et vers les tableaux DREES. Chaque professionnel de santé inscrit possède un numéro RPPS unique et permanent, qui le suit tout au long de sa carrière.
Nom d'exercice / Prénom d'exercice : identité professionnelle (peut différer du nom civil pour les femmes mariées). C'est le nom sous lequel le professionnel apparaît dans les annuaires et les bases partenaires.
Civilité : Mme, M. — utile pour personnaliser les communications SFE.
Catégorie professionnelle : civil, agent public, étudiant autorisé à exercer comme remplaçant.
Code profession / Libellé profession : profession réglementée de santé — Médecin, Pharmacien, Infirmier, Chirurgien-dentiste, Sage-femme, Masseur-kinésithérapeute, Pédicure-podologue, etc.
Code savoir-faire / Libellé savoir-faire : spécialité ou qualification complémentaire reconnue — Médecine générale, Cardiologie, Chirurgie orthopédique et traumatologique, Endocrinologie-diabétologie et maladies métaboliques, Psychiatrie, etc. Un médecin peut avoir plusieurs savoir-faire enregistrés (fichier `PS_LibreAcces_SavoirFaire.txt`).
Code mode exercice / Libellé mode exercice : Libéral, Salarié ou Bénévole. La distinction est structurante pour l'analyse de marché : un médecin libéral génère directement des prescriptions remboursées par la CNAM (visibles dans Open Medic), un médecin salarié prescrit mais ses ordonnances sont souvent rattachées à la structure.
Identifiant structure / Coordonnées structure : identifiant FINESS de la structure d'exercice et adresse postale complète — clé de jointure vers le répertoire FINESS.
Code commune (coord. structure) : code INSEE à 5 caractères de la commune de la structure d'exercice — clé de jointure vers les données géographiques INSEE (COG). Permet de calculer des densités médicales par département ou région.
Diplômes / Autorisations d'exercice : diplômes obtenus en France ou à l'étranger, avec leur statut (fichier `PS_LibreAcces_Dipl_AutExerc.txt`).

Exemples d'utilisation des données :
Pour donner des exemples d'utilisation, nous allons essayer de répondre à trois questions concrètes à partir du fichier RPPS individuel.

1. Combien y a-t-il de professionnels de santé en France et comment se répartissent-ils par profession ?
La France compte environ 1,1 million de lignes dans le fichier principal (une par activité). Après déduplication sur le numéro RPPS, on obtient le nombre de professionnels distincts. La profession la plus représentée numériquement est celle d'infirmier, qui domine largement devant les médecins et les masseurs-kinésithérapeutes. Parmi les médecins — second groupe en volume — la répartition entre médecine générale et spécialités reflète les grands équilibres du système de soins français : la médecine générale constitue le socle du premier recours, tandis que la centaine de spécialités reconnues couvre l'ensemble des pathologies chroniques et aigues.

Press enter or click to view image in full size

Source : Git

2. Comment les médecins se répartissent-ils par spécialité ?
La médecine générale représente environ 45 à 50 % des médecins libéraux inscrits, confirmant son rôle de pivot du système ambulatoire. Parmi les spécialités, les plus représentées sont la psychiatrie, la cardiologie, la pédiatrie, la dermatologie et la gynécologie-obstétrique — soit exactement les spécialités dont les volumes de prescription sont les plus visibles dans Open Medic. Le fichier savoir-faire permet une cartographie fine : un même médecin peut cumuler plusieurs qualifications (ex. cardiologie + médecine vasculaire), créant une ambiguïté de comptage qu'il faut gérer par déduplication sur le numéro RPPS.

Press enter or click to view image in full size

Source : Git

3. Comment se répartit le territoire médical en France ?
La France présente des inégalités de densité médicale marquées entre départements. Les grandes métropoles (Paris, Lyon, Marseille, Bordeaux, Toulouse) concentrent les effectifs les plus élevés, à la fois parce que la population y est dense et parce que les structures hospitalières et universitaires y attirent les spécialistes. À l'opposé, les zones rurales et périurbaines de faible densité — les « déserts médicaux » — présentent des déficits structurels en médecins généralistes, avec des délais de rendez-vous et des taux de renoncement aux soins significativement plus élevés.

La donnée clé pour mesurer ce phénomène est le nombre de médecins généralistes libéraux par département, extrait directement du fichier individuel. Les deux premiers caractères du code commune donnent le département (75 = Paris, 2A = Corse-du-Sud). Pour des densités pour 100 000 habitants, croiser avec les données de population INSEE COG — objet de la Partie 5.

Press enter or click to view image in full size

Source : Git

BONUS. Correspondance RPPS / Open Medic : qui sont les PSP_SPE ?
Open Medic identifie les prescripteurs par un code numérique PSP_SPE (1 = Médecine générale libérale, 3 = Cardiologie, 12 = Pédiatrie, 90 = Salariés dont hôpitaux, etc.). Ce code ne permet pas à lui seul de retrouver les médecins concernés : il est agrégé et ne porte aucun identifiant individuel. Le fichier RPPS individuel ANS fournit la correspondance : en croisant le libellé savoir-faire avec le mapping PSP_SPE, on peut estimer le vivier total de prescripteurs potentiels pour chaque spécialité et construire une liste nominative avec adresse et mode d'exercice.

Limites :
Le fichier RPPS individuel est un registre administratif, non un registre d'activité. Trois limites importantes conditionnent son utilisation analytique.

La multiplicité des lignes par professionnel. Un médecin exerçant dans deux cabinets avec deux modes d'exercice différents génère plusieurs lignes dans `PS_LibreAcces_Personne_activite.txt`. Toute analyse quantitative (dénombrement, densité) nécessite une déduplication préalable sur le numéro RPPS, en choisissant une activité de référence par professionnel. Le fichier ne contient pas de notion d'activité principale — la DREES retient les 5 activités les plus récentes dans ses propres traitements.

L'absence de données d'activité prescriptrice. Le fichier RPPS sait qu'un médecin est inscrit et connaît sa spécialité, mais il ne sait pas s'il prescrit peu ou beaucoup, ni quelles classes thérapeutiques il favorise. Pour passer de l'annuaire à l'activité prescriptrice, le croisement avec Open Medic (volume par spécialité) ou avec Transparence Santé (avantages reçus par praticien) est indispensable.

Les médecins salariés et le code PSP_SPE = 90. Le code mode d'exercice distingue libéral et salarié, mais un médecin hospitalier peut occasionnellement rédiger des ordonnances remboursées. Le code PSP_SPE = 90 d'Open Medic regroupe ces cas de façon agrégée ; il est impossible de les désagréger au niveau individuel sans données complémentaires.

L'absence de l'âge dans les données open data. Les fichiers en libre accès ne contiennent pas l'âge des professionnels (disponible uniquement dans les données restreintes exploitées par la DREES). Pour des analyses démographiques (pyramide des âges, projection de départs à la retraite), utiliser les tableaux DREES (*La démographie des professionnels de santé depuis 2012*).

Ce qui vient ensuite :
Le RPPS individuel donne la liste nominative des prescripteurs ; les tableaux DREES donnent les statistiques agrégées sur leur démographie. FINESS donne la liste des établissements dans lesquels ils travaillent. Pour cartographier les hôpitaux, cliniques et centres spécialisés, et comprendre le marché hospitalier dans lequel prescriptions et achats de médicaments sont réalisés sans passer par la pharmacie d'officine, il faut FINESS — objet de la Partie 4.
