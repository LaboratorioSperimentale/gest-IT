import argparse
import pathlib

import src.automatic_transcription as transcribe


def _transcribe_data(args):
	input_files = list(args.input_dir.glob("*.wav"))+list(args.input_dir.glob("*.mp3"))
	output_folder = args.output_dir
	transcribe.transcribe_timestamped(input_files, output_folder,
								   args.model, args.language)


def _create_input(args):
	input_files = args.input_dir.glob("*.json")
	output_folder = args.output_dir
	transcribe.create_input(input_files, output_folder)


def _produce_srt(args):
	input_files = list(args.input_dir.glob("*.text.txt"))
	words_files = list(args.input_dir.glob("*.words.json"))

	output_folder = args.output_dir
	transcribe.produce_srt(input_files, words_files, output_folder)


if __name__ == "__main__":

	parent_parser = argparse.ArgumentParser(add_help=False)

	root_parser = argparse.ArgumentParser(prog='src', add_help=True)
	subparsers = root_parser.add_subparsers(title="actions", dest="actions")

	parser_processdata = subparsers.add_parser('transcribe', parents=[parent_parser],
											   description='run whisper model',
											   help='run whisper model')
	parser_processdata.add_argument("-o", "--output-dir", default="data/output/",
								 type=pathlib.Path,
								 help="path to output dir, default is data/output/")
	parser_processdata.add_argument("-i", "--input-dir", required=True,
								 type=pathlib.Path,
								 help="path to folder containing audio files in .wav format")
	parser_processdata.add_argument("-m", "--model", default="data/models/medium.pt",
								 type=pathlib.Path, help="path to model file")
	parser_processdata.add_argument("-l", "--language", default="it")
	parser_processdata.set_defaults(func=_transcribe_data)


	parser_input = subparsers.add_parser("create-input", parents=[parent_parser],
										description='create input for human annotators',
										help='create input for human annotators')
	parser_input.add_argument("-o", "--output-dir", default="data/output/",
						   type=pathlib.Path,
						   help="path to output dir, default is data/output/")
	parser_input.add_argument("-i", "--input-dir", default="output/",
						   type=pathlib.Path,
						   help="path to folder containing whisper transcriptions in json format")
	parser_input.set_defaults(func=_create_input)

	parser_produce = subparsers.add_parser("produce-srt", parents=[parent_parser],
										  description='produce srt for elan import',
										  help='produce srt for elan import')
	parser_produce.add_argument("-o", "--output-dir", default="output_srts/",
							type=pathlib.Path,
  							help="path to output dir, default is output_srts/")
	parser_produce.add_argument("-i", "--input-dir", default="annotators_input",
 							 type=pathlib.Path,
						 	help="folder containing text documents annotated with speaker on first column")
	parser_produce.set_defaults(func=_produce_srt)


	args = root_parser.parse_args()

	if "func" not in args:
		root_parser.print_usage()
		exit()

	args.func(args)