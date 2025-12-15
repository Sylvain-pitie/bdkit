#!/usr/bin/env python3
"""
BDkit2.0 — Plot band structure and DOS for any compound.

Usage example:
    ./BDkit2.0 2 "Pb,O" "s,p;d" "blue,red;green" -t "PbO Bands" -lf "(a)"

see: https://github.com/Sylvain-pitie/bdkit

Author: Sylvain Pitie

Updated 12/10/2025 by Morgan Redington
"""

import sys
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib.ticker import StrMethodFormatter
import argparse


# ==========================================================
# ================   BAND + DOS UTILITIES   ================
# ==========================================================

def read_band_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing band data file: {filepath}")
    k_points, energies = np.loadtxt(filepath, unpack=True, comments='#')
    return k_points, energies


def read_pband(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing projected band data file: {filepath}")

    df = pd.read_csv(filepath, delim_whitespace=True, skiprows=3, comment='#')
    df.columns = [f"C{i}" for i in range(1, len(df.columns) + 1)]

    k_points = df["C1"].to_numpy()
    energies = df["C2"].to_numpy()

    s = df["C3"] * 10
    p = (df["C4"] + df["C5"] + df["C6"]) * 10
    d = (df["C7"] + df["C8"] + df["C9"] + df["C10"] + df["C11"]) * 10
    total = s + p + d

    return {"k": k_points, "E": energies, "s": s, "p": p, "d": d, "t": total}


def read_k_labels(filepath):
    labels, coords = [], []
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing KLABELS file: {filepath}")

    with open(filepath) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            try:
                coord = float(parts[1])
            except ValueError:
                continue
            labels.append(parts[0])
            coords.append(coord)

    replacements = {
        "GAMMA": "$\\Gamma$", "DELTA": "$\\Delta$", "SIGMA": "$\\Sigma$",
        "_0": "$_0$", "_1": "$_1$", "_2": "$_2$", "+": " ", "-": " "
    }
    for old, new in replacements.items():
        labels = [lbl.replace(old, new) for lbl in labels]

    return labels, coords


def read_dos(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing TDOS file: {filepath}")
    df = pd.read_csv(filepath, delim_whitespace=True, skiprows=1, comment='#')
    df.columns = ["E", "DOS"]
    return df["E"].to_numpy(), df["DOS"].to_numpy()


def read_pdos(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing PDOS file: {filepath}")
    df = pd.read_csv(filepath, delim_whitespace=True, skiprows=1, comment='#')
    df.columns = [f"C{i}" for i in range(1, len(df.columns) + 1)]

    E = df["C1"].to_numpy()
    s = df["C2"]
    p = (df["C3"] + df["C4"] + df["C5"])
    d = (df["C6"] + df["C7"] + df["C8"] + df["C9"] + df["C10"])
    total = s + p + d
    return {"E": E, "s": s, "p": p, "d": d, "t": total}


def interpolate_dos(dos_dict, num_points=100000):
    E_lin = np.linspace(min(dos_dict["E"]), max(dos_dict["E"]), num_points)
    interp = {
        orb: interp1d(dos_dict["E"], dos_dict[orb], kind='cubic')(E_lin)
        for orb in ["s", "p", "d", "t"]
    }
    interp["E"] = E_lin
    return interp


def band_generic(
    atoms, typeorbs, colors,
    title, labelfig,
    xanch, yanch,
    fsize=14, xrot=0,
    emin=-5, emax=5,
    dpi=300, pformat="png",
    band_dir="./band", dos_dir="./dos"
):

    # --- Load band data ---
    k_points, energies = read_band_data(os.path.join(band_dir, "BAND.dat"))
    k_labels, k_coords = read_k_labels(os.path.join(band_dir, "KLABELS"))
    atom_band_data = {
        atom: read_pband(os.path.join(band_dir, f"PBAND_{atom}.dat"))
        for atom in atoms
    }

    # --- Load DOS data ---
    E_tdos, tdos = read_dos(os.path.join(dos_dir, "TDOS.dat"))
    atom_dos_data = {
        atom: interpolate_dos(read_pdos(os.path.join(dos_dir, f"PDOS_{atom}.dat")))
        for atom in atoms
    }

    # --- Plot setup ---
    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
    plt.subplots_adjust(top=0.93, bottom=0.11, left=0.12, right=0.98, wspace=0.16)

    # --- Band structure ---
    ax1 = plt.subplot(gs[0])

    # Plot the bands in black
    ax1.plot(k_points, energies, color="black", zorder=1)

    # Plot ALL projected scatter points in black as well
    for atom, orbs, cols in zip(atoms, typeorbs, colors):
        data = atom_band_data[atom]
        for orb in orbs:
            ax1.scatter(
                data["k"], data["E"],
                s=data[orb],
                facecolors='none',
                color="black",
                alpha=1.0
             )

    for x in k_coords:
        ax1.axvline(x=x, color="black", lw=0.8)
    ax1.axhline(y=0, color="black", ls="--")
    ax1.set_ylim(emin, emax)
    ax1.set_xlim(min(k_points), max(k_points))
    ax1.set_ylabel("Energy (eV)", fontsize=fsize)
    ax1.set_xticks(k_coords)
    ax1.set_xticklabels(k_labels, rotation=xrot, fontsize=fsize)
    ax1.tick_params(labelsize=fsize)

    # --- DOS subplot ---
    ax2 = plt.subplot(gs[1])
    ax2.plot(tdos, E_tdos, color="black", label="TDOS")
    ax2.fill_between(tdos, E_tdos, color="gray", alpha=0.4)

    # ✅ MODIFIED LEGEND LOGIC HERE
    for atom, orbs, cols in zip(atoms, typeorbs, colors):
        data = atom_dos_data[atom]
        species_only = set(orbs) == {"t"}

        for orb, c in zip(orbs, cols):
            label = atom if species_only else f"{atom}-{orb}"
            ax2.plot(data[orb], data["E"], color=c, label=label)

    ax2.axhline(y=0, color="black", ls="--")
    ax2.set_ylim(emin, emax)
    ax2.set_xlabel("DOS (a.u.)", fontsize=fsize)
    ax2.set_yticks([])
    ax2.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    ax2.legend(fontsize=fsize - 2, loc="upper right",
               bbox_to_anchor=(xanch, yanch), frameon=False)

    plt.suptitle(title, fontsize=fsize)
    fig.text(0.01, 0.95, labelfig, fontsize=fsize + 6)

    outname = f"{''.join(atoms)}_bandplot.{pformat}"
    plt.savefig(outname, dpi=dpi, format=pformat)
    print(f"✅ Figure saved as: {outname}")


# ==========================================================
# =====================   MAIN SCRIPT   =====================
# ==========================================================

def main():
    parser = argparse.ArgumentParser(prog='BDkit2.0')
    parser.add_argument("kindatm", type=int)
    parser.add_argument("typeatm", type=str)
    parser.add_argument("typeorb", type=str)
    parser.add_argument("colors", type=str)
    parser.add_argument("-t", "--title", type=str, default="")
    parser.add_argument("-lf", "--labelfig", type=str, default="")
    parser.add_argument("-xl", "--xlegend", type=float, default=1.1)
    parser.add_argument("-yl", "--ylegend", type=float, default=0.95)
    parser.add_argument("-fsize", "--fontsize", type=int, default=19)
    parser.add_argument("-xrot", "--xrotation", type=int, default=0)
    parser.add_argument("-emin", "--emin", type=float, default=-8.0)
    parser.add_argument("-emax", "--emax", type=float, default=6.0)
    parser.add_argument("-dpi", "--dpi", type=int, default=400)
    parser.add_argument("-pformat", "--pformat", type=str, default='png')
    args = parser.parse_args()

    typeatm = args.typeatm.split(',')
    typeorb = [o.split(',') for o in args.typeorb.split(';')]
    colors = [c.split(',') for c in args.colors.split(';')]

    if len(typeatm) != args.kindatm:
        sys.exit("❌ Atom count mismatch")
    if len(typeorb) != args.kindatm:
        sys.exit("❌ Orbital group mismatch")
    if len(colors) != args.kindatm:
        sys.exit("❌ Color group mismatch")

    for i in range(args.kindatm):
        if len(typeorb[i]) != len(colors[i]):
            sys.exit(f"❌ Orbital/color mismatch for atom {typeatm[i]}")

    band_generic(
        atoms=typeatm,
        typeorbs=typeorb,
        colors=colors,
        title=args.title,
        labelfig=args.labelfig,
        xanch=args.xlegend,
        yanch=args.ylegend,
        fsize=args.fontsize,
        xrot=args.xrotation,
        emin=args.emin,
        emax=args.emax,
        dpi=args.dpi,
        pformat=args.pformat
    )


if __name__ == "__main__":
    main()
