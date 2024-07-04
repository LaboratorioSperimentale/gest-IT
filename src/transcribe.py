import csv
import re

from speach import elan
from conllu.models import TokenList, Token


										#TENERE------ , Intonazione debolmente ascendente
										#TENERE------ . Intonazione discendente


										#TENERE------ >ciao< Pronuncia più rapida
										#TENERE------ <ciao> Pronuncia più lenta
										#TENERE------ : Suono prolungato
										#TENERE------ [ciao] Sovrapposizione tra parlanti
#TENERE------ (.) Pausa breve

											# ((ride)) Comportamento non verbale
											# (ciao) sequenza di difficile comprensione (ipotesi del trascrittore)

#TENERE------ = Unità legate prosodicamente
#TENERE------ xxx sequenza non comprensibile (idealmente, ad ogni x corrisponde una sillaba)
											#TENERE------ °ciao° Volume più basso
											#TENERE------ CIAO Volume più alto

def pipeline_ortography(text):
	return text

def pipeline_whisper(text):
	return text

def annotate(text, start, end):

	ret = []

	# print(text)
	text = re.sub(r" ?\(\.\) ?", "@", text, count=10)
	text = re.sub(r">([^<]+)<", r">\g<1>>", text, count=10)
	text = re.sub(r"<([^<]+)>", r"<\g<1><", text, count=10)

	# ISSUE: ((ride)) alone?
	matches = re.split(r" ?(\(\([^\)]*\)\)) ?", text)
	metadata = [re.fullmatch(r" ?\(\(([^\)]*)\)\) ?", x) for x in matches]
	new_matches = []
	new_metadata = []

	for x, y in zip(matches, metadata):
		if y is None:
			new_matches.append(x)
			new_metadata.append("")
		else:
			if len(new_matches)>0:
				new_metadata[-1] = y[0][2:-2]

	ret = []
	for substring, tag in zip(new_matches, new_metadata):
		tag = "_".join(tag.split(" "))

		annotated_chars = []
		annotations = []
		# print(substring)
		# input()

		for char in substring:
			if char == "(":
				annotated_chars.append("")
				annotations.append("Guess-B")
			elif char == ")":
				annotated_chars.append("")
				annotations.append("Guess-E")
			elif char == "[":
				annotated_chars.append("")
				annotations.append("Overlap-B")
			elif char == "]":
				annotated_chars.append("")
				annotations.append("Overlap-E")
			elif char == " ":
				annotated_chars.append("BREAK")
				annotations.append("")
			elif char == "°":
				annotated_chars.append("LowVolume")
				annotations.append("")
			elif char == "@":
				annotated_chars.append("")
				annotations.append("Pause")
			elif char ==">":
				annotated_chars.append("")
				annotations.append("Fast")
			elif char == "<":
				annotated_chars.append("")
				annotations.append("Slow")
			elif char == ",":
				annotated_chars.append("")
				annotations.append("AscInt")

				annotated_chars.append(",")
				annotations.append("")
			elif char == ".":
				annotated_chars.append("")
				annotations.append("DescInt")

				annotated_chars.append(".")
				annotations.append("")

			elif char == "?":
				annotated_chars.append("")
				annotations.append("Quest")

				annotated_chars.append("?")
				annotations.append("")
			elif char == "=":
				annotated_chars.append("BREAK")
				annotations.append("ProsodicLink")
			elif char.isupper():
				annotated_chars.append(char.lower())
				annotations.append("HighVolume")
			else:
				annotated_chars.append(char)
				annotations.append("")


		annotated_chars.append("BREAK")
		annotations.append("")

		words = []
		annotated_words = []
		start_word = 0
		for i, char in enumerate(annotated_chars):
			if char == "BREAK":
				words.append("".join(annotated_chars[start_word:i]))
				annotated_words.append("|".join([x for x in annotations[start_word:i] if len(x)>0]))
				start_word = i+1

		# print(tag)

		flag_guess = False
		flag_overlap = False
		flag_lowvolume = False
		flag_fast = False
		flag_slow = False

		# print(words)
		# print(annotated_words)

		for w, a in zip(words, annotated_words):
			o = {"text": w,
				"annotations": {}}
			if len(tag)>0:
				o["annotations"]["meta"] = tag

			asplit = a.split("|")

			if "Guess-B" in asplit and "Guess-E" in asplit:
				o["annotations"]["Guess"] = "B"
			elif "Guess-B" in asplit:
				o["annotations"]["Guess"] = "B"
				flag_guess = True
			elif "Guess-E" in asplit:
				o["annotations"]["Guess"] = "I"
				flag_guess=False
			elif flag_guess:
				o["annotations"]["Guess"] = "I"

			if "Overlap-B" in asplit and "Overlap-E" in asplit:
				o["annotations"]["Overlap"] = "B"
			elif "Overlap-B" in asplit:
				o["annotations"]["Overlap"] = "B"
				flag_overlap = True
			elif "Overlap-E" in asplit:
				o["annotations"]["Overlap"] = "I"
				flag_overlap=False
			elif flag_overlap:
				o["annotations"]["Overlap"] = "I"

			if asplit.count("LowVolume")>1:
				o["annotations"]["Volume"] = "Low"
			elif asplit.count("LowVolume") == 1 and flag_lowvolume==False:
				o["annotations"]["Volume"] = "Low"
				flag_lowvolume = True
			elif asplit.count("LowVolume") == 1 and flag_lowvolume==True:
				o["annotations"]["Volume"] = "Low"
				flag_lowvolume = False
			elif flag_lowvolume == True:
				o["annotations"]["Volume"] = "Low"

			if "HighVolume" in asplit:
				o["annotations"]["Volume"] = "High"

			if asplit.count("Fast")>1:
				o["annotations"]["Fast"] = "B"
			elif asplit.count("Fast") == 1 and flag_fast==False:
				o["annotations"]["Fast"] = "B"
				flag_fast = True
			elif asplit.count("Fast") == 1 and flag_fast==True:
				o["annotations"]["Fast"] = "I"
				flag_fast = False
			elif flag_fast == True:
				o["annotations"]["Fast"] = "I"

			if asplit.count("Slow")>1:
				o["annotations"]["Slow"] = "B"
			elif asplit.count("Slow") == 1 and flag_slow==False:
				o["annotations"]["Slow"] = "B"
				flag_slow = True
			elif asplit.count("Slow") == 1 and flag_slow==True:
				o["annotations"]["Slow"] = "I"
				flag_slow = False
			elif flag_slow == True:
				o["annotations"]["Slow"] = "I"

			if ":" in w:
				o["annotations"]["ProlongedSound"] = w
				o["text"] = w.replace(":", "")

			if len(w) > 0 and w[-1] == "-":
				o["annotations"]["Truncated"] = "Final"

			if len(w) > 0 and w[0] == "-":
				o["annotations"]["Truncated"] = "Initial"

			if "Pause" in asplit:
				ret[-1]["annotations"]["PauseAfter"] = "Yes"

			ret.append(o)
		# 	print(o)
		# input()


	ret[0]["annotations"]["Start"] = start
	ret[-1]["annotations"]["End"] = end
	return ret


def produce_conll(input_file, output_folder):

	basename = input_file.stem

	with open(output_folder.joinpath(f"{basename}.conll"), "w") as fout:
		with open(input_file) as csvfile:
			reader = csv.reader(csvfile)

			header = reader.__next__()

			for i, row in enumerate(reader):
				speaker, start, end, duration, transcription, ann_type = row
				# print(ann_type)

				if ann_type == "jefferson":
					text = transcription

				elif ann_type == "ortographic":
					text = pipeline_ortography(transcription)

				elif ann_type == "whisper":
					text = pipeline_whisper(transcription)


				transcription_unit = {
					"speaker": speaker,
					"duration": duration,
					"conversation": basename,
					"text": text,
					"type": ann_type,
					"tu-id": f"TU-{str(i).zfill(4)}",
					"conll": annotate(text, start, end)
				}


				print(f"# conversation: {transcription_unit['conversation']}", file=fout)
				print(f"# tu-id: {transcription_unit['tu-id']}", file=fout)
				print(f"# speaker: {transcription_unit['speaker']}", file=fout)
				print(f"# duration: {transcription_unit['duration']}", file=fout)
				print(f"# text: {transcription_unit['text']}", file=fout)
				print(f"# type: {transcription_unit['type']}", file=fout)
				for token_n, w in enumerate(transcription_unit["conll"]):
					ann_str = "|".join([f"{x}={y}" for x, y in w['annotations'].items()])
					print(f"{token_n+1}\t{w['text']}\t_\t{ann_str}", file=fout)
					# print(w)
				# input()

				# sentence.metadata["Speaker"] = speaker
				# sentence.metadata["Duration"] = duration
				# sentence.metadata["Conversation"] = basename
				# sentence.metadata["Transcription unit"] = i
				# print(vars(sentence))
				# for w in sentence:
				# 	print(f"{w['form']}\t{w['lemma']}\t{w['pros']}\t{w['align']}", file=fout)

				print("\n", file=fout)



def convert_eaf(input_file, jefferson_portions, ortographic_portions, output_folder):

	# for fname in input_files:
	basename = input_file.stem
	with open(input_file, encoding='utf-8') as eaf_stream:
		eaf = elan.parse_eaf_stream(eaf_stream)

		text = eaf.to_csv_rows()
		timesorted_text = sorted(text, key=lambda x: float(x[2]))


		with open(output_folder.joinpath(f"{basename}.csv"), "w") as fout:
			fieldnames = ["Speaker", "start", "end", "span", "transcription", "type"]
			writer = csv.DictWriter(fout, fieldnames=fieldnames)
			writer.writeheader()
			for row in timesorted_text:

				start = float(row[2])
				end = float(row[3])

				found = False
				ann_type = "whisper"
				for s_j, e_j in jefferson_portions:
					if start >=s_j and end <= e_j:
						found = True
						ann_type = "jefferson"
				if not found:
					for s_j, e_j in ortographic_portions:
						if start >=s_j and end <= e_j:
							found = True
							ann_type = "ortographic"

				d = {"Speaker": row[0],
					"start": row[2],
					"end": row[3],
					"span": row[4],
					"transcription": row[5],
					"type": ann_type
				}
				writer.writerow(d)

if __name__ == "__main__":
	from pathlib import Path

#	convert_eaf(Path("data/eaf/DUC22051430.eaf"), [(0, 62)], [(0, 62)], Path("data/csv/"))
	produce_conll(Path("data/csv/DUC22051430.csv"), Path("data/conll/"))