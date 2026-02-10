import streamlit as st
import numpy as np
import pandas as pd
from formulaire import formular

st.title("OptiSolve")
st.markdown("""**OptiSolve** est une application dédiée à la
            résolution de problème d'optimisation linéaire avec la méthode de **Simplexe**. 
            Conçue pour traiter exclusivement des problèmes 
            de maximisation, elle offre une interface conviviale 
            pour modéliser vos équations sous forme de systèmes 
            d'inégalités et de fonctions objectif.""")
st.subheader("Format d'équation résolu")
st.write("1. **Fonction objectif à maximiser**")
st.latex(r"Z = c_1 x_1 + c_2 x_2 + \cdots + c_n x_n")
st.write("2. **Sujets à des contraintes linéaire**")
st.latex(r"""\begin{align*}
		a_{11} x_1 + a_{12} x_2 + \cdots + a_{1n} &\leq b_1\\
		a_{21} x_1 + a_{22} x_2 + \cdots + a_{2n} & \leq b_2\\
		 &  \\
		a_{n1} x_1 + a_{n2} x_2 + \cdots + a_{nn} & \leq b_n\\
      x_1, x_2, \cdots , x_n \geq 0 
	\end{align*} """)

# Test
st.subheader("Faites une résolution de problèmes d'optimisation linéaire avec l'algorithme du simplexe")

# Collecte des informations
nbr_var = st.number_input("Entrez le nombre de variables:", min_value=1, step=1)
nbr_contrainte = st.number_input("Entrez le nombre de contraintes:", min_value=1, step=1)

# Collecte des coefficients de la fonction objective
st.subheader("Fonction objective Z (Coefficient de Z)")
z = []
for i in range(nbr_var):
    if i == 0:
        tmp = st.number_input(f"Entrez le coefficient de la {i+1}-ère variable:", step=0.1)
    else:
        tmp = st.number_input(f"Entrez le coefficient de la {i+1}-ème variable:", step=0.1)
    z.append(tmp)

# Remplissage de la matrice A
st.subheader("Matrice A (coefficients des contraintes)")
A = np.zeros((nbr_contrainte, nbr_var))
for i in range(nbr_contrainte):
    for j in range(nbr_var):
        A[i][j] = st.number_input(f"Entrez l'élément de la matrice A à la position ({i+1},{j+1}):", step=0.1)

# Remplissage de la matrice b
st.subheader("Matrice b (termes constants des contraintes)")
b = np.zeros((nbr_contrainte, 1))
for i in range(nbr_contrainte):
    if i == 0:
        b[i][0] = st.number_input(f"Entrez l'élément de la matrice b à la {i+1}-ère position:", step=0.1)
    else:
        b[i][0] = st.number_input(f"Entrez l'élément de la matrice b à la {i+1}-ème position:", step=0.1)

# Nomenclature des variables
x = [f"x{i}" for i in range(nbr_var)]
t = [f"t{i}" for i in range(nbr_contrainte)]
Z = ["Z"] + z + [0] * (nbr_contrainte + 1)

# Création du tableau du simplexe
tableau = pd.DataFrame(
    {"Hors base/Base": t} |
    {x[i]: A[:, i] for i in range(nbr_var)} |
    {t[i]: np.eye(nbr_contrainte)[:, i] for i in range(nbr_contrainte)} |
    {"b": b[:, 0]}
)
tableau.loc[len(tableau)] = Z

# Affichage du tableau
st.subheader("Tableau du simplexe")
table_show = tableau.copy()
table_show.set_index("Hors base/Base", inplace=True)
st.dataframe(table_show)

# Bouton pour lancer l'algorithme du simplexe
if st.button("Lancez l'algorithme"):
    # itération
      iteration = 0

      # Critere d'arret
      stop = True

      while(stop == True):
            def show_solve(x, tableau):
                  # Affichage de la solution
                  value_sol = []
                  for i in x:
                        verify = False
                        for j in range(len(list(tableau["Hors base/Base"]))):
                              if i == list(tableau["Hors base/Base"])[j]:
                                    verify = True
                                    value_sol.append(list(tableau["b"])[j])
                                    break
                        if verify == False:
                              value_sol.append(0)

                  st.markdown(f"**La solution: {x} = {value_sol}**")
                  st.markdown(f"Et **la fonction objectif Z = {-list(tableau["b"])[len(list(tableau["b"]))-1]}**")
            
            epsilon_all = 0
            epsilon_all1 = 0
            epsilon_all2 = 0
            
            # Condition d'arret1
            for i in tableau.loc[len(tableau)-1][1:len(tableau.loc[len(tableau)-1])-1]:
                  if (i <= 0):
                        epsilon_all = epsilon_all + 1
                  else:
                        iteration = 1 + iteration
                        break
            
            if(epsilon_all == len(tableau.loc[len(tableau)-1][1:len(tableau.loc[len(tableau)-1])-1])):
            #         print(f"\n\nNombre d'itération: n = {iteration}")
                  for i in tableau.loc[len(tableau)-1][len(x)+1:len(tableau.loc[len(tableau)-1])-1]:
                        if (i == 0):
                              epsilon_all1 = epsilon_all1 + 1
                        else:
                              break
                  for i in tableau.loc[len(tableau)-1][1:len(x)+1]:
                        if (i != 0):
                              epsilon_all2 = epsilon_all2 + 1
                        else:
                              break
                  if( epsilon_all1 == len(tableau.loc[len(tableau)-1][len(x)+1:len(tableau.loc[len(tableau)-1])-1]) and epsilon_all2 == len(tableau.loc[len(tableau)-1][1:len(x)+1])):
                        st.write("Il y a une infinité de solutions. La ligne de niveau la plus éloignée de l'origine est confondue à tout un segment de la frontière du polyèdre convexe. Soit:")
                        show_solve(x, tableau)
                  else:
                        st.write("La solution est unique. La ligne de niveau la plus éloigné de l'origine est tangente en un seul sommet du polyèddre convexe.")
                        show_solve(x, tableau)
                  stop = False
                  break
                  
            # Recherche de la variable entrant et de sa position
            for i in range(len(tableau.loc[len(tableau)-1])):
                  if(max(tableau.loc[len(tableau)-1][1:len(tableau.loc[len(tableau)-1])-1]) == tableau.loc[len(tableau)-1][i] ):
                        pos_entrant = i
                        break
            for i in list(tableau.columns):
                  if(i == tableau.columns[pos_entrant]):
                        var_entrant = tableau.columns[pos_entrant]
                        break
            
            # Condition d'arret2
            pos = 0
            for i in range(len(tableau)-1):
                  if( tableau[var_entrant][i] <= 0 ):
                        pos = pos + 1
                  else:
                        break
            if(pos == len(tableau)-1 ):
                  st.write("Le problème n'admet pas de solutions optimale finie")
                  stop = False
                  break
            
            # Varible sortant et sa position
            R = (tableau["b"][0:len(tableau)-1])/tableau[var_entrant][0:len(tableau)-1]
            for i in range(len(R)):
                  if( R[i] == min(R)):
                        pos_sortant = i
                        break
            var_sortant = tableau["Hors base/Base"][pos_sortant]

            # Operation baser sur le pivaut
            pivaut = tableau.loc[pos_sortant][var_entrant]
            tableau.loc[pos_sortant] = [var_entrant] + list(np.array(tableau.loc[pos_sortant][1:len(tableau.columns)])/pivaut)

            # a partir de la ligne sortant, operation sur le tableau par le pivau
            for i in range(len(tableau)):
                  if(i != pos_sortant):
                        tableau.loc[i] = [tableau.loc[i]["Hors base/Base"]] + list(np.array(tableau.loc[i][1:len(tableau.columns)]) - (tableau.loc[i][var_entrant])*np.array(tableau.loc[pos_sortant][1:len(tableau.columns)]))

            # Affichage du tableau
            table_show = tableau.copy()
            table_show.set_index("Hors base/Base", inplace=True)
            st.markdown(f"**{var_sortant} sort de la base et {var_entrant} entre dans la base**")
            st.dataframe(table_show)

st.markdown("""<hr>""", unsafe_allow_html=True)

# importation formulaire 
formular()

# pied de page           
st.markdown("""
    <hr>
    <center><small>Copyright © 2025 Expéra AKAKPO. Tous droits réservés.</small></center>
""", unsafe_allow_html=True)
