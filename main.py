import datetime, os, math
from dateutil.relativedelta import relativedelta
from pathlib import Path

### I - Fonction de calcul des situations individuelles ###

def calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 1, enregistrer = 0, filename = "no_filename"):
    
    # initialisation du fichier
    if enregistrer:
        if not os.path.exists(filename + '.csv'):
            Path(filename + '.csv').touch()
            with open(filename + '.csv',"w") as f:
                f.write("date_naissance;date_debut_travail;AV_cas_carriere_longue;AV_date_depart_selon_AP_age_legal;AV_date_depart_selon_nb_trim;AV_ce_qui_determine_vrai_age_depart;AV_age_reel_depart;AV_duree_reelle_cotis;AV_duree_reelle_travail;AP_cas_carriere_longue;AP_date_depart_selon_AP_age_legal;AP_date_depart_selon_nb_trim;AP_ce_qui_determine_vrai_age_depart;AP_age_reel_depart;AP_duree_reelle_cotis;AP_duree_reelle_travail")


    date_naissance = datetime.datetime.strptime(date_naissance, '%d/%m/%Y')
    date_debut_travail = datetime.datetime.strptime(date_debut_travail, '%d/%m/%Y')
    

    #### AVANT REFORME ####
     
    
    # 1 - Détermination du nombre de mois de travail à faire avant 31/12 de l'année du Xème anniversaire, en fonction du trimestre de naissance
    if date_naissance.month in range(1,10):
        # quelqu'un né de janvier à septembre inclus doit cotiser 5 trimestres avant le 31/12 de ses 16 (ou 20 ans) pour être éligible carrière longue
        # ce qui signifie 4 trimestres dans l'année de ses 16 ans (ou 20 ans) et 1 trimestre dans l'année de ses 15 ans (ou 19 ans)
        # ce qui signifie travailler toute l'année de ses 16 ans (ou 20 ans) et au moins un mois dans l'année de ses 15 ans (ou 19 ans)
        # ce qui signifie 13 mois de travail
        AV_nb_mois_avant_avant_borne = 13
    elif date_naissance.month in range(10,13):
        # quelqu'un né d'octobre à décembre inclus doit cotiser 4 trimestres avant le 31/12 de ses 16 (ou 20 ans) pour être éligible carrière longue
        # ce qui signifie 4 trimestres dans l'année de ses 16 ans (ou 20 ans)
        # ce qui signifie 4 mois de travail
        AV_nb_mois_avant_avant_borne = 4
    else:
        raise Exception("Il y a un souci sur le mois de naissance...")
    
    # 2 - Calcul de l'éligibilité à un des dispositifs carrière longue
    AV_CL = "non"
    # on regarde si la date de début de travail permet d'être éligible au dispositif carrière longue 20 ans, compte tenu de la date de naissance
    # que la réponse soit oui ou non, on teste ensuite la même chose pour le dispositif carrière longue 16 ans, et si c'est oui, on corrige
    for AV_borne in [20,16]: # on teste chacune des bornes, en descendant, de manière à ne retenir que la dernière qui est valide
        AV_date_31_12_X_ans = datetime.datetime(date_naissance.year + AV_borne, 12, 31)
        
        # Si la date de début de travail est au moins 4 ou 13 mois avant le 31 décembre du Xème anniversaire, alors AV_CL = X ans
        if date_debut_travail < AV_date_31_12_X_ans - relativedelta(months = AV_nb_mois_avant_avant_borne):
            AV_CL = str(AV_borne)
    
    # 3 - Ici, on entre les âges légaux de départ, et les durées de cotisation requises, pour les générations transitoires
    # Source : dossier de presse https://www.gouvernement.fr/upload/media/content/0001/05/1548a2feb27d6e5ed4d637eb051bb95daeb2200f.pdf
    # Tableau page 18, colonnes 3    

    # 4 - Ensuite, on rectifie l'âge légal de départ à la retraite pour les cas carrière longue
    # Source : https://www.service-public.fr/particuliers/vosdroits/F13845
    AV_age_legal = 62
    AV_total_trim_a_cotiser = 172
    
    # 4.1 - On rectifie pour les cas transitoires
    if date_naissance.year <= 1960:         
        AV_total_trim_a_cotiser = 167
        if AV_CL == "16":                         # de là            # TODO
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 180
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 172
        else:
            AV_age_legal = 62
            AV_total_trim_a_cotiser = 172         # à là, c'est probablement faux, mais le code n'est pas fait pour bien gérer les cas avant 1960
    elif date_naissance.year == 1961 or date_naissance.year == 1962 or date_naissance.year == 1963:       
        AV_total_trim_a_cotiser = 168
        if AV_CL == "16":
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 176
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 168
    elif date_naissance.year == 1964 or date_naissance.year == 1965 or date_naissance.year == 1966:       
        AV_total_trim_a_cotiser = 169
        if AV_CL == "16":
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 177
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 169
    elif date_naissance.year == 1967 or date_naissance.year == 1968 or date_naissance.year == 1969:
        AV_total_trim_a_cotiser = 170
        if AV_CL == "16":
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 178
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 170
    elif date_naissance.year == 1970 or date_naissance.year == 1971 or date_naissance.year == 1972:
        AV_total_trim_a_cotiser = 171
        if AV_CL == "16":
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 179
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 171
    elif date_naissance.year >= 1973:       
        if AV_CL == "16":
            AV_age_legal = 58
            AV_total_trim_a_cotiser = 180
        elif AV_CL == "20":
            AV_age_legal = 60
            AV_total_trim_a_cotiser = 172
    
    
    # 5 - Calcul date légale de départ
    # Pour quelqu'un né entre le 2 et le 31 du mois, il peut partir le 1er du mois qui suit sont Xème anniversaire, où X = son âge légal de départ en retraite
    # Pour quelqu'un né le 1er du mois, il peut partir dès ce jour là
    if date_naissance.day == 1:
        AV_date_legale = date_naissance + relativedelta(years=AV_age_legal)
    else:
        AV_date_legale = (date_naissance.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) + relativedelta(years=AV_age_legal)
    
    # 6 - Calcul date de départ avec nombre de trimestres de cotisation
    AV_nb_trimestres_cotises = 0
    AV_annees_civiles_pleinement_cotisees = 0
    
    # 6.1 - Nb trimestres cotisés première année
    # La première année, entre 0 et 4 trimestres peuvent être cotisés, selon la date de début de travail :
        # Si tout décembre est travaillé : 1 trimestre cotisé
        # Si tout novembre est également travaillé : 2 trimestres cotisés
        # Si tout octobre est également travaillé : 3 trimestres cotisés
        # Si tout septembre est également travaillé : 4 trimestres cotisés
        # Au delà : 4 trimestres cotisés, car c'est le maximum chaque année
        # (NB il est fait l'hypothèse simplificatrice que 150 heures au SMIC = un mois plein de travail)
        # (En effet, 150h au SMIC, à 35h par semaine et 5 jours ouvrés par semaine, ça fait 21,4 jours de travail, soit à peu près le nombre de jours ouvrés dans un mois)
    if date_debut_travail <= datetime.datetime(date_debut_travail.year, 9, 1):
        AV_nb_trimestres_cotises = 4
        AV_annees_civiles_pleinement_cotisees += 1
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 10, 1):
        AV_nb_trimestres_cotises = 3
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 11, 1):
        AV_nb_trimestres_cotises = 2
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 12, 1):    
        AV_nb_trimestres_cotises = 1
    
    # 6.2 - Nb trimestres cotisés carrière
    # Pour chaque année pleinement cotisée, on rajoute 4 trimestres, tout en veillant à ne jamais dépasser le nombre total de trimestres que doit cotiser la personne
    for i in range(50):
        if AV_nb_trimestres_cotises <= (AV_total_trim_a_cotiser-4):
            AV_nb_trimestres_cotises += 4
            AV_annees_civiles_pleinement_cotisees += 1
    
    # 6.3 - Nb trimestres cotisés dernière année
    if AV_nb_trimestres_cotises >= AV_total_trim_a_cotiser:
        # si le nb de trimestres cotisés est pile 172 (pour le cas général), c'est que 4 trimestres ont été cotisés la première année, toutes les années suivantes aussi
        # et 4 la dernière année. Notre cas aura tous ses trimestres le 31 décembre de sa dernière année de travail et pourra partir le 1er janvier suivant
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 0, 1, 1) # c'est +1 parce que annees_civ_pleinement_cotisees = 43
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-1:
        # si c'est 171, il lui manque un trimestre, il pourra partir au 1er avril
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 1, 4, 1) # c'est +2 parce que annees_civ_pleinement_cotisees = 42
        AV_nb_trimestres_cotises +=1
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-2:
        # si c'est 170, il lui manque deux trimestres, il pourra partir au 1er juillet
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 1, 7, 1)
        AV_nb_trimestres_cotises += 2
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-3:
        # si c'est 169, il lui manque trois trimestres, il pourra partir au 1er octobre
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 1, 10, 1)
        AV_nb_trimestres_cotises += 3
    
    del AV_annees_civiles_pleinement_cotisees
    
    # 7 - Calcul de l'âge réel de départ = max entre date légale et date depart avec nb trim
    if AV_CL == "non":
        AV_date_depart_reelle = AV_date_legale
    else:
        AV_date_depart_reelle = max(AV_date_depart_avec_nb_trim, AV_date_legale)
    AV_age_reel = relativedelta(AV_date_depart_reelle, date_naissance)
    
    # 8 - Vu l'âge réel de départ, calcul de la durée réellement cotisée
    AV_nb_trim_reellement_cotises = 0
    # nb trimestres cotisés première année
    if date_debut_travail <= datetime.datetime(date_debut_travail.year, 9, 1):
        AV_nb_trim_reellement_cotises = 4
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 10, 1):
        AV_nb_trim_reellement_cotises = 3
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 11, 1):
        AV_nb_trim_reellement_cotises = 2
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 12, 1):    
        AV_nb_trim_reellement_cotises = 1
    # nb trimestres cotisés années civiles pleines
    # nb années du 01/01/(date_debut_travail.year + 1) et 31/12/(AV_date_depart_reelle.year - 1) compris (donc 1/1/AV_date_depart_reelle.year)
    AV_nb_trim_reellement_cotises += relativedelta(datetime.datetime(AV_date_depart_reelle.year,1,1), datetime.datetime(date_debut_travail.year+1,1,1)).years*4
    # nb trimestres cotisés dernière année
    # si date depart réelle après 1er avril, +1 trimestre, après 1 juillet, +2 trimestres, après 1er octobre, +3 trimestres
    if AV_date_depart_reelle >= datetime.datetime(AV_date_depart_reelle.year, 10, 1):
        AV_nb_trim_reellement_cotises += 3
    elif AV_date_depart_reelle >= datetime.datetime(AV_date_depart_reelle.year, 7, 1):
        AV_nb_trim_reellement_cotises += 2           
    elif AV_date_depart_reelle >= datetime.datetime(AV_date_depart_reelle.year, 4, 1):
        AV_nb_trim_reellement_cotises += 1
    
    # 9 - Calcul de la durée réellement travaillée
    AV_duree_reelle_travail = relativedelta(AV_date_depart_reelle, date_debut_travail)
    AV_duree_reelle_travail_days = (AV_date_depart_reelle - date_debut_travail).days





    #### APRES REFORME ####
    
    
    # 1 - Détermination du nombre de mois de travail à faire avant 31/12 de l'année du Xème anniversaire, en fonction du trimestre de naissance
    # Pas modifié par la réforme
    if date_naissance.month in range(1,10):
        # quelqu'un né de janvier à septembre inclus doit cotiser 5 trimestres avant le 31/12 de ses 16 (ou 20 ans) pour être éligible carrière longue
        # ce qui signifie 4 trimestres dans l'année de ses 16 ans (ou 20 ans) et 1 trimestre dans l'année de ses 15 ans (ou 19 ans)
        # ce qui signifie travailler toute l'année de ses 16 ans (ou 20 ans) et au moins un mois dans l'année de ses 15 ans (ou 19 ans)
        # ce qui signifie 13 mois de travail
        AP_nb_mois_avant_avant_borne = 13
    elif date_naissance.month in range(10,13):
        # quelqu'un né d'octobre à décembre inclus doit cotiser 4 trimestres avant le 31/12 de ses 16 (ou 20 ans) pour être éligible carrière longue
        # ce qui signifie 4 trimestres dans l'année de ses 16 ans (ou 20 ans)
        # ce qui signifie 4 mois de travail
        AP_nb_mois_avant_avant_borne = 4
    else:
        raise Exception("Il y a un souci sur le mois de naissance...")
    
    # 2 - Calcul de l'éligibilité à un des dispositifs carrière longue
    # Modifié par la réforme
    AP_CL = "non"
    # on regarde si la date de début de travail permet d'être éligible au dispositif carrière longue 20 ans, compte tenu de la date de naissance
    # que la réponse soit oui ou non, on teste ensuite la même chose pour le dispositif carrière longue 20 ans, et si c'est oui, on corrige
    # puis on teste 18 ans, puis 16 ans
    for AP_borne in [21,20,18,16]: # on teste chacune des bornes, en descendant, de manière à ne retenir que la dernière qui est valide
        AP_date_31_12_X_ans = datetime.datetime(date_naissance.year + AP_borne, 12, 31)   

        # Si la date de début de travail est au moins 4 ou 13 mois avant le 31 décembre du Xème anniversaire, alors AP_CL = X ans
        if date_debut_travail < AP_date_31_12_X_ans - relativedelta(months = AP_nb_mois_avant_avant_borne):
            AP_CL = str(AP_borne)
    
    # 3 - Ici, on entre les âges légaux de départ, et les durées de cotisation requises, pour les générations transitoires
    # Modifié par la réforme
    # Source : dossier de presse https://www.gouvernement.fr/upload/media/content/0001/05/1548a2feb27d6e5ed4d637eb051bb95daeb2200f.pdf
    # Tableau page 18, colonnes 2 et 4
    
    AP_total_trim_a_cotiser = 172
    
    if date_naissance.year <= 1960:
        AP_age_legal = 62
        AP_total_trim_a_cotiser = 167
    elif date_naissance < datetime.datetime(1961, 9, 1):  # jusqu'à aout 1961
        AP_age_legal = 62
        AP_total_trim_a_cotiser = 168
    elif date_naissance.year == 1961: 
        AP_age_legal = 62.25
        AP_total_trim_a_cotiser = 169            
    elif date_naissance.year == 1962:
        AP_age_legal = 62.5
        AP_total_trim_a_cotiser = 169
    elif date_naissance.year == 1963:
        AP_age_legal = 62.75
        AP_total_trim_a_cotiser = 170
    elif date_naissance.year == 1964:
        AP_age_legal = 63
        AP_total_trim_a_cotiser = 171
    elif date_naissance.year == 1965:
        AP_age_legal = 63.25
        AP_total_trim_a_cotiser = 172
    elif date_naissance.year == 1966:
        AP_age_legal = 63.5
        AP_total_trim_a_cotiser = 172
    elif date_naissance.year == 1967:
        AP_age_legal = 63.75
        AP_total_trim_a_cotiser = 172
    elif date_naissance.year >= 1968:
        AP_age_legal = 64
        AP_total_trim_a_cotiser = 172
    
    # 4 - Ensuite, on rectifie l'âge légal de départ à la retraite pour les cas carrière longue
    # Modifié par la réforme
    # TODO : chercher si je trouve la réponse aux trois lignes de commentaires suivantes :
    # Par ailleurs, je fais l'hypothèse, peut être fausse, que l'accélération de Touraine est appliquée de la même manière aux cas CL18, 20 et 21
    # Pour les cas CL 16, pour lesquels la durée de cotisation en droit actuel est comprise en 176 et 180 T (https://www.service-public.fr/particuliers/vosdroits/F13845)
    # Je fais l'hypothèse qu'elle est immédiatement abaissée à 172 T
    if AP_CL == "16":
        AP_age_legal = 58
        AP_total_trim_a_cotiser = 172
    elif AP_CL == "18":
        AP_age_legal = 60
    elif AP_CL == "20":
        AP_age_legal = AP_age_legal - 2 
    elif AP_CL == "21":
        AP_age_legal = AP_age_legal - 1 # Pas complètement certain, mais fixer 63, plutôt que "âge légal - 1"  n'aurait pas de sens et créerait des effets de seuil sur les cas transitoires
    else:
        AP_age_legal = AP_age_legal
    
    # relativedelta() n'aime pas les float, donc il faut gérer ça et lui donner les mois
    AP_age_legal_month = 0
    if math.modf(AP_age_legal)[0] == 0:
        AP_age_legal_month = 0
    elif math.modf(AP_age_legal)[0] == 0.25:
        AP_age_legal_month = 3
    elif math.modf(AP_age_legal)[0] == 0.5:
        AP_age_legal_month = 6
    elif math.modf(AP_age_legal)[0] == 0.75:
        AP_age_legal_month = 9
    else:
        raise Exception("Y'a un souci dans AP_age_legal")
        
    # 5 - Calcul date légale de départ
    # Pas modifié par la réforme
    # Pour quelqu'un né entre le 2 et le 31 du mois, il peut partir le 1er du mois qui suit sont Xème anniversaire, où X = son âge légal de départ en retraite
    # Pour quelqu'un né le 1er du mois, il peut partir dès ce jour là
    if date_naissance.day == 1:
        AP_date_legale = date_naissance + relativedelta(years=math.floor(AP_age_legal), months=AP_age_legal_month)
    else:
        AP_date_legale = (date_naissance.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) + relativedelta(years=math.floor(AP_age_legal), months=AP_age_legal_month)
    
    # 6 - Calcul date de départ avec nombre de trimestres de cotisation
    AP_nb_trimestres_cotises = 0
    AP_annees_civiles_pleinement_cotisees = 0
    
    # 6.1 - Nb trimestres cotisés première année
    # Pas modifié par la réforme
    # La première année, entre 0 et 4 trimestres peuvent être cotisés, selon la date de début de travail :
        # Si tout décembre est travaillé : 1 trimestre cotisé
        # Si tout novembre est également travaillé : 2 trimestres cotisés
        # Si tout octobre est également travaillé : 3 trimestres cotisés
        # Si tout septembre est également travaillé : 4 trimestres cotisés
        # Au delà : 4 trimestres cotisés, car c'est le maximum chaque année
        # (NB il est fait l'hypothèse simplificatrice que 150 heures au SMIC = un mois plein de travail)
        # (En effet, 150h au SMIC, à 35h par semaine et 5 jours ouvrés par semaine, ça fait 21,4 jours de travail, soit à peu près le nombre de jours ouvrés dans un mois)
    if date_debut_travail <= datetime.datetime(date_debut_travail.year, 9, 1):
        AP_nb_trimestres_cotises = 4
        AP_annees_civiles_pleinement_cotisees += 1
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 10, 1):
        AP_nb_trimestres_cotises = 3
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 11, 1):
        AP_nb_trimestres_cotises = 2
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 12, 1):    
        AP_nb_trimestres_cotises = 1
        
    # 6.2 - Nb trimestres cotisés carrière
    # Pas modifié par la réforme
    # Pour chaque année pleinement cotisée, on rajoute 4 trimestres, tout en veillant à ne jamais dépasser le nombre total de trimestres que doit cotiser la personne
    for i in range(50):
        if AP_nb_trimestres_cotises <= (AP_total_trim_a_cotiser-4):
            AP_nb_trimestres_cotises += 4
            AP_annees_civiles_pleinement_cotisees += 1
    
    # 6.3 - Nb trimestres cotisés dernière année
    # Pas modifié par la réforme
    if AP_nb_trimestres_cotises >= AP_total_trim_a_cotiser:
        # si le nb de trimestres cotisés est pile 172 (pour le cas général), c'est que 4 trimestres ont été cotisés la première année, toutes les années suivantes aussi
        # et 4 la dernière année. Notre cas aura tous ses trimestres le 31 décembre de sa dernière année de travail et pourra partir le 1er janvier suivant
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 0, 1, 1) # c'est +1 parce que annees_civ_pleinement_cotisees = 43
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-1:
        # si c'est 171, il lui manque un trimestre, il pourra partir au 1er avril
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 1, 4, 1) # c'est +2 parce que annees_civ_pleinement_cotisees = 42
        AP_nb_trimestres_cotises +=1
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-2:
        # si c'est 170, il lui manque deux trimestres, il pourra partir au 1er juillet
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 1, 7, 1)
        AP_nb_trimestres_cotises += 2
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-3:
        # si c'est 169, il lui manque trois trimestres, il pourra partir au 1er octobre
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 1, 10, 1)
        AP_nb_trimestres_cotises += 3
    
    del AP_annees_civiles_pleinement_cotisees
    
    # 7 - Calcul de l'âge réel de départ = max entre date légale et date depart avec nb trim
    # Pas modifié par la réforme
    if AP_CL == "non":
        AP_date_depart_reelle = AP_date_legale
    else:
        AP_date_depart_reelle = max(AP_date_depart_avec_nb_trim, AP_date_legale)
    AP_age_reel = relativedelta(AP_date_depart_reelle, date_naissance)

    # 8 - Vu l'âge réel de départ, calcul de la durée réellement cotisée
    # Pas modifié par la réforme
    AP_nb_trim_reellement_cotises = 0
    # nb trimestres cotisés première année
    if date_debut_travail <= datetime.datetime(date_debut_travail.year, 9, 1):
        AP_nb_trim_reellement_cotises = 4
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 10, 1):
        AP_nb_trim_reellement_cotises = 3
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 11, 1):
        AP_nb_trim_reellement_cotises = 2
    elif date_debut_travail <= datetime.datetime(date_debut_travail.year, 12, 1):    
        AP_nb_trim_reellement_cotises = 1
    # nb trimestres cotisés années civiles pleines
    # nb années du 01/01/(date_debut_travail.year + 1) et 31/12/(AP_date_depart_reelle.year - 1) compris (donc 1/1/AP_date_depart_reelle.year)
    AP_nb_trim_reellement_cotises += relativedelta(datetime.datetime(AP_date_depart_reelle.year,1,1), datetime.datetime(date_debut_travail.year+1,1,1)).years*4   
    
    # nb trimestres cotisés dernière année
    # si date depart réelle après 1er avril, +1 trimestre, après 1 juillet, +2 trimestres, après 1er octobre, +3 trimestres
    if AP_date_depart_reelle >= datetime.datetime(AP_date_depart_reelle.year, 10, 1):
        AP_nb_trim_reellement_cotises += 3
    elif AP_date_depart_reelle >= datetime.datetime(AP_date_depart_reelle.year, 7, 1):
        AP_nb_trim_reellement_cotises += 2           
    elif AP_date_depart_reelle >= datetime.datetime(AP_date_depart_reelle.year, 4, 1):
        AP_nb_trim_reellement_cotises += 1
    
    # 9 - Calcul de la durée réellement travaillée
    # Pas modifié par la réforme
    AP_duree_reelle_travail = relativedelta(AP_date_depart_reelle, date_debut_travail)
    AP_duree_reelle_travail_days = (AP_date_depart_reelle - date_debut_travail).days
    
    
    
    # Résumé
    AV_vraie_cause_depart =""
    AP_vraie_cause_depart =""

    if AV_date_depart_reelle == AP_date_depart_reelle and AV_nb_trim_reellement_cotises == AP_nb_trim_reellement_cotises and AV_duree_reelle_travail_days == AP_duree_reelle_travail_days:
        situation_changee = "non"
        if verbose:
            print(" ")
            print("RIEN NE CHANGE")
        else:
            pass
    else:
        if AV_date_depart_reelle < AP_date_depart_reelle or AV_nb_trim_reellement_cotises < AP_nb_trim_reellement_cotises or AV_duree_reelle_travail_days < AP_duree_reelle_travail_days:
            # si la date de départ a reculé après réforme, ou le nombre de trimestres réellement cotisés
            # ou la durée réelle de travail, alors le cas est marqué comme "dégradé". Et sinon, on considère que la situation a été améliorée
            situation_changee = "dégradée"
        else:
            situation_changee = "améliorée"
        
       
    if AV_date_depart_reelle == AV_date_depart_avec_nb_trim:
        AV_vraie_cause_depart = "duree_cotisation"
    elif AV_date_depart_reelle == AV_date_legale:
        AV_vraie_cause_depart = "age_legal"

    if AP_date_depart_reelle == AP_date_depart_avec_nb_trim:
        AP_vraie_cause_depart = "duree_cotisation"
    elif AP_date_depart_reelle == AP_date_legale:
        AP_vraie_cause_depart = "age_legal"
        
        

    if verbose:
        print("\t\t\t\t\t\t\t\t\t\t\t\t yyyy-mm-dd")
        print("Né le \t\t\t\t\t\t\t\t\t\t\t", date_naissance.date())
        print("Début travail le \t\t\t\t\t\t\t\t", date_debut_travail.date())
        print("\t\t\t\t\t\t\t - AVANT réforme -")
        print("Cas carrière longue :", AV_CL)
        print("Date départ selon âge légal \t\t\t\t\t", AV_date_legale.date())
        print("Date départ selon nb trim \t\t\t\t\t\t", AV_date_depart_avec_nb_trim.date())
        
        if AV_vraie_cause_depart == "duree_cotisation":
            print("Date de départ déterminée par le nb de trim \t", AV_date_depart_reelle.date())
        elif AV_vraie_cause_depart == "age_legal":
            print("Date de départ déterminée par l'âge légal \t\t", AV_date_depart_reelle.date())
        print("Âge réel de départ =", AV_age_reel)
        print("Durée réelle de cotis =", AV_nb_trim_reellement_cotises/4)
        print("Durée reelle de travail =", AV_duree_reelle_travail)

        print("\t\t\t\t\t\t\t - APRES réforme -")
        print("Cas carrière longue :", AP_CL)
        print("Date départ selon âge légal \t\t\t\t\t", AP_date_legale.date())
        print("Date départ selon nb trim \t\t\t\t\t\t", AP_date_depart_avec_nb_trim.date())
        
        if AP_vraie_cause_depart == "duree_cotisation":
            print("Date de départ déterminée par le nb de trim \t", AP_date_depart_reelle.date())
        elif AP_vraie_cause_depart == "age_legal":
            print("Date de départ déterminée par l'âge légal \t\t", AP_date_depart_reelle.date())
        print("Âge réel de départ =", AP_age_reel)
        print("Durée réelle de cotis =", AP_nb_trim_reellement_cotises/4)
        print("Durée reelle de travail =", AP_duree_reelle_travail)
        print("Situation changée :", situation_changee)
        print(" ")

  
    # Enregistrement dans fichier
    
    if enregistrer:
        with open(filename + '.csv',"a") as f:
            f.write("\n"+\
                    str(date_naissance.date())+\
                    ";"+str(date_debut_travail.date())+\
                    ";"+str(AV_CL)+\
                    ";"+str(AV_date_legale.date())+\
                    ";"+str(AV_date_depart_avec_nb_trim.date())+\
                    ";"+str(AV_vraie_cause_depart)+\
                    ";"+str(AV_age_reel.years)+" an(s),"+ str(AV_age_reel.months) +" mois et "+ str(AV_age_reel.days) +" jour(s)"+\
                    ";"+str(AV_nb_trim_reellement_cotises)+\
                    ";"+str(AV_duree_reelle_travail.years)+" an(s),"+ str(AV_duree_reelle_travail.months) +" mois et "+ str(AV_duree_reelle_travail.days) +" jour(s)"
                    ";"+str(AP_CL)+\
                    ";"+str(AP_date_legale.date())+\
                    ";"+str(AP_date_depart_avec_nb_trim.date())+\
                    ";"+str(AP_vraie_cause_depart)+\
                    ";"+str(AP_age_reel.years)+" an(s),"+ str(AP_age_reel.months) +" mois et "+ str(AP_age_reel.days) +" jour(s)"+\
                    ";"+str(AP_nb_trim_reellement_cotises)+\
                    ";"+str(AP_duree_reelle_travail.years)+" an(s),"+ str(AP_duree_reelle_travail.months) +" mois et "+ str(AP_duree_reelle_travail.days) +" jour(s)"+\
                    ";"+str(situation_changee))
    
    # Gestion ouput
    
    output_dict = dict()
    output_dict["date_naissance"] = str(date_naissance.date())
    output_dict["date_debut_travail"] = str(date_debut_travail.date())
    
    output_dict["AV_CL"] = AV_CL
    output_dict["AV_date_legale"] = str(AV_date_legale.date())
    output_dict["AV_date_depart_avec_nb_trim"] = str(AV_date_depart_avec_nb_trim.date())
    output_dict["AV_vraie_cause_depart"] = AV_vraie_cause_depart
    output_dict["AV_age_reel"] = str(AV_age_reel.years)+" an(s), "+ str(AV_age_reel.months) +" mois et "+ str(AV_age_reel.days) +" jour(s)"
    output_dict["AV_age_reel.years"] = AV_age_reel.years
    output_dict["AV_age_reel.months"] = AV_age_reel.months
    output_dict["AV_age_reel.days"] = AV_age_reel.days
    output_dict["AV_nb_trim_reellement_cotises"] = AV_nb_trim_reellement_cotises
    output_dict["AV_duree_reelle_travail"] = str(AV_duree_reelle_travail.years)+" an(s), "+ str(AV_duree_reelle_travail.months) +" mois et "+ str(AV_duree_reelle_travail.days) +" jour(s)"
    output_dict["AV_duree_reelle_travail.years"] = AV_duree_reelle_travail.years
    output_dict["AV_duree_reelle_travail.months"] = AV_duree_reelle_travail.months
    output_dict["AV_duree_reelle_travail.days"] = AV_duree_reelle_travail.days
    
    output_dict["AP_CL"] = AP_CL
    output_dict["AP_date_legale"] = str(AP_date_legale.date())
    output_dict["AP_date_depart_avec_nb_trim"] = str(AP_date_depart_avec_nb_trim.date())
    output_dict["AP_vraie_cause_depart"] = AP_vraie_cause_depart
    output_dict["AP_age_reel"] = str(AP_age_reel.years)+" an(s), "+ str(AP_age_reel.months) +" mois et "+ str(AP_age_reel.days) +" jour(s)"
    output_dict["AP_age_reel.years"] = AP_age_reel.years
    output_dict["AP_age_reel.months"] = AP_age_reel.months
    output_dict["AP_age_reel.days"] = AP_age_reel.days
    output_dict["AP_nb_trim_reellement_cotises"] = AP_nb_trim_reellement_cotises
    output_dict["AP_duree_reelle_travail"] = str(AP_duree_reelle_travail.years)+" an(s), "+ str(AP_duree_reelle_travail.months) +" mois et "+ str(AP_duree_reelle_travail.days) +" jour(s)"
    output_dict["AP_duree_reelle_travail.years"] = AP_duree_reelle_travail.years
    output_dict["AP_duree_reelle_travail.months"] = AP_duree_reelle_travail.months
    output_dict["AP_duree_reelle_travail.days"] = AP_duree_reelle_travail.days
    
    output_dict["situation_changee"] = situation_changee

    return output_dict

#%% Simulations individuelles pour mes tests

# Dates au format "jj/mm/aaaa"
date_naissance = "2/09/2000"
date_debut_travail = "2/12/2015"
# calcul_situation_indiv(date_naissance, date_debut_travail)


date_naissance = "12/12/2000"
date_debut_travail = "13/7/2014"
# calcul_situation_indiv(date_naissance, date_debut_travail)

date_naissance = "02/01/2000"
date_debut_travail = "11/8/2021"
#calcul_situation_indiv(date_naissance, date_debut_travail)

date_naissance = "05/01/2000"
date_debut_travail = "31/12/2021"
# calcul_situation_indiv(date_naissance, date_debut_travail)


#%% 

### II - Simulations (générations non transitoires,  cas général (non carrières longues)) ###

# calculs pour : 
    # les situations générales (donc pas les années transitoires, autrement dit, tout le monde né après 1969
    # des gens non carrière longue (c'est à dire qui ont commencé, grosso modo, après 21 ans)

# initialisation des variables, ne pas prêter attention
total_cas = 0
nb_cas_changed = 0
nb_cas_degraded = 0
nb_cas_ameliored = 0
nb_cas_171_ou_moins = 0
nb_cas_172 = 0
nb_cas_173 = 0
nb_cas_174 = 0
nb_cas_175 = 0
nb_cas_176 = 0
nb_cas_177_ou_plus = 0
nb_cas_travail_43_ou_plus = 0
nb_cas_travail_44_ou_plus = 0
nb_cas_travail_45_ou_plus = 0

tous_les_cas = 1

for Nm in range(1,13):
    for Nd in range(1,32):
        date_naissance = str(Nd)+"/"+str(Nm)+"/2000"
        #print(date_naissance)
        
        for Ty in range(2022,2023):
            for Tm in range(1,13):
                for Td in range(1,32):
                    date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)

                    try:
                        result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0)
                        
                        total_cas += 1
                        if result["situation_changee"] != "non":
                            nb_cas_changed += 1
                        if result["situation_changee"] == "dégradée":
                            nb_cas_degraded +=1
                        if result["situation_changee"] == "améliorée":
                            nb_cas_ameliored +=1
                            
                        if result["situation_changee"] != "non" or tous_les_cas:
                            if result["AP_nb_trim_reellement_cotises"] <= 171 : nb_cas_171_ou_moins += 1
                            if result["AP_nb_trim_reellement_cotises"] == 172 : nb_cas_172 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 173 : nb_cas_173 += 1
                            if result["AP_nb_trim_reellement_cotises"] >= 173 : nb_cas_173 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 174 : nb_cas_174 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 175 : nb_cas_175 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 176 : nb_cas_176 += 1
                            if result["AP_nb_trim_reellement_cotises"] > 176 : 
                                nb_cas_177_ou_plus += 1
                                print("176+", date_naissance, date_debut_travail)

                            if result["AP_duree_reelle_travail.years"] >= 43 : 
                                nb_cas_travail_43_ou_plus += 1
                            if result["AP_duree_reelle_travail.years"] >= 44 : nb_cas_travail_44_ou_plus += 1
                            if result["AP_duree_reelle_travail.years"] >= 45 : 
                                nb_cas_travail_45_ou_plus += 1
                                print("45+", date_naissance, date_debut_travail)

                    except ValueError:
                        pass
                    except Exception as e:
                        print("autre erreur")
                        err = e

# résultats

total_cas # nombre de situations simulées : 365 * 366 = 133590
nb_cas_changed # nombre de situations modifiées par la réforme : 133590, soit 100%
nb_cas_degraded # nombre de situations dégradées par la réforme : 133590, soit 100%
nb_cas_ameliored # nombre de situations améliorées par la réforme : 0

# Résultats pour les situations modifiées par la réforme
nb_cas_171_ou_moins # 126270   # assez logiquement, l'essentiel des situations pourra partir avant 172 trimestres cotisés (puisque ce n'est pas une condition exigée quand on est pas carrière longue)
nb_cas_172 # 73
nb_cas_173 # 0
nb_cas_174 # 0
nb_cas_175 # 0
nb_cas_176 # 0
nb_cas_177_ou_plus # 0
nb_cas_travail_43_ou_plus # 30 : les gens nés entre le 2 décembre et le 31 décembre inclus, et qui ont commencé le 1er janvier 2022 : ils ne pourront partir qu'à compter du 1er janvier 2065 et auront donc travaillé pile 43 ans. Anecdotique.
nb_cas_travail_44_ou_plus # 0
nb_cas_travail_45_ou_plus # 0

# Résultats pour l'ensemble des situations, qu'elles soient modifiées par la réforme
# Même résultats qu'au dessus, ce qui est logique, vu que toutes les situations sont modifiées par la réforme

#%% 

### III - Simulations (générations non transitoires, carrières longues) ###

# calculs pour : 
    # les situations générales (donc pas les années transitoires, autrement dit, tout le monde né après 1969
    # des gens qui ont commencé, avant le 31 décembre de l'année de leur 21 ans (c'est à dire en situation de carrière longue pour la plupart)

# initialisation des variables, ne pas prêter attention
total_cas = 0
nb_cas_changed = 0
nb_cas_degraded = 0
nb_cas_ameliored = 0
nb_cas_171_ou_moins = 0
nb_cas_172 = 0
nb_cas_173 = 0
nb_cas_173_ou_plus = 0
nb_cas_174 = 0
nb_cas_175 = 0
nb_cas_176 = 0
nb_cas_177 = 0
nb_cas_178 = 0
nb_cas_179 = 0
nb_cas_180 = 0
nb_cas_181_ou_plus = 0
nb_cas_travail_43_plus = 0
nb_cas_travail_44_plus = 0
nb_cas_travail_45_plus = 0

nb_age_legal = 0
nb_cotisation = 0

tous_les_cas = 1

for Nm in range(1,13):
    for Nd in range(1,32):
        date_naissance = str(Nd)+"/"+str(Nm)+"/2000"
        #print(date_naissance)
        
        for Ty in range(2015,2022):
            for Tm in range(1,13):
                for Td in range(1,32):
                    date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)

                    try:
                        result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0)
                        
                        total_cas += 1
                        if result["situation_changee"] != "non":
                            nb_cas_changed += 1
                        if result["situation_changee"] == "dégradée":
                            nb_cas_degraded +=1
                        if result["situation_changee"] == "améliorée":
                            nb_cas_ameliored +=1
                            
                        if result["situation_changee"] != "non" or tous_les_cas:
                            if result["AP_nb_trim_reellement_cotises"] <= 171 : 
                                nb_cas_171_ou_moins += 1
                                # print("171-", date_naissance, date_debut_travail)
                            if result["AP_nb_trim_reellement_cotises"] == 172 : 
                                nb_cas_172 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 173 : nb_cas_173 += 1
                            if result["AP_nb_trim_reellement_cotises"] >= 173 : 
                                nb_cas_173_ou_plus += 1
                                if result["AP_vraie_cause_depart"] == 'duree_cotisation':
                                    nb_cotisation += 1
                                    print(date_naissance, date_debut_travail)
                                elif result["AP_vraie_cause_depart"] == 'age_legal':
                                    nb_age_legal += 1
                            if result["AP_nb_trim_reellement_cotises"] == 174 : nb_cas_174 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 175 : nb_cas_175 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 176 : nb_cas_176 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 177 : nb_cas_177 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 178 : nb_cas_178 += 1
                            if result["AP_nb_trim_reellement_cotises"] == 179 : 
                                nb_cas_179 += 1
                                
                            if result["AP_nb_trim_reellement_cotises"] == 180 : 
                                nb_cas_180 += 1

                            if result["AP_nb_trim_reellement_cotises"] > 180 : nb_cas_181_ou_plus += 1

                            if result["AP_duree_reelle_travail.years"] >= 43 : 
                                nb_cas_travail_43_plus += 1
                            if result["AP_duree_reelle_travail.years"] >= 44 : nb_cas_travail_44_plus += 1
                            if result["AP_duree_reelle_travail.years"] >= 45 : 
                                nb_cas_travail_45_plus += 1

                    except ValueError:
                        pass
                    except Exception as e:
                        print("autre erreur")
                        print(date_naissance, date_debut_travail)
                        err = e

# résultats

total_cas #  nombre de situations simulées : 935862 (dans l'idée, c'est 365 * 365 * 7, mais en vérité, c'est 366 * (6*365 + 2*366) parce que 2000, 2016 et 2020 sont bissextiles)
nb_cas_changed # nombre de situations modifiées par la réforme : 629673, soit 67,3 % 
nb_cas_degraded # nombre de situations dégradées par la réforme : 482495, soit 51,6 %
nb_cas_ameliored # nombre de situations améliorées par la réforme : 147178, soit 15,7 % => ce sont très probablement les gens en CL 16 ans, à qui on va arrêter de demander 45 annuités pour ne leur en demander que 43

# Résultats pour les situations modifiées par la réforme (= variable tous_les_cas à 0)
nb_cas_171_ou_moins # nombre de situations qui vont cotiser 171 trimestres ou moins : 29583 : que des cas de gens ayant commencé dans leur 21ème année, mais pas assez tôt pour être carrière longue, qui peuvent donc partir à 64 ans sans avoir leur 172 trimestres, puisque pour les non CL, ce n'est pas une exigence
nb_cas_172 # nombre de situations qui vont cotiser 172 trimestres pile : 170421
nb_cas_173_ou_plus # nombre de situations qui vont cotiser 173 trimestres ou plus (donc plus que 43 ans) : 429669 = 45.9 % des cas
nb_cas_173 # 126162
nb_cas_174 # 117823
nb_cas_175 # 74717
nb_cas_176_ou_plus = nb_cas_176 + nb_cas_177 + nb_cas_178 + nb_cas_179 + nb_cas_180
nb_cas_176_ou_plus # nombre de situations qui vont cotiser 176 trimestres ou plus (donc 44 ou plus) : 110 849 = 11,8 % des situations donnent une durée de cotisation de 44 ans ou plus
nb_cas_176 # 40832
nb_cas_177 # 31811
nb_cas_178 # 29052
nb_cas_179 # 9154
# exemples de cas qui vont cotiser 179 trimestres (44 ans et 3 trimestres) :
# nés du 2 juin au 31 aout 2000 qui ont commencé à travailler le 30 novembre ou le 1er décembre 2017
# nés en septembre 2000 qui ont commencé à travailler entre le 2 et le 31 décembre 2017 <= SUJET
# nés en septembre 2000 qui ont commencé à travailler entre le 1er janvier et le 1er septembre 2018 <= SUJET
# nés en octobre, novembre 2000 qui ont commencé à travailler le 31 août ou le 1er septembre 2018
# nés en décembre 2000 qui ont commencé à travailler entre le 2 septembre et le 1er octobre 2018 <= SUJET
nb_cas_180 # 118 : nés entre 2 et 30 septembre 2000, qui ont commencé à travailler le 30 novembre ou le 1er décembre 2017 + nés entre 2 et 31 décembre 2000, qui ont commencé à travailler le 31 aout ou le 1er septembre 2018
            # Ils sont CL 20. S'ils avaient commencé avant, ils seraient CL 18
            # Artefact de calcul dû à ma simplification "un mois plein de travail = 150 heures au SMIC"
#nb_cas_181_ou_plus # 0
nb_cas_travail_43_plus # 296130
nb_cas_travail_44_plus # 59067
nb_cas_travail_45_plus # 0


# Résultats pour l'ensemble des situations, qu'elles soient modifiées par la réforme ou pas (= variable tous_les_cas à 1)
nb_cas_171_ou_moins # nombre de situations qui vont cotiser 171 trimestres ou moins : 31443 : que des cas de gens ayant commencé dans leur 21ème année, mais pas assez tôt pour être carrière longue, qui peuvent donc partir à 64 ans sans avoir leur 172 trimestres, puisque pour les non CL, ce n'est pas une exigence
nb_cas_172 # nombre de situations qui vont cotiser 172 trimestres pile : 270751
nb_cas_173_ou_plus #  nombre de situations qui vont cotiser 173 trimestres ou plus (donc plus que 43 ans) : 633668 = 67,7 % des cas vont cotiser plus que 43 ans <= CE CHIFFRE EST LE CHIFFRE LE PLUS IMPORTANT
nb_cas_173 # 159681
nb_cas_174 # 151342
nb_cas_175 # 107993
nb_cas_176_ou_plus = nb_cas_176 + nb_cas_177 + nb_cas_178 + nb_cas_179 + nb_cas_180
nb_cas_176_ou_plus # 214 652 = 22,9 % des cas vont cotiser 44 ans ou plus
nb_cas_176 # 74169
nb_cas_177 # 63714
nb_cas_178 # 58196
nb_cas_179 # 18337
nb_cas_180 # 236 
#nb_cas_181_ou_plus # 0
nb_cas_travail_43_plus # 575070
nb_cas_travail_44_plus # 117736
nb_cas_travail_45_plus # 0


#%% 

### IV - Simulations (générations transitoires, carrières longues) ###

# calculs pour : 
    # les situations transitoires (donc les gens né entre septembre 1961 et décembre 1968)
    # des gens non carrière longue (c'est à dire qui ont commencé, grosso modo, après 21 ans)

# initialisation des variables, ne pas prêter attention

total_cas = 0
nb_cas_changed = 0
nb_cas_degraded = 0
nb_cas_ameliored = 0
nb_cas_171_ou_moins = 0
nb_cas_172 = 0
nb_cas_173 = 0
nb_cas_173_ou_plus = 0
nb_cas_174 = 0
nb_cas_175 = 0
nb_cas_176 = 0
nb_cas_177 = 0
nb_cas_178 = 0
nb_cas_179 = 0
nb_cas_180 = 0
nb_cas_181_ou_plus = 0
nb_cas_travail_43_plus = 0
nb_cas_travail_44_plus = 0
nb_cas_travail_45_plus = 0

nb_age_legal = 0
nb_cotisation = 0

tous_les_cas = 1

for Ny in range(1961,1969): # on ne va pas jusqu'en 1973 parce que la génération 1968 est la dernière qui, post réforme, fera l'objet de règles transitoires
    for Nm in range(1,13):
        for Nd in range(1,32):
            date_naissance = str(Nd)+"/"+str(Nm)+"/"+str(Ny)
            try:
                if datetime.datetime.strptime(date_naissance, '%d/%m/%Y') < datetime.datetime(1961, 9, 1):
                    continue # on ne regarde pas les cas nés avant le 1er septembre 1961, car pas concernés par la réforme
            except:
                continue
            #print(date_naissance)
            
            for Ty in range(Ny+15,Ny+23):
                for Tm in range(1,13):
                    for Td in range(1,32):
                        date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)
                            
                        try:
                            result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0, enregistrer = 0, filename = "cas_CL_transitoires_1961_1972")
                            
                            total_cas += 1
                            if result["situation_changee"] != "non":
                                nb_cas_changed += 1
                            if result["situation_changee"] == "dégradée":
                                nb_cas_degraded +=1
                            if result["situation_changee"] == "améliorée":
                                nb_cas_ameliored +=1
                                
                            if result["situation_changee"] != "non" or tous_les_cas:
                                if result["AP_nb_trim_reellement_cotises"] <= 171 : 
                                    nb_cas_171_ou_moins += 1
                                    # print("171-", date_naissance, date_debut_travail)
                                if result["AP_nb_trim_reellement_cotises"] == 172 : nb_cas_172 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 173 : nb_cas_173 += 1
                                if result["AP_nb_trim_reellement_cotises"] >= 173 : 
                                    nb_cas_173_ou_plus += 1
                                    if result["AP_vraie_cause_depart"] == 'duree_cotisation':
                                        nb_cotisation += 1
                                    elif result["AP_vraie_cause_depart"] == 'age_legal':
                                        nb_age_legal += 1
                                if result["AP_nb_trim_reellement_cotises"] == 174 : nb_cas_174 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 175 : nb_cas_175 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 176 : nb_cas_176 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 177 : nb_cas_177 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 178 : nb_cas_178 += 1
                                if result["AP_nb_trim_reellement_cotises"] == 179 : 
                                    nb_cas_179 += 1
                                    #print(date_naissance, date_debut_travail)
                                    
                                if result["AP_nb_trim_reellement_cotises"] == 180 : 
                                    nb_cas_180 += 1
    
                                if result["AP_nb_trim_reellement_cotises"] > 180 : nb_cas_181_ou_plus += 1
    
                                if result["AP_duree_reelle_travail.years"] >= 43 : 
                                    nb_cas_travail_43_plus += 1
                                if result["AP_duree_reelle_travail.years"] >= 44 : nb_cas_travail_44_plus += 1
                                if result["AP_duree_reelle_travail.years"] >= 45 : 
                                    nb_cas_travail_45_plus += 1
    
                        except ValueError:
                            pass
                        except Exception as e:
                            print("autre erreur")
                            err = e

# résultats

total_cas # 7 828 038
nb_cas_changed # 6245777
nb_cas_degraded # 4577298
nb_cas_ameliored # 1668479

# Avec tous les cas = 0 (donc que les cas changés par la réforme)
nb_cas_171_ou_moins # 2053121
nb_cas_172 # 1595692
#nb_cas_173_ou_plus # 2596964 =  % des cas
nb_cas_173 # 941517
nb_cas_174 # 714050
nb_cas_175 # 683152
nb_cas_176 # 140367
#nb_cas_177_ou_plus #  = 24.5 % des cas
nb_cas_177 # 70164
nb_cas_178 # 38324
nb_cas_179 # 9272
nb_cas_180 # 118
#nb_cas_181_ou_plus # 0
nb_cas_travail_43_plus # 2076811
nb_cas_travail_44_plus # 96630
nb_cas_travail_45_plus # 0


#TODO : remplir au dessus
#TODO : faire tourner et remplir en dessous


# Avec tous les cas = 1 (donc y compris les cas PAS changés par la réforme)
nb_cas_171_ou_moins # 2 121 690
nb_cas_172 # 1 697 001
#nb_cas_173_ou_plus # = 53,1 % des cas
nb_cas_173 # 1 107 573
nb_cas_174 # 946 698
nb_cas_175 # 941 980
nb_cas_176 # 405 082
#nb_cas_177_ou_plus #  = 7.9 % des cas
nb_cas_177 # 296 766
nb_cas_178 # 245 806
nb_cas_179 # 82 380
nb_cas_180 # 1062
#nb_cas_181_ou_plus # 0
nb_cas_travail_43_plus # 3 446 330
nb_cas_travail_44_plus # 525 513
nb_cas_travail_45_plus # 0


# calcul_situation_indiv("8/1/1964", "15/4/1983", verbose = 1)

#%% création fichier cas carrière longue non transitoires

# for Nm in range(1,13):
#     for Nd in range(1,32):
#         date_naissance = str(Nd)+"/"+str(Nm)+"/2000"
#         #print(date_naissance)
        
#         for Ty in range(2015,2022):
#             for Tm in range(1,13):
#                 for Td in range(1,32):
#                     date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)

#                     try:
#                         result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0, enregistrer = 1, filename = "cas_CL_non_transitoires")
#                         # if AP_nb_trim_reellement_cotises==175:
#                         #     print(date_naissance,"\t\t",date_debut_travail,"\t\t",AP_nb_trim_reellement_cotises)
#                     except ValueError:
#                         pass
#                     except Exception as e:
#                         print("autre erreur")
#                         err = e

#%% création fichier cas général (début travail à partir de l'année des 22 ans)

# for Nm in range(1,13):
#     for Nd in range(1,32):
#         date_naissance = str(Nd)+"/"+str(Nm)+"/2000"
#         #print(date_naissance)
        
#         for Ty in range(2022,2023):
#             for Tm in range(1,13):
#                 for Td in range(1,32):
#                     date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)

#                     try:
#                         result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0, enregistrer = 1, filename = "cas_generaux")
#                         # if AP_nb_trim_reellement_cotises==175:
#                         #     print(date_naissance,"\t\t",date_debut_travail,"\t\t",AP_nb_trim_reellement_cotises)
#                     except ValueError:
#                         pass
#                     except Exception as e:
#                         print("autre erreur")
#                         err = e

#%% création fichier cas carrière longue transitoires

for Ny in range(1961,1969): # on ne va pas jusqu'en 1973 parce que la génération 1968 est la dernière qui, post réforme, fera l'objet de règles transitoires
    for Nm in range(1,13):
        for Nd in range(1,32):
            date_naissance = str(Nd)+"/"+str(Nm)+"/"+str(Ny)
            try:
                if datetime.datetime.strptime(date_naissance, '%d/%m/%Y') < datetime.datetime(1961, 9, 1):
                    continue # on ne regarde pas les cas nés avant le 1er septembre 1961, car pas concernés par la réforme
            except:
                continue
            #print(date_naissance)
            
            for Ty in range(Ny+15,Ny+23):
                for Tm in range(1,13):
                    for Td in range(1,32):
                        date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)
    
                        try:
                            result = calcul_situation_indiv(date_naissance, date_debut_travail, verbose = 0, enregistrer = 1, filename = "cas_CL_transitoires_1961_1972")
                            # if AP_nb_trim_reellement_cotises==175:
                            #     print(date_naissance,"\t\t",date_debut_travail,"\t\t",AP_nb_trim_reellement_cotises)
                        except ValueError:
                            pass
                        except Exception as e:
                            print("autre erreur")
                            err = e





















