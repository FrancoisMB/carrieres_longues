# -*- coding: utf-8 -*-

import datetime, os
from dateutil.relativedelta import relativedelta
from pathlib import Path

# set le dossier de travail
path_wd = r"D:\Code\Code_Python\calcul_carriere_longue_44"
os.chdir(path_wd)

# initialisation des fichiers
if not os.path.exists('csv_resultats.txt'):
    Path('csv_resultats.txt').touch()
    with open("csv_resultats.txt","w") as f:
        f.write("date_naissance;date_debut_travail;AV_cas_carriere_longue;AV_date_depart_selon_AP_age_legal;AV_date_depart_selon_nb_trim;AV_ce_qui_determine_vrai_age_depart;AV_AP_age_reel_depart;AV_duree_reelle_cotis;AV_AP_duree_reelle_travail;AP_cas_carriere_longue;AP_date_depart_selon_AP_age_legal;AP_date_depart_selon_nb_trim;AP_ce_qui_determine_vrai_age_depart;AP_AP_age_reel_depart;AP_duree_reelle_cotis;AP_AP_duree_reelle_travail")


def calcul_regles(date_naissance, date_debut_travail, verbose = 1, enregistrer = 0):
    
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
    AV_total_trim_a_cotiser = 172
    AV_age_legal = 62

    if date_naissance.year <= 1960:         AV_total_trim_a_cotiser = 167
    elif date_naissance.year == 1961:       AV_total_trim_a_cotiser = 168
    elif date_naissance.year == 1962:       AV_total_trim_a_cotiser = 168
    elif date_naissance.year == 1963:       AV_total_trim_a_cotiser = 168
    elif date_naissance.year == 1964:       AV_total_trim_a_cotiser = 169
    elif date_naissance.year == 1965:       AV_total_trim_a_cotiser = 169
    elif date_naissance.year == 1966:       AV_total_trim_a_cotiser = 169
    elif date_naissance.year == 1967:       AV_total_trim_a_cotiser = 170
    elif date_naissance.year == 1968:       AV_total_trim_a_cotiser = 170
    elif date_naissance.year == 1969:       AV_total_trim_a_cotiser = 170
    elif date_naissance.year == 1970:       AV_total_trim_a_cotiser = 171
    elif date_naissance.year == 1971:       AV_total_trim_a_cotiser = 171
    elif date_naissance.year == 1972:       AV_total_trim_a_cotiser = 171
    elif date_naissance.year >= 1973:       AV_total_trim_a_cotiser = 172

    # 4 - Ensuite, on rectifie l'âge légal de départ à la retraite pour les cas carrière longue
    if AV_CL == "16":
        AV_age_legal = 58
    elif AV_CL == "20":
        AV_age_legal = 60
    else:
        AV_age_legal = 62
    
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
        # Si tout décembre est travaillé : 1 mois cotisé
        # Si tout novembre est également travaillé : 2 mois cotisés
        # Si tout octobre est également travaillé : 3 mois cotisés
        # Si tout septembre est également travaillé : 4 mois cotisés
        # Au delà : 4 mois cotisés, car c'est le maximum chaque année
        # (NB il est fait l'hypothèse simplificatrice que 150 heures au SMIC = un mois plein de travail)
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
        # si le nb de trimestres cotisés est pile 172, c'est que 4 trimestres ont été cotisés la première année, toutes les années suivantes aussi
        # et 4 la dernière année. Notre cas aura tous ses trimestres le 31 décembre de sa dernière année de travail et pourra partir le 1er janvier suivant
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 1, 1, 1)
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-1:
        # si c'est 171, il lui manque un trimestre, il pourra partir au 1er avril
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 2, 4, 1) # c'est +2 parce que annees_civ_pleinement_cotisees = 42
        AV_nb_trimestres_cotises +=1
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-2:
        # si c'est 171, il lui manque deux trimestres, il pourra partir au 1er juillet
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 2, 7, 1)
        AV_nb_trimestres_cotises += 2
    elif AV_nb_trimestres_cotises == AV_total_trim_a_cotiser-3:
        # si c'est 169, il lui manque trois trimestres, il pourra partir au 1er octobre
        AV_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AV_annees_civiles_pleinement_cotisees + 2, 10, 1)
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
    if AP_CL == "16":
        AP_age_legal = 58
    elif AP_CL == "18":
        AP_age_legal = 60
    elif AP_CL == "20":
        AP_age_legal = AP_age_legal - 2 
    elif AP_CL == "21":
        AP_age_legal = AP_age_legal - 1 # Pas complètement certain, mais fixer 63, plutôt que "âge légal - 1"  n'aurait pas de sens et créerait des effets de seuil sur les cas transitoires
    else:
        AP_age_legal = 64
    
    # 5 - Calcul date légale de départ
    # Pas modifié par la réforme
    # Pour quelqu'un né entre le 2 et le 31 du mois, il peut partir le 1er du mois qui suit sont Xème anniversaire, où X = son âge légal de départ en retraite
    # Pour quelqu'un né le 1er du mois, il peut partir dès ce jour là
    if date_naissance.day == 1:
        AP_date_legale = date_naissance + relativedelta(years=AP_age_legal)
    else:
        AP_date_legale = (date_naissance.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) + relativedelta(years=AP_age_legal)
    
    # 6 - Calcul date de départ avec nombre de trimestres de cotisation
    AP_nb_trimestres_cotises = 0
    AP_annees_civiles_pleinement_cotisees = 0
    
    # 6.1 - Nb trimestres cotisés première année
    # Pas modifié par la réforme
    # La première année, entre 0 et 4 trimestres peuvent être cotisés, selon la date de début de travail :
        # Si tout décembre est travaillé : 1 mois cotisé
        # Si tout novembre est également travaillé : 2 mois cotisés
        # Si tout octobre est également travaillé : 3 mois cotisés
        # Si tout septembre est également travaillé : 4 mois cotisés
        # Au delà : 4 mois cotisés, car c'est le maximum chaque année
        # (NB il est fait l'hypothèse simplificatrice que 150 heures au SMIC = un mois plein de travail)
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
        # si le nb de trimestres cotisés est pile 172, c'est que 4 trimestres ont été cotisés la première année, toutes les années suivantes aussi
        # et 4 la dernière année. Notre cas aura tous ses trimestres le 31 décembre de sa dernière année de travail et pourra partir le 1er janvier suivant
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 1, 1, 1)
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-1:
        # si c'est 171, il lui manque un trimestre, il pourra partir au 1er avril
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 2, 4, 1)
        AP_nb_trimestres_cotises +=1
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-2:
        # si c'est 171, il lui manque deux trimestres, il pourra partir au 1er juillet
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 2, 7, 1)
        AP_nb_trimestres_cotises += 2
    elif AP_nb_trimestres_cotises == AP_total_trim_a_cotiser-3:
        # si c'est 169, il lui manque trois trimestres, il pourra partir au 1er octobre
        AP_date_depart_avec_nb_trim = datetime.datetime(date_debut_travail.year + AP_annees_civiles_pleinement_cotisees + 2, 10, 1)
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
    
    
    
    
    
    
    # Résumé
    AV_vraie_cause_depart =""
    AP_vraie_cause_depart =""

    if AV_date_depart_reelle == AP_date_depart_reelle:
        if verbose:
            print(" ")
            print("RIEN NE CHANGE")
        else:
            pass

    if verbose:
        print("\t\t\t\t\t\t\t\t\t\t\t\t yyyy-mm-dd")
        print("Né le \t\t\t\t\t\t\t\t\t\t\t", date_naissance.date())
        print("Début travail le \t\t\t\t\t\t\t\t", date_debut_travail.date())
        print("\t\t\t\t\t\t\t - AVANT réforme -")
        print("Cas carrière longue :", AV_CL)
        print("Date départ selon âge légal \t\t\t\t\t", AV_date_legale.date())
        print("Date départ selon nb trim \t\t\t\t\t\t", AV_date_depart_avec_nb_trim.date())
        
        if AV_date_depart_reelle == AV_date_depart_avec_nb_trim:
            print("Date de départ déterminée par le nb de trim \t", AV_date_depart_reelle.date())
            AV_vraie_cause_depart = "duree_cotisation"
        elif AV_date_depart_reelle == AV_date_legale:
            print("Date de départ déterminée par l'âge légal \t\t", AV_date_depart_reelle.date())
            AV_vraie_cause_depart = "AV_age_legal"
        print("Âge réel de départ =", AV_age_reel)
        print("Durée réelle de cotis =", AV_nb_trim_reellement_cotises/4)
        print("Durée reelle de travail =", AV_duree_reelle_travail)

        print("\t\t\t\t\t\t\t - APRES réforme -")
        print("Cas carrière longue :", AP_CL)
        print("Date départ selon âge légal \t\t\t\t\t", AP_date_legale.date())
        print("Date départ selon nb trim \t\t\t\t\t\t", AP_date_depart_avec_nb_trim.date())
        
        if AP_date_depart_reelle == AP_date_depart_avec_nb_trim:
            print("Date de départ déterminée par le nb de trim \t", AP_date_depart_reelle.date())
            AP_vraie_cause_depart = "duree_cotisation"
        elif AP_date_depart_reelle == AP_date_legale:
            print("Date de départ déterminée par l'âge légal \t\t", AP_date_depart_reelle.date())
            AP_vraie_cause_depart = "AP_age_legal"
        print("Âge réel de départ =", AP_age_reel)
        print("Durée réelle de cotis =", AP_nb_trim_reellement_cotises/4)
        print("Durée reelle de travail =", AP_duree_reelle_travail)
        print(" ")
        print(" ")
        print(" ")

  
    # Enregistrement dans fichier
    if AV_date_depart_reelle == AV_date_depart_avec_nb_trim:
        AV_vraie_cause_depart = "duree_cotisation"
    elif AV_date_depart_reelle == AV_date_legale:
        AV_vraie_cause_depart = "AV_age_legal"

    if AP_date_depart_reelle == AP_date_depart_avec_nb_trim:
        AP_vraie_cause_depart = "duree_cotisation"
    elif AP_date_depart_reelle == AP_date_legale:
        AP_vraie_cause_depart = "AP_age_legal"
    
    if enregistrer:
        with open("csv_resultats.txt","a") as f:
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
                    ";"+str(AP_duree_reelle_travail.years)+" an(s),"+ str(AP_duree_reelle_travail.months) +" mois et "+ str(AP_duree_reelle_travail.days) +" jour(s)") 
    
    if AP_nb_trim_reellement_cotises > 172:
        return AP_nb_trim_reellement_cotises
    else:
        return 0

# Dates au format "jj/mm/aaaa"
date_naissance = "2/09/2000"
date_debut_travail = "2/12/2015"
# calcul_regles(date_naissance, date_debut_travail)


date_naissance = "12/12/2000"
date_debut_travail = "13/7/2014"
# calcul_regles(date_naissance, date_debut_travail)

# Vont travailler 176 trimestres
# Né entre 2 et 30 septembre
# Début travail 30/11 ou 1/12 de 2015 ou 2017

# Né entre 2 et 31 décembre
# Début travail 31/8, 1/9 ou 2/9 de 2016 ou 2018

date_naissance = "02/01/2000"
date_debut_travail = "15/11/2021"
#calcul_regles(date_naissance, date_debut_travail)



#%%


for Nm in range(1,13):
    for Nd in range(1,32):
        date_naissance = str(Nd)+"/"+str(Nm)+"/2000"
        #print(date_naissance)
        
        for Ty in range(2015,2018):
            for Tm in range(1,13):
                for Td in range(1,32):
                    date_debut_travail = str(Td)+"/"+str(Tm)+"/"+str(Ty)

                    try:
                        AP_nb_trim_reellement_cotises = calcul_regles(date_naissance, date_debut_travail, verbose = 0, enregistrer = 1)
                        # if AP_nb_trim_reellement_cotises==175:
                        #     print(date_naissance,"\t\t",date_debut_travail,"\t\t",AP_nb_trim_reellement_cotises)
                    except ValueError:
                        pass
                    except Exception as e:
                        print("autre erreur")
                        err = e

