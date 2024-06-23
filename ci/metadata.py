import pathlib
import yaml

_PARTICIPANTS_FOLDER = pathlib.Path("metadata/participants")
_CONVERSATIONS_FOLDER = pathlib.Path("metadata/conversations")


for participant_filename in _PARTICIPANTS_FOLDER.glob("*.yaml"):
	print(participant_filename)
	with open(participant_filename) as stream:
		try:
			data = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			exit()


	print(data)