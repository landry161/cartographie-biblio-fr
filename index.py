import pdb
import duckdb
import csv
import os
import folium
from folium import plugins
import pandas as pd
import requests
import webbrowser

#Téléchargement du Fichier
def downloadCSVFile():
	url="https://www.data.gouv.fr/fr/datasets/adresses-des-bibliotheques-publiques-2/#/resources/806a8aa1-952f-404d-9857-3f27b7c0ca86"
	files=requests.get("https://www.data.gouv.fr/fr/datasets/r/806a8aa1-952f-404d-9857-3f27b7c0ca86").content
	with open("bibliotheques.csv","wb") as file:
		file.write(files)
	print("Téléchargement du fichier CSV terminé")
	launchHTMLFile()

#On vérifie si le fichier existe
def checkIfExistingFile(fileName):
	checkFile=os.path.isfile(fileName)
	if checkFile==False:
		print("Téléchargement en cours...")
		downloadCSVFile()
	else:
		print("Fichier déjà téléchargé")
		launchHTMLFile()

def launchHTMLFile():
	print("Exécution du fichier html")
	map=folium.Map(location=(46.539758,2.430331),zoom_start=6)
	fg=folium.plugins.MarkerCluster(control=False)
	map.add_child(fg)
	query=duckdb.sql("SELECT region,latitude,longitude,nom_de_l_etablissement,adresse,departement,ville,code_insee_commune FROM bibliotheques.csv").fetchall()
	regions=duckdb.sql("SELECT DISTINCT(region) FROM bibliotheques.csv").fetchall()

	for reg in range(0,len(regions)):
		region=folium.plugins.FeatureGroupSubGroup(fg,regions[reg][0])
		for q in range(0,len(query)):
			if (regions[reg][0]==query[q][0]) and (isinstance(query[q][1],float)==True):
				latitude=query[q][1]
				longitude=query[q][2]
				popupValue="<p><b>Nom : "+str(query[q][3])+"</b></p><p><b>Adresse : "+str(query[q][4])+"</b></p> <p><b>Code postal : "+str(query[q][7])+"</b></p> <p><b>Ville : "+str(query[q][6])+"</b></p><p><b>Département : "+str(query[q][5])+"</b></p>"
				folium.Marker([latitude,longitude],tooltip=str(query[q][3]),popup=popupValue).add_to(region)
		map.add_child(region)
	l=folium.LayerControl().add_to(map)
	map.save("index.html")
	webbrowser.open_new_tab("index.html")

#Appel de la fonction
checkIfExistingFile("bibliotheques.csv")