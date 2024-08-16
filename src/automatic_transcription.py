import json
import datetime

import whisper_timestamped as whisper
import tqdm


def transcribe_timestamped(input_files, output_folder, model_path,
						   language):
	"""
	This Python function transcribes audio files using a specified whisper model and language setting,
	saving the results as JSON files in an output folder.

	:param input_files: A list of input audio files that you want to transcribe. Each file should be in
	a format that can be processed by the `whisper.load_audio` function
	:param output_folder: The `output_folder` parameter in the `transcribe_timestamped` function is the
	path to the folder where the transcribed results will be saved as JSON files
	:param model_path: The `model_path` parameter in the `transcribe_timestamped` function is the path
	to the model file that will be used for transcription. This model file contains the pre-trained
	machine learning model that will be used to transcribe the audio files provided as input
	:param language: The `language` parameter in the `transcribe_timestamped` function is used to
	specify the language in which the audio should be transcribed. This parameter determines the
	language model that will be used for transcription
	"""


	model = whisper.load_model(model_path, device="cpu")

	for filename in (pbar := tqdm.tqdm(input_files)):
		stem = filename.stem
		pbar.set_description(f"Processing {stem}")
		audio = whisper.load_audio(filename)

		result = whisper.transcribe(model, audio, language=language)

		with open(output_folder.joinpath(f"{stem}.json"), "w", encoding="utf-8") as fout:
			print(json.dumps(result, indent = 2, ensure_ascii = False), file=fout)


def create_input(input_files, output_folder):
	"""
	The function `create_input` processes input files containing text segments and outputs cleaned text
	files and JSON files with word-level data.

	:param input_files: A list of file paths containing input data in JSON format
	:param output_folder: The `output_folder` parameter in the `create_input` function is the directory
	where the output files will be saved. This folder should be specified as a path where the generated
	text and JSON files will be written to
	"""

	for filename in tqdm.tqdm(input_files):
		stem = filename.stem
		data = json.load(open(filename, encoding="utf-8"))

		text = []
		words = []

		segments = data["segments"]
		for segment in segments:
			text_string = segment["text"].split(" ")
			text.append(" ".join(x.strip(".,?!").lower() for x in text_string))
			for w in segment["words"]:
				w["text"] = w["text"].strip(".,?!").lower()
				words.append(w)

		with open(output_folder.joinpath(f"{stem}.text.txt"), "w", encoding="utf-8") as fout:
			for t in text:
				print(f"\t{t.strip()}", file=fout)

		print(json.dumps(words, indent = 2, ensure_ascii = False),
		file=open(output_folder.joinpath(f"{stem}.words.json"), "w", encoding="utf-8"))


def produce_srt(input_files, words_files, output_folder):
	"""
	The function `produce_srt` processes input files and words files to generate SRT subtitle files
	based on the timing information provided.

	:param input_files: The `input_files` parameter in the `produce_srt` function is a list of file
	paths that contain the dialogue data for which you want to generate SRT files. Each file represents
	a different dialogue or conversation
	:param words_files: list of files containing word-level data
	:param output_folder: The `output_folder` parameter in the `produce_srt` function represents the
	directory where the output SRT files will be saved. This folder should be specified as a path where
	the SRT files will be written to.
	"""

	for filename in input_files:
		print(filename)
		stem = filename.stem[:-5]
		words_file = ""

		for word_filename in words_files:
			stem_word = word_filename.stem[:-6]

			if stem_word == stem:
				words_file = word_filename

		words = json.load(open(words_file, encoding="utf-8"))

		output = {}
		turns = []

		word_index = 0
		speaker = ""

		with open(filename, encoding="utf-8") as fin:
			for _, line in enumerate(fin):
				linesplit = line.split("\t")
				if len(linesplit)>1:

					curr_speaker, text = linesplit
					segmented_text = text.strip().split(" ")

					if len(curr_speaker) > 0:
						speaker = curr_speaker

					if speaker not in output:
						output[speaker] = []

					start = -1
					end = -1

					for i, word in enumerate(segmented_text):
						unique_word = words[word_index]
						if word_index < len(words)-1:
							word_index += 1

						output[speaker].append((word, unique_word["start"], unique_word["end"]))

						if i == 0:
							start = unique_word["start"]
						if i == len(segmented_text)-1:
							end = unique_word["end"]

					turns.append((speaker, text, start, end))

		for speaker in output:
			with open(output_folder.joinpath(f"{stem}_turns_speaker{speaker}.srt"),
			 		"w", encoding="utf-8") as fout:
				for sp, text, begin, end in turns:
					if sp == speaker:
						begin_formatted = datetime.timedelta(seconds=begin)
						end_formatted = datetime.timedelta(seconds=end)
						print(f"{begin_formatted} --> {end_formatted}", file=fout)
						print(text, file=fout)
						print("", file=fout)