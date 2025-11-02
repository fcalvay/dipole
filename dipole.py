#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 19:51:57 2025

@author: florentcalvayrac
"""

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Source non idéale & dipôles", layout="wide")

# -----------------------------
# Dipôles : U_d(I)
# -----------------------------
def v_resistance(I, R):
    return I * R

def v_lampe(I, R, a=0.5):
    return I * (R * (1 + a * I**2))

def v_moteur(I, R, k=0.2):
    return I * R + k * I

st.title("Générateur non idéal + Dipôles")
st.write("Source de Thévenin : $U = E - rI$. On affiche en même temps la **courbe U(I)** et la **puissance P(I)** du dipôle.")

with st.sidebar:
    st.header("Paramètres")
    E = st.slider("E (V)", 1.0, 48.0, 12.0, 0.5)
    r = st.slider("r (Ω)", 0.05, 10.0, 1.0, 0.05)
    dipole = st.selectbox("Dipôle", ["Résistance", "Lampe", "Moteur"])
    R = st.slider("R base (Ω)", 0.1, 100.0, 10.0, 0.1)
    a_lampe = st.slider("a (lampe)", 0.0, 2.0, 0.5, 0.05)
    k_moteur = st.slider("k (moteur)", 0.0, 5.0, 0.2, 0.05)
    N = st.slider("Points de calcul", 200, 2000, 600, 50)

I_max = max(E / r, 1e-6)
I = np.linspace(0.0, I_max, N)

if dipole == "Résistance":
    Vd = v_resistance(I, R)
elif dipole == "Lampe":
    Vd = v_lampe(I, R, a=a_lampe)
else:
    Vd = v_moteur(I, R, k=k_moteur)

Vg = E - r * I
idx = int(np.argmin(np.abs(Vd - Vg)))
I_star = float(I[idx])
U_star = float(Vd[idx])
P_dipole_star = I_star * U_star
P_pertes_source = (I_star**2) * r
P_entree = I_star * E
eta = P_dipole_star / P_entree if P_entree > 0 else float("nan")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(6, 4.5))
    ax1.plot(I, Vd, label="Dipôle : U_d(I)")
    ax1.plot(I, Vg, label="Générateur : U_g(I)")
    ax1.plot(I_star, U_star, "o", label="Point de fonctionnement")
    ax1.set_xlabel("Courant I (A)")
    ax1.set_ylabel("Tension U (V)")
    ax1.set_title(f"E={E:.2f} V, r={r:.2f} Ω — {dipole}")
    ax1.grid(True); ax1.legend()
    st.pyplot(fig1, clear_figure=True)

with col2:
    Pd = I * Vd
    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
    ax2.plot(I, Pd, label="P_dipôle(I)")
    ax2.plot(I_star, P_dipole_star, "o", label="Au point de fonctionnement")
    ax2.set_xlabel("Courant I (A)")
    ax2.set_ylabel("Puissance P (W)")
    ax2.set_title("Puissance dissipée dans le dipôle")
    ax2.grid(True); ax2.legend()
    st.pyplot(fig2, clear_figure=True)

st.markdown("---")
st.subheader("Valeurs au point de fonctionnement")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("I*", f"{I_star:.4f} A")
c2.metric("U*", f"{U_star:.4f} V")
c3.metric("P_dipôle", f"{P_dipole_star:.4f} W")
c4.metric("P_perdue (r)", f"{P_pertes_source:.4f} W")
c5.metric("Rendement", f"{100*eta:.2f} %")