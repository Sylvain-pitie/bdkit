import sys
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import gridspec  # Importez gridspec

def band3(kindatm,atm1,atm2,atm3,typeorb1,typeorb2,typeorb3,color1,color2,color3,title,labelfig,xanch,yanch,fsize,xrot,emin,emax,dpi):
###########Lecture des datas nécessaires au tracés des bandes######################
###############Lecture de la structures de bandes totales##########################
    colonne1 = []
    colonne2 = []

    with open("./band/BAND.dat","r") as fichier:
        lignes = fichier.readlines()

    for ligne in lignes:
        # Ignorez les lignes qui commencent par un caractère de commentaire
        if not ligne.startswith('#'):
            # Vérifiez si la ligne contient au moins deux valeurs avant de les déballer
            valeurs = ligne.strip().split()
            if len(valeurs) >= 2:
                valeur1, valeur2 = map(float, valeurs)
                colonne1.append(valeur1)
                colonne2.append(valeur2)

#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier

    nom_fichier = "./band/PBAND_"+atm1+".dat"


    # Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    donnees = pd.read_csv(nom_fichier, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], skiprows=3, comment='#')

    # Renommez les colonnes si nécessaire
    donnees.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5", "Colonne6","Colonne7", "Colonne8", "Colonne9", "Colonne10", "Colonne11",]

    # Convertissez les données en listes
    raw1 = donnees["Colonne1"].tolist()
    raw2 = donnees["Colonne2"].tolist()
    donnees["Colonne3"] = donnees["Colonne3"] * 10
    raws1 = donnees["Colonne3"].tolist()
    donnees["Somme"] = donnees["Colonne4"] + donnees["Colonne5"] + donnees["Colonne6"]
    donnees["Somme"] = donnees["Somme"] * 10
    rawp1 = donnees["Somme"].tolist()
    donnees["Sommed"] = donnees["Colonne7"] + donnees["Colonne8"] + donnees["Colonne9"] + donnees["Colonne10"] + donnees["Colonne11"]
    donnees["Sommed"] = donnees["Sommed"] * 10
    rawd1 = donnees["Sommed"].tolist()
#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier

    nom_fichier = "./band/PBAND_"+atm2+".dat"


    # Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    donnees = pd.read_csv(nom_fichier, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], skiprows=3, comment='#')

    # Renommez les colonnes si nécessaire
    donnees.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5", "Colonne6","Colonne7", "Colonne8", "Colonne9", "Colonne10", "Colonne11",]

    # Convertissez les données en listes
    raw1 = donnees["Colonne1"].tolist()
    raw2 = donnees["Colonne2"].tolist()
    donnees["Colonne3"] = donnees["Colonne3"] * 10
    raws2 = donnees["Colonne3"].tolist()
    donnees["Somme"] = donnees["Colonne4"] + donnees["Colonne5"] + donnees["Colonne6"]
    donnees["Somme"] = donnees["Somme"] * 10
    rawp2 = donnees["Somme"].tolist()
    donnees["Sommed"] = donnees["Colonne7"] + donnees["Colonne8"] + donnees["Colonne9"] + donnees["Colonne10"] + donnees["Colonne11"]
    donnees["Sommed"] = donnees["Sommed"] * 10
    rawd2 = donnees["Sommed"].tolist()
#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier

    nom_fichier = "./band/PBAND_"+atm3+".dat"


    # Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    donnees = pd.read_csv(nom_fichier, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], skiprows=3, comment='#')

    # Renommez les colonnes si nécessaire
    donnees.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5", "Colonne6","Colonne7", "Colonne8", "Colonne9", "Colonne10", "Colonne11",]

    # Convertissez les données en listes
    raw1 = donnees["Colonne1"].tolist()
    raw2 = donnees["Colonne2"].tolist()
    donnees["Colonne3"] = donnees["Colonne3"] * 10
    raws3 = donnees["Colonne3"].tolist()
    donnees["Somme"] = donnees["Colonne4"] + donnees["Colonne5"] + donnees["Colonne6"]
    donnees["Somme"] = donnees["Somme"] * 10
    rawp3 = donnees["Somme"].tolist()
    donnees["Sommed"] = donnees["Colonne7"] + donnees["Colonne8"] + donnees["Colonne9"] + donnees["Colonne10"] + donnees["Colonne11"]
    donnees["Sommed"] = donnees["Sommed"] * 10
    rawd3 = donnees["Sommed"].tolist()


##########################################################################################
# Ouvrir le fichier en mode lecture
    with open("./band/KLABELS", "r") as fichier:
        lignes = fichier.readlines()

# Initialiser des listes pour stocker les labels et les coordonnées
    etiquettes = []
    coordonnees_x = []
# Parcourir chaque ligne du fichier
    for ligne in lignes:
    # Supprimer les espaces en début et fin de ligne
        ligne = ligne.strip()
    
    # Ignorer les lignes vides
        if not ligne:
            continue
    
    # Diviser la ligne en mots
        mots = ligne.split()
    
    # Vérifier si la ligne a au moins deux mots
        if len(mots) >= 2:
        # Essayer de convertir le deuxième mot en nombre
            try:
                coordonnee = float(mots[1])
                etiquettes.append(mots[0])
                coordonnees_x.append(coordonnee)
            except ValueError:
            # Si la conversion échoue, ignorez cette ligne
                continue
    etiquettes = [label.replace("GAMMA", "$\Gamma$") for label in etiquettes]
    etiquettes = [label.replace("_2", "$_2$") for label in etiquettes]
    etiquettes = [label.replace("_0", "$_0$") for label in etiquettes]
    etiquettes = [label.replace("_1", "$_1$") for label in etiquettes]
    etiquettes = [label.replace("+", "  ") for label in etiquettes]
    etiquettes = [label.replace("-", "  ") for label in etiquettes]
    etiquettes = [label.replace("SIGMA", "$\Sigma$") for label in etiquettes]
###########Lecture des datas nécessaires au tracés des bandes######################
###############Lecture de la structures de bandes totales##########################
    tdosfile = "./dos/TDOS.dat"

    TDdos = pd.read_csv(tdosfile, delim_whitespace=True, usecols=[0, 1], skiprows=1, comment='#')
# Renommez les colonnes si nécessaire
    TDdos.columns = ["Colonne1", "Colonne2"]
# Convertissez les données en listes
    doscol1 = TDdos["Colonne1"].tolist()
    doscol2 = TDdos["Colonne2"].tolist()

#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier
    ndosfile = "./dos/PDOS_"+atm1+".dat"


# Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    ndos = pd.read_csv(ndosfile, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], skiprows=1, comment='#')

# Renommez les colonnes si nécessaire
    ndos.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5","Colonne6", "Colonne7", "Colonne8", "Colonne9", "Colonne10"]

# Convertissez les données en listes
    dos1 = ndos["Colonne1"].tolist()
    doss1 = ndos["Colonne2"].tolist()
    ndos["Somme"] = ndos["Colonne3"] + ndos["Colonne4"] + ndos["Colonne5"]
    dosp1 = ndos["Somme"].tolist()
    ndos["Somme"] = ndos["Colonne6"] + ndos["Colonne7"] + ndos["Colonne8"] + ndos["Colonne9"] + ndos["Colonne10"]
    dosd1 = ndos["Somme"].tolist()

#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier
    ndosfile = "./dos/PDOS_"+atm2+".dat"


# Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    ndos = pd.read_csv(ndosfile, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], skiprows=1, comment='#')

# Renommez les colonnes si nécessaire
    ndos.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5","Colonne6", "Colonne7", "Colonne8", "Colonne9", "Colonne10"]

# Convertissez les données en listes
    dos1 = ndos["Colonne1"].tolist()
    doss2 = ndos["Colonne2"].tolist()
    ndos["Somme"] = ndos["Colonne3"] + ndos["Colonne4"] + ndos["Colonne5"]
    dosp2 = ndos["Somme"].tolist()
    ndos["Somme"] = ndos["Colonne6"] + ndos["Colonne7"] + ndos["Colonne8"] + ndos["Colonne9"] + ndos["Colonne10"]
    dosd2 = ndos["Somme"].tolist()
#########Lecture de la structure de bandes projeté sur N###########################
# Définissez le nom de votre fichier
    ndosfile = "./dos/PDOS_"+atm3+".dat"


# Utilisez la fonction `read_csv` de pandas pour lire uniquement les 6 premières colonnes
    ndos = pd.read_csv(ndosfile, delim_whitespace=True, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], skiprows=1, comment='#')

# Renommez les colonnes si nécessaire
    ndos.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", "Colonne5","Colonne6", "Colonne7", "Colonne8", "Colonne9", "Colonne10"]

# Convertissez les données en listes
    dos1 = ndos["Colonne1"].tolist()
    doss3 = ndos["Colonne2"].tolist()
    ndos["Somme"] = ndos["Colonne3"] + ndos["Colonne4"] + ndos["Colonne5"]
    dosp3 = ndos["Somme"].tolist()
    ndos["Somme"] = ndos["Colonne6"] + ndos["Colonne7"] + ndos["Colonne8"] + ndos["Colonne9"] + ndos["Colonne10"]
    dosd3 = ndos["Somme"].tolist()

#######################################################################################################
#######################################################################################################
    fig, ax = plt.subplots(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
    plt.subplot(gs[0])
    plt.plot(colonne1, colonne2, color="gray", zorder=1)
    for f in range(len(typeorb1)):
        if str(typeorb1[f]) == "s":
            plt.scatter(raw1,raw2, s=raws1, facecolors='none', alpha=1.0, color=color1[f], zorder=2, label=atm1+'-s')
        elif str(typeorb1[f]) == "p":
            plt.scatter(raw1,raw2, s=rawp1, facecolors='none', alpha=1.0, color=color1[f], zorder=2, label=atm1+'-p')
        elif str(typeorb1[f]) == "d":
            plt.scatter(raw1,raw2, s=rawd1, facecolors='none', alpha=1.0, color=color1[f], zorder=2, label=atm1+'-d')
    for f in range(len(typeorb2)):
        if str(typeorb2[f]) == "s":
            plt.scatter(raw1,raw2, s=raws2, facecolors='none', alpha=1.0, color=color2[f], zorder=2, label=atm2+'-s')
        elif str(typeorb2[f]) == "p":
            plt.scatter(raw1,raw2, s=rawp2, facecolors='none', alpha=1.0, color=color2[f], zorder=2, label=atm2+'-p')
        elif str(typeorb2[f]) == "d":
            plt.scatter(raw1,raw2, s=rawd2, facecolors='none', alpha=1.0, color=color2[f], zorder=2, label=atm2+'-d')
    for f in range(len(typeorb3)):
        if str(typeorb3[f]) == "s":
            plt.scatter(raw1,raw2, s=raws3, facecolors='none', alpha=1.0, color=color3[f], zorder=2, label=atm3+'-s')
        elif str(typeorb3[f]) == "p":
            plt.scatter(raw1,raw2, s=rawp3, facecolors='none', alpha=1.0, color=color3[f], zorder=2, label=atm3+'-p')
        elif str(typeorb3[f]) == "d":
            plt.scatter(raw1,raw2, s=rawd3, facecolors='none', alpha=1.0, color=color3[f], zorder=2, label=atm3+'-d')

    plt.axhline(y=0,color="black", linestyle="dashed")
    # Ajoutez des lignes verticales aux coordonnées spécifiées
    for coord_x in coordonnees_x:
        plt.axvline(x=coord_x, color='black', zorder=3)

    # Personnalisez les marques de l'axe x
    plt.xticks(coordonnees_x, etiquettes, rotation=xrot)


    plt.xlim(min(colonne1),max(colonne1)+0.001)
    plt.ylim(emin,emax)
    plt.ylabel("Energy (eV)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    plt.subplot(gs[1])  # Utilisez gs[1] pour le premier sous-tracé
    plt.plot(doscol2, doscol1, color="black", zorder=1, label="TDOS")
    plt.fill_between(doscol2, doscol1, color='gray', alpha=0.8)
    for f in range(len(typeorb1)):
        if str(typeorb1[f]) == "s":
            plt.plot(doss1,dos1, color=color1[f], zorder=2, label=atm1+'-s')
        elif str(typeorb1[f]) == "p":
            plt.plot(dosp1,dos1, color=color1[f], zorder=2, label=atm1+'-p')
        elif str(typeorb1[f]) == "d":
            plt.plot(dosd1,dos1, color=color1[f], zorder=2, label=atm1+'-d')
    for f in range(len(typeorb2)):
        if str(typeorb2[f]) == "s":
            plt.plot(doss2,dos1, color=color2[f], zorder=2, label=atm2+'-s')
        elif str(typeorb2[f]) == "p":
            plt.plot(dosp2,dos1, color=color2[f], zorder=2, label=atm2+'-p')
        elif str(typeorb2[f]) == "d":
            plt.plot(dosd2,dos1, color=color2[f], zorder=2, label=atm2+'-d')
    for f in range(len(typeorb3)):
        if str(typeorb3[f]) == "s":
            plt.plot(doss3,dos1, color=color3[f], zorder=2, label=atm3+'-s')
        elif str(typeorb3[f]) == "p":
            plt.plot(dosp3,dos1, color=color3[f], zorder=2, label=atm3+'-p')
        elif str(typeorb3[f]) == "d":
            plt.plot(dosd3,dos1, color=color3[f], zorder=2, label=atm3+'-d') 
    plt.axhline(y=0,color="black", linestyle="dashed")

    maxx = 0
    for i in range(len(doscol1)):
        if doscol1[i] >= -8 and doscol1[i] <= 5:
            if doscol2[i] > maxx:
                maxx = doscol2[i]

    plt.xlim(min(doscol2),maxx+1)
    plt.ylim(emin,emax)
    plt.xlabel("DOS (a. u.)",fontsize=fsize)
    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places

    plt.gca().set_ylabel("")
    plt.gca().set_yticks([])
    plt.suptitle(title, y=0.98, fontsize=fsize)
    plt.legend(loc="upper right",fontsize=fsize,bbox_to_anchor=(xanch, yanch),frameon=False)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    fig.text(0.01, 0.95, labelfig, fontsize=22)
    plt.subplots_adjust(top=0.93, bottom=0.11, left=0.12, right=0.98,wspace=0.15)
    plt.savefig(atm1+atm2+atm3+"bandplot.png", format="png", dpi=dpi)
