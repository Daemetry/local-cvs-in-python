# Local CVS in Python

This repository contains a local CVS implementation in Python.

## Getting Started

To get started with this local CVS implementation, follow these steps:

### Prerequisites

- Python 3.10

### Installation

1. Clone the repository:

```shell
git clone https://github.com/Daemetry/local-cvs-in-python.git
```

2. Navigate to the project directory:

```shell
cd local-cvs-in-python
```

3. Install the required dependencies:

```shell
pip install -r requirements.txt
```

### Usage

Once you have installed the project, you can use its commands. Any command starts with 

```shell
python *your-path-to*/local-cvs-in-python/main.py
```

which further will be abbreviated to "gym".

Pick a directory you want your repository to be in, then cd into it.

- Creating a new repository:

```shell
gym init
```

- Adding files to the repository:

```shell
gym add filename.fileformat
```

Note that no "gym add ." is supported.

- Committing changes to the repository:

```shell
gym commit -m "Commit message"
```

which creates new commit in the system with specified message. Note that message parametre is not optional.

- You can create new branches:

```shell
gym branch name
```

Default branch is called "boss" and it is created alongside the repository.

- Tagging specific commits:

```shell
gym tag everything-went-wrong-from-here
```

- Checking out branches and tages using their names, and commits directly by their hashes:

```shell
gym checkout branch/name
gym checkout tag/name
gym checkout 1h2a3s4h5
```

Take note that checking out on tags and commits is DETACHED HEAD.

- Merging branches. For this you want to first check out the recipient branch, then run:

```shell
gym merge incoming-branch
```

Note that any merge conflicts have to be resolved manually, 
after which you would want to add the changes and commit them. 

## Contributing

Contributions are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the CC BY-SA. 
I don't know why would you even be interested in it, but whatever.

## Acknowledgments

- This implementation of local CVS is inspired by Git CVS and aims to recreate it to some extent 
as a method for its creators to get better at python

## Contact

If you have any questions or feedback, please feel free to contact the project maintainer at [hrudmirom@gmail.com](mailto:hrudmirom@gmail.com).

## Credits

All of the credit for the project goes first and foremost to its two creators:
- Khrustalev Dmitry aka [Daemetry](https://github.com/Daemetry)
- Sharov Alexander aka [IronRino](https://github.com/IronRino)

---
