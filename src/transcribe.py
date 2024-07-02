from speach import elan
import csv

def get_ortographic (text, start, end):

	objects = {"form": "_",
			"lemma": "_",
			"pros": "_",
			"align": "_"}

	ret = []

	split_text = text.split(" ")
	for word in split_text:
		ret.append({"form": word,
					"lemma": "_",
					"pros": "_",
					"align": "_"})

	ret[0]["align"] = f"Start={start}"
	ret[-1]["align"] = f"End={end}"
	return ret




def get_jefferson (text, start, end):

	objects = {"form": "_",
			"lemma": "_",
			"pros": "_",
			"align": "_"}

	ret = {}

	split_text = text.split(" ")
	return []

def produce_conll(input_file, output_folder):

	basename = input_file.stem
	with open(output_folder.joinpath(f"{basename}.conll"), "w") as fout:

		with open(input_file) as csvfile:
			reader = csv.reader(csvfile)

			header = reader.__next__()

			for row in reader:
				speaker, start, end, duration, transcription, ann_type = row
				print(ann_type)

				#print(f"# text = {' '.join(sentence)}", file=fout)
				print(f"# speaker = {speaker}", file=fout)
				print(f"# duration = {duration}", file=fout)
				print(f"# fields = FORM LEMMA PROS ALIGN", file=fout)

				if ann_type == "jefferson":
					sentence = get_ortographic(transcription, start, end)
				elif ann_type == "ortographic":
					sentence = get_ortographic(transcription, start, end)
				elif ann_type == "whisper":
					sentence = transcription.split(" ")

				for w in sentence:
					print(f"{w['form']}\t{w['lemma']}\t{w['pros']}\t{w['align']}", file=fout)

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

	#convert_eaf(Path("data/eaf/DUC22051430.eaf"), [(0, 62)], [(0, 62)], Path("data/csv/"))
	produce_conll(Path("data/csv/DUC22051430.csv"), Path("data/conll/"))