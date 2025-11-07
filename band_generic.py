import sys
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import MaxNLocator

def band_generic(atoms, typeorbs, colors, title, labelfig, xanch, yanch, fsize, xrot, emin, emax, dpi, pformat):
    """
    Fonction généraliste pour tracer les structures de bandes pour n'importe quel nombre d'atomes
    
    Args:
        atoms: liste des noms d'atomes ['N', 'Pb', 'O', ...]
        typeorbs: liste des listes d'orbitales [['p'], ['s','p'], ['d'], ...]
        colors: liste des listes de couleurs [['green'], ['blue','red'], ['orange'], ...]
        title: titre du graphique
        labelfig: label de la figure
        xanch, yanch: position de la légende
        fsize: taille de police
        xrot: rotation des labels k-path
        emin, emax: limites en énergie
        dpi: résolution de l'image
        pformat: plot format
    """
    
    # Lecture des données de bande principale
    colonne1 = []
    colonne2 = []
    
    with open("./band/BAND.dat", "r") as fichier:
        lignes = fichier.readlines()
    
    for ligne in lignes:
        if not ligne.startswith('#'):
            valeurs = ligne.strip().split()
            if len(valeurs) >= 2:
                valeur1, valeur2 = map(float, valeurs)
                colonne1.append(valeur1)
                colonne2.append(valeur2)
    
    # Stockage des données projetées pour chaque atome
    atoms_data = {}
    
    # Lecture des données projetées pour chaque atome
    for atom in atoms:
        nom_fichier = f"./band/PBAND_{atom}.dat"
        
        # Lecture des données de bande projetées
        donnees = pd.read_csv(nom_fichier, delim_whitespace=True, 
                             usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                             skiprows=3, comment='#')
        
        donnees.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", 
                          "Colonne5", "Colonne6", "Colonne7", "Colonne8", 
                          "Colonne9", "Colonne10", "Colonne11"]
        
        # Extraction des coordonnées k et énergies
        raw1 = donnees["Colonne1"].tolist()
        raw2 = donnees["Colonne2"].tolist()
        
        # Calcul des contributions orbitales
        donnees["Colonne3"] = donnees["Colonne3"] * 10
        raws = donnees["Colonne3"].tolist()  # s orbital
        
        donnees["Somme_p"] = donnees["Colonne4"] + donnees["Colonne5"] + donnees["Colonne6"]
        donnees["Somme_p"] = donnees["Somme_p"] * 10
        rawp = donnees["Somme_p"].tolist()  # p orbitals
        
        donnees["Somme_d"] = (donnees["Colonne7"] + donnees["Colonne8"] + 
                             donnees["Colonne9"] + donnees["Colonne10"] + 
                             donnees["Colonne11"])
        donnees["Somme_d"] = donnees["Somme_d"] * 10
        rawd = donnees["Somme_d"].tolist()  # d orbitals
        
        donnees["Total"] = donnees["Colonne3"] + donnees["Somme_p"] + donnees["Somme_d"]
        rawt = donnees["Total"].tolist()  # total
        
        atoms_data[atom] = {
            'raw1': raw1,
            'raw2': raw2,
            'raws': raws,
            'rawp': rawp,
            'rawd': rawd,
            'rawt': rawt
        }
    
    # Lecture des labels k-path
    with open("./band/KLABELS", "r") as fichier:
        lignes = fichier.readlines()
    
    etiquettes = []
    coordonnees_x = []
    
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        
        mots = ligne.split()
        if len(mots) >= 2:
            try:
                coordonnee = float(mots[1])
                etiquettes.append(mots[0])
                coordonnees_x.append(coordonnee)
            except ValueError:
                continue
    
    # Formatage des labels k-path
    replacements = {
        "GAMMA": "$\\Gamma$",
        "DELTA": "$\\Delta$", 
        "SIGMA": "$\\Sigma$",
        "_2": "$_2$",
        "_0": "$_0$",
        "_1": "$_1$",
        "+": "  ",
        "-": "  "
    }
    
    for old, new in replacements.items():
        etiquettes = [label.replace(old, new) for label in etiquettes]
    
    # Lecture des DOS
    # TDOS
    tdosfile = "./dos/TDOS.dat"
    TDdos = pd.read_csv(tdosfile, delim_whitespace=True, usecols=[0, 1], 
                       skiprows=1, comment='#')
    TDdos.columns = ["Colonne1", "Colonne2"]
    doscol1tmp = TDdos["Colonne1"].tolist()
    doscol2tmp = TDdos["Colonne2"].tolist()
    
    # PDOS pour chaque atome
    atoms_dos = {}
    
    for atom in atoms:
        ndosfile = f"./dos/PDOS_{atom}.dat"
        
        ndos = pd.read_csv(ndosfile, delim_whitespace=True, 
                          usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 
                          skiprows=1, comment='#')
        
        ndos.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4", 
                       "Colonne5", "Colonne6", "Colonne7", "Colonne8", 
                       "Colonne9", "Colonne10"]
        
        dos1tmp = ndos["Colonne1"].tolist()
        doss = ndos["Colonne2"].tolist()  # s DOS
        
        ndos["Somme_p"] = ndos["Colonne3"] + ndos["Colonne4"] + ndos["Colonne5"]
        dosp = ndos["Somme_p"].tolist()  # p DOS
        
        ndos["Somme_d"] = (ndos["Colonne6"] + ndos["Colonne7"] + 
                          ndos["Colonne8"] + ndos["Colonne9"] + ndos["Colonne10"])
        dosd = ndos["Somme_d"].tolist()  # d DOS
        
        ndos["Total"] = ndos["Colonne2"] + ndos["Somme_p"] + ndos["Somme_d"]
        dost = ndos["Total"].tolist()  # total DOS
        
        atoms_dos[atom] = {
            'dos1': dos1tmp,
            'doss': doss,
            'dosp': dosp,
            'dosd': dosd,
            'dost': dost
        }
    
    # Interpolation
    dos1tmp = np.array(doscol1tmp)
    doscol1tmp = np.array(doscol1tmp)
    doscol2tmp = np.array(doscol2tmp)
    
    interpolationcol2 = interp1d(doscol1tmp, doscol2tmp, kind='cubic')
    
    # Interpolation pour chaque atome
    atoms_dos_interp = {}
    
    for atom in atoms:
        dos_data = atoms_dos[atom]
        dos1tmp = np.array(dos_data['dos1'])
        doss_tmp = np.array(dos_data['doss'])
        dosp_tmp = np.array(dos_data['dosp'])
        dosd_tmp = np.array(dos_data['dosd'])
        dost_tmp = np.array(dos_data['dost'])
        
        interpolation_s = interp1d(dos1tmp, doss_tmp, kind='cubic')
        interpolation_p = interp1d(dos1tmp, dosp_tmp, kind='cubic')
        interpolation_d = interp1d(dos1tmp, dosd_tmp, kind='cubic')
        interpolation_t = interp1d(dos1tmp, dost_tmp, kind='cubic')
        
        dos1 = np.linspace(min(dos1tmp), max(dos1tmp), 100000)
        doss = interpolation_s(dos1)
        dosp = interpolation_p(dos1)
        dosd = interpolation_d(dos1)
        dost = interpolation_t(dos1)
        
        atoms_dos_interp[atom] = {
            'dos1': dos1,
            'doss': doss,
            'dosp': dosp,
            'dosd': dosd,
            'dost': dost
        }
    
    # Interpolation TDOS
    doscol1 = np.linspace(min(doscol1tmp), max(doscol1tmp), 100000)
    doscol2 = interpolationcol2(doscol1)
    
    # Création du graphique
    fig, ax = plt.subplots(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
    
    # Subplot 1: Structure de bandes
    plt.subplot(gs[0])
    plt.plot(colonne1, colonne2, color="gray", zorder=1)
    
    # Tracé des contributions pour chaque atome
    for i, atom in enumerate(atoms):
        atom_data = atoms_data[atom]
        typeorb = typeorbs[i]
        color = colors[i]
        
        for j, orb_type in enumerate(typeorb):
            if orb_type == "s":
                plt.scatter(atom_data['raw1'], atom_data['raw2'], 
                          s=atom_data['raws'], facecolors='none', alpha=1.0, 
                          color=color[j], zorder=2, label=f'{atom}-s')
            elif orb_type == "p":
                plt.scatter(atom_data['raw1'], atom_data['raw2'], 
                          s=atom_data['rawp'], facecolors='none', alpha=1.0, 
                          color=color[j], zorder=2, label=f'{atom}-p')
            elif orb_type == "d":
                plt.scatter(atom_data['raw1'], atom_data['raw2'], 
                          s=atom_data['rawd'], facecolors='none', alpha=1.0, 
                          color=color[j], zorder=2, label=f'{atom}-d')
            elif orb_type == "t":
                plt.scatter(atom_data['raw1'], atom_data['raw2'], 
                          s=atom_data['rawt'], facecolors='none', alpha=1.0, 
                          color=color[j], zorder=2, label=f'{atom}')
    
    plt.axhline(y=0, color="black", linestyle="dashed")
    
    # Lignes verticales pour k-path
    for coord_x in coordonnees_x:
        plt.axvline(x=coord_x, color='black', zorder=3)
    
    plt.xticks(coordonnees_x, etiquettes, rotation=xrot)
    plt.xlim(min(colonne1), max(colonne1) + 0.001)
    plt.ylim(emin, emax)
    plt.ylabel("Energy (eV)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    
    # Subplot 2: DOS
    plt.subplot(gs[1])
    plt.plot(doscol2, doscol1, color="black", zorder=1, label="TDOS")
    plt.fill_between(doscol2, doscol1, color='gray', alpha=0.8)
    
    # Tracé des DOS pour chaque atome
    for i, atom in enumerate(atoms):
        dos_data = atoms_dos_interp[atom]
        typeorb = typeorbs[i]
        color = colors[i]
        
        for j, orb_type in enumerate(typeorb):
            if orb_type == "s":
                plt.plot(dos_data['doss'], dos_data['dos1'], 
                        color=color[j], zorder=2, label=f'{atom}-s')
            elif orb_type == "p":
                plt.plot(dos_data['dosp'], dos_data['dos1'], 
                        color=color[j], zorder=2, label=f'{atom}-p')
            elif orb_type == "d":
                plt.plot(dos_data['dosd'], dos_data['dos1'], 
                        color=color[j], zorder=2, label=f'{atom}-d')
            elif orb_type == "t":
                plt.plot(dos_data['dost'], dos_data['dos1'], 
                        color=color[j], zorder=2, label=f'{atom}')
    
    plt.axhline(y=0, color="black", linestyle="dashed")
    
    # Calcul de la limite x pour DOS
    maxx = 0
    for i in range(len(doscol1)):
        if -8 <= doscol1[i] <= 5:
            if doscol2[i] > maxx:
                maxx = doscol2[i]
    
    plt.xlim(0, maxx + 1)
    plt.ylim(emin, emax)
    plt.xlabel("DOS (a. u.)", fontsize=fsize)
    ticks = plt.gca().get_xticks()
    filtered_ticks = [ticks[0]]
    for t in ticks[1:]:
        if abs(t - filtered_ticks[-1]) > 0.1:
            filtered_ticks.append(t)
    plt.gca().set_xticks(filtered_ticks)
    plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    plt.gca().set_ylabel("")
    plt.gca().set_yticks([])
    
    # Finalisation
    plt.suptitle(title, y=0.98, fontsize=fsize)
    plt.legend(loc="upper right", fontsize=fsize, bbox_to_anchor=(xanch, yanch), frameon=False)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)
    fig.text(0.01, 0.95, labelfig, fontsize=22)
    plt.subplots_adjust(top=0.93, bottom=0.11, left=0.12, right=0.98, wspace=0.15)
    
    # Sauvegarde
    filename = "".join(atoms) + "bandplot."+pformat
    plt.savefig(filename, format=pformat, dpi=dpi)
#    plt.show()
