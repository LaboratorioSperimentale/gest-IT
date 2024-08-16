# Guidelines for maintainers

- [Guidelines for maintainers](#guidelines-for-maintainers)
- [Before working on the repository](#before-working-on-the-repository)
	- [Install Git and (optionally) a GUI-client](#install-git-and-optionally-a-gui-client)
	- [Install a text editor](#install-a-text-editor)
	- [Clone the repo and swith on `dev` branch](#clone-the-repo-and-swith-on-dev-branch)
	- [Make sure your folders are rightly organized](#make-sure-your-folders-are-rightly-organized)
	- [Create environment](#create-environment)
- [Workflow](#workflow)
	- [General information](#general-information)
	- [1. Video editing](#1-video-editing)
	- [2. Automatic transcription with whisper](#2-automatic-transcription-with-whisper)
	- [3. Anonimization and preparation of `.srt` files](#3-anonimization-and-preparation-of-srt-files)
	- [3. Ortographic Transcription](#3-ortographic-transcription)
		- [Numbers](#numbers)
		- [Common conventions](#common-conventions)
			- [Other](#other)
	- [Anonymization](#anonymization)
	- [4. Prosodic Transcription](#4-prosodic-transcription)
	- [5. Gesture Transcription](#5-gesture-transcription)




The `gest-IT` repository is collaboratively maintained by PIs, lab technicians and students involved in the creation of the `gest-IT` corpus.

The development of the corpus is loosely based on the principles of [Continuous Integration](https://en.wikipedia.org/wiki/Continuous_integration), a software development methodology practice that aims at ensuring that the integrated resource remains in a workable state.

[TODO: expand on git-based development]

The repository is constituted by two main branches:
* `main` - contains the last, officially released version of the repository
* `dev` - contains the working version of the repository

Maintainers should never work directly on the `main` branch: every change is done on `dev` and, at release time, a designated maintainer will take care of propagating changes from `dev` to `main` and therefore produce the next release of the resource.


# Before working on the repository

In order to set up their environment, maintaners should perform a set of preliminary steps, namely:

## Install Git and (optionally) a GUI-client

In order for continuous integration to happen, the repository is synced via `git`.
Therefore, as a first step, you should make sure to have both `git` and an user interface installed on your laptop.

Choose the most suitable version of git from the [official download page](https://git-scm.com/downloads) and a [GUI of your choice](https://git-scm.com/downloads/guis)

It's a nice idea to go through a [basic tutorial](https://www.atlassian.com/git) to understand how git works and what are the best practices when working on a collaborative project.

## Install a text editor

In order to work with the text files in the corpus, a suitable text editor is needed.
[Visual Studio Code](https://code.visualstudio.com/) is a popular choice that allows for multiple operations that might be needed when operating with this repository (e.g., modifying text files, running python code, refactoring the folder structure...).
Of course other options are possible as well.

## Clone the repo and swith on `dev` branch

Next, you'll need to clone the repository (i.e., creating a local tracked copy on your machine).

* If you're actively involed in the development, project admins will have added you among the authorized maintainers and you're therefore able to clone the repository directly from GUI.
* Otherwise, you can fork the repository on github and work on your own version of it.

You should then switch on the `dev` branch (find how to do it on your GUI, it's on the bottom left side of the screen on VSCode) to make sure you're working on the right version of the repository.

## Make sure your folders are rightly organized

For both space and privacy reasons, not everything about `gest-IT` can be tracked via git.
However, if you're a maintainer in the project, you're likely to have on your local machine all of the corpus files, also the non-tracked ones.

In order for everything to work right, your local folder should have the following structure, where untracked files are in paretheses:

```
gest-IT/
├── data
│   ├── (audio)
│   │   └── (DMC31051430.wav)
│   ├── (whisper-transcribed)
│   │   └── (DMC31051430.json)
│   │   └── (DMC31051430.text.txt)
│   │   └── (DMC31051430.words.json)
│   ├── (srts)
│   |   ├── (DMC31051430_speakerA.srt)
│   |   └── (DMC31051430_speakerB.srt)
│   ├── (eaf)
│   │   └── (DMC31051430.eaf)
│   ├── gestual
│   │   └── DMC31051430.conll
│   ├── ortographic
│   │   └── DMC31051430.conll
│   ├── prosodic
│   │   └── DMC31051430.conll
│   └── (video)
│       ├── (DMC31051430_left.mp4)
│       ├── (DMC31051430_centre.mp4)
│       └── (DMC31051430_right.mp4)
├── (models)
├── docs
│   ├── education.md
│   └── professioni_istat.md
├── GUIDELINES.md
├── LICENSE
├── metadata
│   ├── conversations
│   |   ├── DMC31051430.yaml
│   |   └── generic_conversation.yaml
│   ├── (name-code-mapping.csv)
│   └── participants
│       ├── B001.yaml
│       ├── B002.yaml
│       ├── ...
│       └── generic_participant.yaml
└── README.md
```

## Create environment

In order to work with the available scripting tools, the first step consists in setting up the necessary virtual environment.

You can do it by running:

```
python3.11 -m venv .venv
```

The required python packages are reported in the `required.txt` file. After having activated the virtual environment (`source ./venv/bin/activate`) you can either install them manually or run:

```
pip install -r requirements.txt
```


# Workflow

## General information

TODO: add metadata description


## 1. Video editing

**Video Editing** is performed in Adobe Premiere Pro. For each conversation, the three videos capturing three points of view are automatically synchronized and cut.
For each conversation, 4 files are generated:

```
data
 ├── audio
 │   └── [CONVERSATION_CODE].wav
 └── video
     ├── [CONVERSATION_CODE].mp4
     ├── [CONVERSATION_CODE].mp4
     └── [CONVERSATION_CODE].mp4
```

## 2. Automatic transcription with whisper

Audio files are then **automatically transcribed** via `whisper`.

In order to transcribe audio files, you can run:

```
python main.py transcribe -o path/to/output/folder -i path/to/input/folder -m path/to/model/file
```

This will create a `[CONVERSATION_NAME].json` file in your chosen output folder.

In order to proceed with processing, you can the use the `create-input` command by running:

```
python main.py create-input -o path/to/output/folder -i path/to/input/folder
```

The input folder should contain the previously created `json` file.
By running this step, you will obtain two files:
* `[CONVERSATION_NAME].text.txt`: a two column file with the first column being empty and the second containing a sequence of tokens that `whisper` identified as a coherent unit
* `[CONVERSATION_NAME].words.json` containing timestamps associated to each word produced in whisper transcription


## 3. Anonimization and preparation of `.srt` files

At this point, a manual annotator will proceed to assign speakers IDs to the units contained in the `[CONVERSATION_NAME].text.txt` file.

Example:

- file before turn assignment:
  ```
	e in giappone
	no che bello
	cioè quindi le scuole più fighe fuori ovviamente dalla spagna sono queste due mie
	parliamo di un altro viaggio in giappone io ci sono stata
  ```
- file after turn assignment:
  ```
  S001	e in giappone
  B003	no che bello
  B003	cioè quindi le scuole più fighe fuori ovviamente dalla spagna sono queste due mie
  S001	parliamo di un altro viaggio in giappone io ci sono stata
  ```
TODO: edit with real speakers


This step will also include **anonymization**. As far as this is concerned, annotators should follow these rules:
* proper names
* references to specific events
* ...

TODO: check anonymization rules


After these steps are performed, one can produce `.srt` files that will be imported into `ELAN` for further processing.

In order to produce these, you should run:

```
python main.py produce-srt
```

## 3. Ortographic Transcription

- one layer per speaker (using its identifier as tiername) + one layer for the experimeter + one layer for environment (metalanguage)
- everything will be lowercased

### Numbers
- if specific pronunciation (ex. `centun volte`), then transcribe
- else, you can transcribe the number as is and it will be automatically converted to words (library `num2word`)
- TODO: decide if there's a difference between years, ordinals, cardinals etc...

### Common conventions

- `ok` will be transformed into `okei`
- acronyms have to be expanded (eg. cgil -> cigielle)
- `cioè` sometimes pronounced fast is transcribed as `ceh`
- `yuhu`
- Le interiezioni sono sempre trascritte con una ‘h’ alla fine (es, mh; ah; eh)

#### Other
- interruptions with hyphen
- ((ride)) etc
- TODO: define possible values

## Anonymization

## 4. Prosodic Transcription

TODO: define general guidelines

## 5. Gesture Transcription

TODO: define general guidelines