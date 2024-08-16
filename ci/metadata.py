import csv
import pathlib
import yaml

_PARTICIPANTS_FOLDER = pathlib.Path("metadata/participants")
_CONVERSATIONS_FOLDER = pathlib.Path("metadata/conversations")

_EDUCATION_LEVELS = {"Primaria", "Medie inferiori", "Medie superiori", "Laurea", "PhD"}
_ISTAT_CATEGORIES = {"STUDIO", "PENSIONE", "LEGISLATORI, IMPRENDITORI E ALTA DIRIGENZA",
					"PROFESSIONI INTELLETTUALI, SCIENTIFICHE E DI ELEVATA SPECIALIZZAZIONE",
					"PROFESSIONI TECNICHE",
					"PROFESSIONI ESECUTIVE NEL LAVORO D'UFFICIO",
					"PROFESSIONI QUALIFICATE NELLE ATTIVITÀ COMMERCIALI E NEI SERVIZI",
					"ARTIGIANI, OPERAI SPECIALIZZATI E AGRICOLTORI",
					"CONDUTTORI DI IMPIANTI, OPERAI DI MACCHINARI FISSI E MOBILI E CONDUCENTI DI VEICOLI",
					"PROFESSIONI NON QUALIFICATE",
					"FORZE ARMATE"}
_ITALIAN_REGIONS = {"Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
					"Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", "Molise",
					"Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", "Trentino-Alto Adige",
					"Umbria", "Valle d'Aosta", "Veneto"}
_GENDER = {"F", "M", "O"}
_FACING_CONDITIONS = {"masked", "unmasked"}

participants = {}
fieldnames = []

for participant_filename in _PARTICIPANTS_FOLDER.glob("*.yaml"):
	print(f"Reading file: {participant_filename} ...")
	with open(participant_filename) as stream:
		try:
			participant = yaml.safe_load(stream)

			assert participant["Region"] in _ITALIAN_REGIONS, \
		  			f"Error for participant {participant['Code']}: Region not allowed"
			assert participant["Education level"] in _EDUCATION_LEVELS, \
		  			f"Error for participant {participant['Code']}: Education Level not allowed"
			assert participant["Profession"] in _ISTAT_CATEGORIES, \
		  			f"Error for participant {participant['Code']}: Profession not allowed"
			assert participant["Gender"] in _GENDER, \
		  			f"Error for participant {participant['Code']}: Gender not allowed"

			participant["Conversations"] = []
			fieldnames = list(participant.keys())
			participants[participant["Code"]] = participant

		except yaml.YAMLError as exc:
			print(exc)
			exit()

for conversation_filename in _CONVERSATIONS_FOLDER.glob("*.yaml"):
	print(f"Reading file: {conversation_filename} ...")

	with open(conversation_filename) as stream:
		try:
			conversation = yaml.safe_load(stream)

			assert conversation["Facing"] in _FACING_CONDITIONS, \
		  			f"Error for conversation {conversation['Facing']}: Facing value not allowed"

			conv_participants = conversation["Participants"]

			for participant in conv_participants:

				assert participant in participants, \
					f"Participant {participant} found in conversation {conversation['Code']} but was never defined"

				participants[participant]["Conversations"].append(conversation["Code"])


		except yaml.YAMLError as exc:
			print(exc)
			exit()


for participant in participants:
	participants[participant]["Conversations"] = ", ".join(participants[participant]["Conversations"])

with open(pathlib.Path("metadata/metadata-recap.csv"), "w") as fout:
	writer = csv.DictWriter(fout, fieldnames=fieldnames)
	writer.writeheader()

	for participant in participants:
		writer.writerow(participants[participant])