import pathlib
import yaml

_PARTICIPANTS_FOLDER = pathlib.Path("metadata/participants")
_CONVERSATIONS_FOLDER = pathlib.Path("metadata/conversations")

_EDUCATION_LEVELS = set("Primaria", "Medie inferiori", "Medie superiori", "Laurea", "PhD")
_ISTAT_CATEGORIES = set("STDUIO", "PENSIONE", "LEGISLATORI, IMPRENDITORI E ALTA DIRIGENZA",
						"PROFESSIONI INTELLETTUALI, SCIENTIFICHE E DI ELEVATA SPECIALIZZAZIONE",
						"PROFESSIONI TECNICHE",
						"PROFESSIONI ESECUTIVE NEL LAVORO D'UFFICIO",
						"PROFESSIONI QUALIFICATE NELLE ATTIVITÀ COMMERCIALI E NEI SERVIZI",
						"ARTIGIANI, OPERAI SPECIALIZZATI E AGRICOLTORI",
						"CONDUTTORI DI IMPIANTI, OPERAI DI MACCHINARI FISSI E MOBILI E CONDUCENTI DI VEICOLI",
						"PROFESSIONI NON QUALIFICATE",
						"FORZE ARMATE")
_ITALIAN_REGIONS = set("Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
					   "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", "Molise",
					   "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", "Trentino-Alto Adige",
					   "Valle d'Aosta", "Veneto")

_GENDER = set("F", "M")

participants = {}

for participant_filename in _PARTICIPANTS_FOLDER.glob("*.yaml"):
	print(participant_filename)
	with open(participant_filename) as stream:
		try:
			data = yaml.safe_load(stream)

			assert(data["Region"] in _ITALIAN_REGIONS)

		except yaml.YAMLError as exc:
			print(exc)
			exit()