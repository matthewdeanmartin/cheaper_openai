"""
All functions for viewing code.

Pure AI concerns
- Needs to always be able to count tokens & set a max with fallback to word count or byte count

Source code
- code to .md file(s)
- https://github.com/liftoff/pyminifier

Source Code - AST
- https://github.com/samuelstevens/pycodesearch

Imported module
- source code
- dir(module), except just important stuff
- help(module)

Concerns
- Don't allow parent directory traversal
- Everything has maximum lines of text
- Multiple output formats
    - plain text
    - markdown out with very light markdown
    - json out (structured objects)
- Skip over .gitignore files
- Skip over hidden by OS files
- args should be similar to bash
- minimize tokens (section headers instead of repeating on every line)

No file system modification

"""
import fnmatch
import glob
import os
import re
import time
from io import StringIO
from itertools import islice
from pathlib import Path
from typing import Optional

import python_minifier
import tiktoken

# grep the code

#



def tree(dir_path: Path, level: int = -1, limit_to_directories: bool = False, length_limit: int = 1000):
    """Given a directory Path object print a visual tree structure
    Credits: https://stackoverflow.com/a/59109706/33264
    """
    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "

    dir_path = Path(dir_path)  # accept string coerceable to Path
    files = 0
    directories = 0

    result = ""

    def inner(dir_path: Path, prefix: str = "", level=-1):
        nonlocal files, directories
        if not level:
            return  # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix + extension, level=level - 1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    result += dir_path.name + "\n"
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        result += line + "\n"
    if next(iterator, None):
        result += f"... length_limit, {length_limit}, reached, counted:" + "\n"
    result += f"\n{directories} directories" + (f", {files} files" if files else "") + "\n"
    return result


def is_python_file(file: str) -> bool:
    return file.endswith(".py")


def format_path_as_header(path):
    return f"## {path}\n\n"


def read_file_contents(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def format_code_as_markdown(base_path: str, output_file: str, header: str) -> None:
    if header == "tree":
        tree_text = tree(Path(base_path))
        markdown_content = f"# Source Code Filesystem Tree\n\n{tree_text}"
        write_or_append(markdown_content, output_file)
        return

    markdown_content = f"# {header} Source Code\n\n"

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if is_python_file(file):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, base_path)
                markdown_content += format_path_as_header(relative_path)
                markdown_content += "```python\n"
                markdown_content += read_file_contents(full_path)
                markdown_content += "\n```\n\n"
    write_or_append(markdown_content, output_file)


def write_or_append(markdown_content, output_file):
    if os.path.exists(output_file):
        mode = "a"
    else:
        mode = "w"
    with open(output_file, mode, encoding="utf-8") as md_file:
        md_file.write(markdown_content)


def is_file_in_root_folder(file_path: str, root_folder: str) -> bool:
    """
    Check if a file is in a given root folder or its subfolders.

    :param file_path: The path of the file to check.
    :param root_folder: The root folder path to check against.
    :return: True if the file is in the root folder or its subfolders, False otherwise.
    """
    # Normalize paths to create absolute paths
    absolute_file_path = os.path.abspath(file_path)
    absolute_root_folder = os.path.abspath(root_folder)

    # Use os.path.commonpath to check if the root folder is a prefix of the file path
    common_path = os.path.commonpath([absolute_file_path, absolute_root_folder])

    return common_path == absolute_root_folder


def remove_root_folder(file_path: str, root_folder: str) -> str:
    # Normalize paths to create absolute paths
    absolute_file_path = os.path.abspath(file_path)
    absolute_root_folder = os.path.abspath(root_folder)
    return os.path.relpath(absolute_file_path, absolute_root_folder)


def is_ignored_by_gitignore(file_path: str, gitignore_path: str = ".gitignore") -> bool:
    """
    Check if a file is ignored by .gitignore.

    Args:
        file_path (str): The path of the file to check.
        gitignore_path (str): The path to the .gitignore file. Defaults to '.gitignore' in the current directory.

    Returns:
        bool: True if the file is ignored, False otherwise.
    """
    if not os.path.isfile(gitignore_path):
        raise FileNotFoundError(f"No .gitignore file found at {gitignore_path}")

    # Normalize file path
    file_path = os.path.abspath(file_path)

    with open(gitignore_path) as gitignore:
        for line in gitignore:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Convert the .gitignore pattern to a glob pattern
            gitignore_pattern = os.path.join(os.path.dirname(gitignore_path), line)

            if fnmatch.fnmatch(file_path, gitignore_pattern):
                return True

    return False


import ast


class SandBoxedShell:
    def __init__(self, root_folder: str) -> None:
        self.root_folder = root_folder
        self.token_model = "gpt-3.5-turbo"

    def grep(self, regex: str, glob_pattern: str, skip_first_matches: int = -1, maximum_matches: int = -1):
        """
        Search for lines matching a regular expression in files specified by a glob pattern.

        :param regex: A regular expression string to search for.
        :param glob_pattern: A glob pattern string to specify files.
        """
        pattern = re.compile(regex)
        matches = 0
        skip_count = 0 if skip_first_matches < 0 else skip_first_matches
        for filename in glob.glob(glob_pattern):
            with open(filename) as file:
                if not is_file_in_root_folder(filename, self.root_folder):
                    continue
                line_number = 0
                for line in file:
                    line_number += 1
                    if pattern.search(line):
                        matches += 1

                        if matches <= (maximum_matches + skip_count) or maximum_matches == -1:
                            if (skip_first_matches > 0 and matches > skip_first_matches) or skip_first_matches == -1:
                                minimal_filename = remove_root_folder(filename, root_folder)
                                print(f"{minimal_filename}: line {line_number}: {line.strip()}")
        print(
            f"{matches} matches found and {matches if matches <= maximum_matches else maximum_matches} displayed. "
            f"Skipped {skip_first_matches}"
        )

    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a string."""
        # gpt3 turbo - cl100k_base
        # gpt2 (or r50k_base) 	Most GPT-3 models
        # p50k_base 	Code models, text-davinci-002, text-davinci-003
        # cl100k_base 	text-embedding-ada-002
        # enc = tiktoken.get_encoding("cl100k_base")

        encoding = tiktoken.encoding_for_model(self.token_model)
        tokens = encoding.encode(text)
        token_count = len(tokens)
        return token_count

    def cat(
        self,
        file_paths: list[str],
        number_lines: bool = True,
        show_ends: bool = False,
        squeeze_blank: bool = True,
        show_tabs: bool = False,
        minify_py: bool = False,
        as_ast: bool = False,
    ) -> None:
        """
        Mimics the basic functionalities of the 'cat' command in Unix.

        :param file_paths: A list of file paths to concatenate.
        :param number_lines: If True, number all output lines.
        :param show_ends: If True, show '$' at the end of each line.
        """
        for file_path in file_paths:
            if not is_file_in_root_folder(file_path, self.root_folder):
                raise Exception("No parent folder traversals allowed")
        line_number = 1

        for file_path in file_paths:
            print(file_path)
            try:
                if is_python_file(file_path) and (minify_py or as_ast):
                    with open(file_path) as f:
                        raw_text = f.read()
                        if as_ast:
                            file_text = ast.dump(ast.parse(raw_text), indent=4)
                        else:
                            file_text = python_minifier.minify(raw_text)

                    with StringIO(file_text) as file:
                        self.process_cat_file(file, line_number, number_lines, show_ends, show_tabs, squeeze_blank)
                else:
                    with open(file_path, "rb") as file:
                        self.process_cat_file(file, line_number, number_lines, show_ends, show_tabs, squeeze_blank)
            except FileNotFoundError:
                print(f"python_cat: {file_path}: No such file or directory")
            except Exception as e:
                print(f"python_cat: {file_path}: {e}")

    def process_cat_file(self, file, line_number, number_lines, show_ends, show_tabs, squeeze_blank):
        was_blank = False
        skip = False
        for line in file:
            if isinstance(line, bytes):
                line_text = line.decode("utf-8")  # Decode bytes to string
            else:
                line_text = line
            if was_blank and line_text in ("\r\n", "\n"):
                skip = True
                print(line_text)

            if line_text not in ("\r\n", "\n"):
                # never skip a line with text
                skip = False

            if not skip or not squeeze_blank:
                if show_ends:
                    if line_text.endswith("\r\n"):
                        line_text = line_text.replace("\r\n", "^M$\n")
                    elif line_text.endswith("\n"):
                        line_text = line_text.replace("\n", "$\n")
                if show_tabs:
                    line_text = line_text.replace("\t", "^I")

                if number_lines:
                    print(f"{line_number}\t", end="")

                if line_text.endswith("\r\n"):
                    # save some tokens.
                    line_text = line_text.replace("\r\n", "\n")
                print(line_text, end="")

                line_number += 1
            was_blank = line_text in ("\r\n", "\n")

    def find_files(self, pattern: str) -> list[str]:
        """
        Recursively search for files matching a given pattern in a directory and its subdirectories.

        Args:
            pattern (str): The pattern to match filenames against.

        Returns:
            List[str]: A list of paths to files that match the pattern.
        """
        matching_files = []
        for root, dirs, files in os.walk(self.root_folder):
            for file in files:
                if is_file_in_root_folder(file, self.root_folder):
                    if pattern in file:
                        matching_files.append(os.path.join(root, file))
        return matching_files

    def head(self, file_path: str, lines: int = 10) -> None:
        for line in self.head_tail(file_path, lines, "head"):
            print(line)

    def tail(self, file_path: str, lines: int = 10) -> None:
        for line in self.head_tail(file_path, lines, "tail"):
            print(line)

    def head_tail(self, file_path: str, lines: int = 10, mode: str = "head") -> list[str]:
        """
        Read lines from the start ('head') or end ('tail') of a file.

        Args:
            file_path (str): Path to the file.
            lines (int): Number of lines to read. Defaults to 10.
            mode (str): Operation mode, either 'head' or 'tail'. Defaults to 'head'.

        Returns:
            List[str]: A list of the requested lines from the file.
        """
        if mode not in ["head", "tail"]:
            raise ValueError("Mode must be 'head' or 'tail'")

        if is_file_in_root_folder(file_path, self.root_folder):
            with open(file_path) as file:
                if mode == "head":
                    return [next(file) for _ in range(lines)]
                else:  # mode == 'tail'
                    return list(file)[-lines:]

    def ls(self, path: Optional[str] = ".", all: bool = False, long: bool = False) -> list[str]:
        """
        List directory contents, with options to include all files and detailed view.

        Args:
            path (str, optional): The directory path to list. Defaults to the current directory '.'.
            all (bool): If True, include hidden files. Defaults to False.
            long (bool): If True, include details like permissions, owner, size, and modification date. Defaults to False.

        Returns:
            List[str]: List of files and directories, optionally with details.
        """
        entries = os.listdir(path) if all else [entry for entry in os.listdir(path) if not entry.startswith(".")]
        entries_info = []

        for entry in entries:
            full_path = os.path.join(path, entry)
            if not is_file_in_root_folder(full_path, self.root_folder):
                continue
            if long:
                stats = os.stat(full_path)
                # permissions = stat.filemode(stats.st_mode)
                size = stats.st_size
                mod_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(stats.st_mtime))
                entries_info.append(f"{size:>10} {mod_time} {entry}")
            else:
                entries_info.append(entry)
        for line in entries_info:
            print(line)
        return entries_info


import inspect

import markpickle


def get_source(module_path: str, function_name: str) -> str:
    """Takes file system path to module and name of function as string, Return source code"""
    # TODO: use importlib to import markpickle from "e:/github/src/"
    return inspect.getsource(markpickle.split_file)


if __name__ == "__main__":
    a = SandBoxedShell("E:/github/")
    # a.ls("E:/github/untruncate_json")

    a.cat(
        [
            "E:/github/untruncate_json/untruncate_json/untrunc.py",
            # "E:/github/untruncate_json/pyproject.toml"
        ],
        number_lines=True,
        show_ends=False,
        squeeze_blank=True,
        as_ast=False,
    )
    # print(get_source("a"))
    # grep_like_function("\\bdef\\b|\\bclass\\b",
    #                    "e:/github/markpickle/docs/../**/*.py",
    #                    "e:/github/markpickle/",
    #                    skip_first_matches=25,
    #                    maximum_matches=15)

    # format_code_as_markdown("E:/github/untruncate_json/untruncate_json", "output.md", "tree")
    # format_code_as_markdown("E:/github/untruncate_json/untruncate_json", "output.md", "module")
    # format_code_as_markdown("E:/github/untruncate_json/tests", "output.md", "tests")
    # # TODO: supporting files, eg. pyproject.toml/setup.py
    # # TODO: somehow docs
    # # TODO: uh...
