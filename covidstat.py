import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse
from datetime import datetime, timedelta

class CmdStat():
    def __init__(self, covid_data):
        self.data = self.charger_fichier_csv(covid_data)

    def charger_fichier_csv(self, nom_fichier):
        donnees = []
        with open(nom_fichier, newline='') as f:
            lecteur = csv.reader(f, delimiter=',', quotechar='"')
            for ligne in lecteur:
                donnees.append(ligne)
        return donnees

    def extraire_donnees(self, info, location=None):
        entetes = self.data[0]
        index_info = entetes.index(info)
        donnees = []
        for ligne in self.data[1:]:
            if location is None or ligne[1] in location:
                donnees.append(int(ligne[index_info]))
        return donnees

    def extraire_donnees_par_date(self, info, date_debut, date_fin, location=None):
        entetes = self.data[0]
        index_info = entetes.index(info)
        donnees = []
        for ligne in self.data[1:]:
            if location is None or ligne[1] in location:
                date = datetime.strptime(ligne[0], '%Y-%m-%d')
                if date_debut <= date <= date_fin:
                    donnees.append(int(ligne[index_info]))
        return donnees

    def extraire_donnees_par_periode(self, info, periode, location=None):
        entetes = self.data[0]
        index_info = entetes.index(info)
        donnees = []
        for ligne in self.data[1:]:
            if location is None or ligne[1] in location:
                date = datetime.strptime(ligne[0], '%Y-%m-%d')
                if date >= periode[0] and date <= periode[1]:
                    donnees.append(int(ligne[index_info]))
        return donnees

    def extraire_donnees_par_aggregation(self, info, aggregation, location=None):
        entetes = self.data[0]
        index_info = entetes.index(info)
        donnees = []
        for ligne in self.data[1:]:
            if location is None or ligne[1] in location:
                donnees.append(int(ligne[index_info]))
        if aggregation == 'max':
            return max(donnees)
        elif aggregation == 'min':
            return min(donnees)
        elif aggregation == 'avg':
            return sum(donnees) / len(donnees)

    def afficher_histogramme(self, info, periode=None, location=None):
        donnees = self.extraire_donnees_par_date(info, periode[0], periode[1], location)
        plt.hist(donnees, bins=20)
        plt.title(f"Histogramme de {info}")
        plt.xlabel("Valeur")
        plt.ylabel("Fréquence")
        plt.show()

    def afficher_graphique(self, info, location=None):
        donnees = self.extraire_donnees(info, location)
        plt.plot(donnees)
        plt.title(f"Graphique de {info}")
        plt.xlabel("Temps")
        plt.ylabel("Valeur")
        plt.show()

    def terminal(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--info", choices=['total_cases', 'total_deaths', 'total_icu_patients', 'total_hosp_patients', 'total_tests', 'total_positives', 'new_cases', 'new_deaths', 'new_icu_patients', 'new_hosp_patients', 'new_tests', 'new_positives'], help="Information à afficher.")
        parser.add_argument("--hist", choices=['new_cases', 'new_deaths', 'new_icu_patients', 'new_hosp_patients', 'new_tests', 'new_positives'], help="Afficher un histogramme.")
        parser.add_argument("--plt", choices=['total_cases', 'total_deaths', 'total_icu_patients', 'total_hosp_patients', 'total_tests', 'total_positives', 'new_cases', 'new_deaths', 'new_icu_patients', 'new_hosp_patients', 'new_tests', 'new_positives'], help="Afficher un graphique.")
        parser.add_argument("--aggregation", choices=['max', 'min', 'avg'], help="Type d'agrégation.")
        parser.add_argument("--location", nargs='+', help="Localisation.")
        parser.add_argument("--time", nargs=2, type=int, help="Période de temps.")
        parser.add_argument("value", type=int, help="Valeur.")
        args = parser.parse_args()

        if args.info:
            if args.aggregation:
                resultat = self.extraire_donnees_par_aggregation(args.info, args.aggregation, args.location)
                print(f"{args.aggregation} {args.info}: {resultat}")
            elif args.time:
                date_fin = datetime.today() - timedelta(days=args.time[0])
                date_debut = datetime.today() - timedelta(days=args.time[1])
                donnees = self.extraire_donnees_par_date(args.info, date_debut, date_fin, args.location)
                print(f"{args.info} au cours des {args.time[0]} derniers jours: {donnees}")
            else:
                donnees = self.extraire_donnees(args.info, args.location)
                print(f"{args.info}: {donnees}")
        elif args.hist:
            periode = (datetime.today() - timedelta(days=args.time[0]), datetime.today())
            self.afficher_histogramme(args.hist, periode, args.location)
        elif args.plt:
            self.afficher_graphique(args.plt, args.location)