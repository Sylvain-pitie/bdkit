import sys
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import StrMethodFormatter
from matplotlib.ticker import MaxNLocator

def band_generic(atoms, typeorbs, colors, title, labelfig, xanch, yanch, fsize, xrot,
                 emin, emax, dpi, pformat, seuil=0.5, ndos=2000):
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
        seuil: taille minimale d'un marqueur scatter pour être tracé (filtre les
               points à contribution quasi nulle, invisibles mais très lourds en SVG)
        ndos: nombre de points pour l'interpolation des DOS (2000 suffit visuellement,
              100000 rendait le SVG énorme)
    """

    # Important pour SVG : texte conservé en vrai texte éditable (pas de chemins)
    # et marqueurs scatter référencés via <use> (un seul symbole défini, réutilisé)
    if pformat == "svg":
        plt.rcParams['svg.fonttype'] = 'none'

    # Lecture des données de bande principale
    colonne1 = []
    colonne2 = []

    with open("./band/BAND.dat", "r") as fichier:
        lignes = fichier.readlines()

    for ligne in lignes:
        if ligne.startswith('#'):
            continue
        valeurs = ligne.strip().split()
        if len(valeurs) >= 2:
            valeur1, valeur2 = map(float, valeurs[:2])
            colonne1.append(valeur1)
            colonne2.append(valeur2)
        else:
            # Ligne vide entre deux bandes : on insère un NaN pour couper le
            # tracé et éviter les lignes verticales parasites entre bandes
            if colonne1 and not np.isnan(colonne2[-1]):
                colonne1.append(colonne1[-1])
                colonne2.append(np.nan)

    colonne1 = np.array(colonne1)
    colonne2 = np.array(colonne2)

    # Stockage des données projetées pour chaque atome
    atoms_data = {}

    # Lecture des données projetées pour chaque atome
    for atom in atoms:
        nom_fichier = f"./band/PBAND_{atom}.dat"

        # Lecture des données de bande projetées
        donnees = pd.read_csv(nom_fichier, sep=r'\s+',
                             usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                             skiprows=3, comment='#')

        donnees.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4",
                          "Colonne5", "Colonne6", "Colonne7", "Colonne8",
                          "Colonne9", "Colonne10", "Colonne11"]

        # Extraction des coordonnées k et énergies (en numpy pour le filtrage)
        raw1 = donnees["Colonne1"].to_numpy()
        raw2 = donnees["Colonne2"].to_numpy()

        # Calcul des contributions orbitales
        raws = (donnees["Colonne3"] * 10).to_numpy()  # s orbital

        somme_p = (donnees["Colonne4"] + donnees["Colonne5"] + donnees["Colonne6"]) * 10
        rawp = somme_p.to_numpy()  # p orbitals

        somme_d = (donnees["Colonne7"] + donnees["Colonne8"] +
                   donnees["Colonne9"] + donnees["Colonne10"] +
                   donnees["Colonne11"]) * 10
        rawd = somme_d.to_numpy()  # d orbitals

        rawt = raws + rawp + rawd  # total

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
    TDdos = pd.read_csv(tdosfile, sep=r'\s+', usecols=[0, 1],
                       skiprows=1, comment='#')
    TDdos.columns = ["Colonne1", "Colonne2"]
    doscol1tmp = np.array(TDdos["Colonne1"].tolist())
    doscol2tmp = np.array(TDdos["Colonne2"].tolist())

    # PDOS pour chaque atome
    atoms_dos = {}

    for atom in atoms:
        ndosfile = f"./dos/PDOS_{atom}.dat"

        ndos_df = pd.read_csv(ndosfile, sep=r'\s+',
                          usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                          skiprows=1, comment='#')

        ndos_df.columns = ["Colonne1", "Colonne2", "Colonne3", "Colonne4",
                       "Colonne5", "Colonne6", "Colonne7", "Colonne8",
                       "Colonne9", "Colonne10"]

        dos1tmp = ndos_df["Colonne1"].to_numpy()
        doss = ndos_df["Colonne2"].to_numpy()  # s DOS

        dosp = (ndos_df["Colonne3"] + ndos_df["Colonne4"] + ndos_df["Colonne5"]).to_numpy()  # p DOS

        dosd = (ndos_df["Colonne6"] + ndos_df["Colonne7"] +
                ndos_df["Colonne8"] + ndos_df["Colonne9"] + ndos_df["Colonne10"]).to_numpy()  # d DOS

        dost = doss + dosp + dosd  # total DOS

        atoms_dos[atom] = {
            'dos1': dos1tmp,
            'doss': doss,
            'dosp': dosp,
            'dosd': dosd,
            'dost': dost
        }

    # Interpolation TDOS
    # NB: ndos points (défaut 2000) au lieu de 100000 -> SVG ~50x plus léger,
    # rendu strictement identique à l'écran et à l'impression
    interpolationcol2 = interp1d(doscol1tmp, doscol2tmp, kind='cubic')
    doscol1 = np.linspace(doscol1tmp.min(), doscol1tmp.max(), ndos)
    doscol2 = interpolationcol2(doscol1)

    # Interpolation pour chaque atome
    atoms_dos_interp = {}

    for atom in atoms:
        dos_data = atoms_dos[atom]
        dos1tmp = dos_data['dos1']

        dos1 = np.linspace(dos1tmp.min(), dos1tmp.max(), ndos)
        doss = interp1d(dos1tmp, dos_data['doss'], kind='cubic')(dos1)
        dosp = interp1d(dos1tmp, dos_data['dosp'], kind='cubic')(dos1)
        dosd = interp1d(dos1tmp, dos_data['dosd'], kind='cubic')(dos1)
        dost = interp1d(dos1tmp, dos_data['dost'], kind='cubic')(dos1)

        atoms_dos_interp[atom] = {
            'dos1': dos1,
            'doss': doss,
            'dosp': dosp,
            'dosd': dosd,
            'dost': dost
        }

    # Création du graphique
    fig, ax = plt.subplots(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])

    # Subplot 1: Structure de bandes
    plt.subplot(gs[0])
    lignes_bandes, = plt.plot(colonne1, colonne2, color="gray", zorder=1)
    lignes_bandes.set_gid("bandes_grises")  # groupe nommé dans le SVG

    # Marge en énergie pour le filtrage (les marqueurs un peu hors cadre
    # peuvent encore déborder visuellement dans la fenêtre)
    marge = 0.5 * (emax - emin) * 0.05 + 0.3

    # Tracé des contributions pour chaque atome
    for i, atom in enumerate(atoms):
        atom_data = atoms_data[atom]
        typeorb = typeorbs[i]
        color = colors[i]

        k = atom_data['raw1']
        E = atom_data['raw2']
        # Masque énergie : on ne garde que les points dans la fenêtre tracée
        mask_E = (E >= emin - marge) & (E <= emax + marge)

        orb_map = {"s": ('raws', f'{atom}-s'),
                   "p": ('rawp', f'{atom}-p'),
                   "d": ('rawd', f'{atom}-d'),
                   "t": ('rawt', f'{atom}')}

        for j, orb_type in enumerate(typeorb):
            if orb_type not in orb_map:
                continue
            key, lab = orb_map[orb_type]
            taille = atom_data[key]

            # Masque taille : on élimine les marqueurs quasi invisibles
            # (contribution ~0) qui alourdissent énormément le SVG
            mask = mask_E & (taille >= seuil)

            sc = plt.scatter(k[mask], E[mask],
                             s=taille[mask], facecolors='none', alpha=0.5,
                             color=color[j], zorder=2, label=lab)
            # gid -> chaque famille de points devient un groupe nommé,
            # sélectionnable d'un clic dans l'éditeur XML d'Inkscape
            sc.set_gid(f"pband_{lab.replace('-', '_')}")

    plt.axhline(y=0, color="black", linestyle="dashed")

    # Lignes verticales pour k-path
    for coord_x in coordonnees_x:
        plt.axvline(x=coord_x, color='black', zorder=3)

    plt.xticks(coordonnees_x, etiquettes, rotation=xrot)
    plt.xlim(colonne1[~np.isnan(colonne2)].min(), colonne1[~np.isnan(colonne2)].max() + 0.001)
    plt.ylim(emin, emax)
    plt.ylabel("Energy (eV)", fontsize=fsize)
    plt.xticks(fontsize=fsize)
    plt.yticks(fontsize=fsize)

    # Subplot 2: DOS
    plt.subplot(gs[1])
    tdos_line, = plt.plot(doscol2, doscol1, color="black", zorder=1, label="TDOS")
    tdos_line.set_gid("TDOS")
    remplissage = plt.fill_between(doscol2, doscol1, color='gray', alpha=0.8)
    remplissage.set_gid("TDOS_fill")

    # Tracé des DOS pour chaque atome
    for i, atom in enumerate(atoms):
        dos_data = atoms_dos_interp[atom]
        typeorb = typeorbs[i]
        color = colors[i]

        orb_map = {"s": ('doss', f'{atom}-s'),
                   "p": ('dosp', f'{atom}-p'),
                   "d": ('dosd', f'{atom}-d'),
                   "t": ('dost', f'{atom}')}

        for j, orb_type in enumerate(typeorb):
            if orb_type not in orb_map:
                continue
            key, lab = orb_map[orb_type]
            ligne, = plt.plot(dos_data[key], dos_data['dos1'],
                              color=color[j], zorder=2, label=lab)
            ligne.set_gid(f"pdos_{lab.replace('-', '_')}")

    plt.axhline(y=0, color="black", linestyle="dashed")

    # Calcul de la limite x pour DOS (vectorisé)
    fenetre = (doscol1 >= -8) & (doscol1 <= 5)
    maxx = doscol2[fenetre].max() if fenetre.any() else doscol2.max()

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
    filename = "".join(atoms) + "bandplot." + pformat
    if pformat == "svg":
        plt.savefig(filename, format=pformat, bbox_inches='tight')
    else:
        plt.savefig(filename, format=pformat, dpi=dpi)
#    plt.show()
