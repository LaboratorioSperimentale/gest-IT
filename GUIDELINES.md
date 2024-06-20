# Guidelines for maintainers

- [Guidelines for maintainers](#guidelines-for-maintainers)
- [Before working on the repository](#before-working-on-the-repository)
	- [Install Git and (optionally) a GUI-client](#install-git-and-optionally-a-gui-client)
	- [Install a text editor](#install-a-text-editor)
	- [Clone the repo and swith on `dev` branch](#clone-the-repo-and-swith-on-dev-branch)
	- [Make sure your folders are rightly organized](#make-sure-your-folders-are-rightly-organized)




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
│   ├── audio
│   │   └── (DMC31051430.wav)
│   ├── eaf
│   │   └── (DMC31051430.eaf)
│   ├── gestual
│   │   └── DMC31051430.conll
│   ├── ortographic
│   │   └── DMC31051430.conll
│   ├── prosodic
│   │   └── DMC31051430.conll
│   └── video
│       ├── DMC31051430_left.mp4
│       ├── DMC31051430_centre.mp4
│       └── DMC31051430_right.mp4
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