import git

repo = git.Repo(".")
commits = list(repo.iter_commits())

for commit in commits:
    author = commit.author
    date = commit.committed_datetime.strftime("%x")
    message = commit.message.strip()
    changes = []
    for diff in commit.diff(create_patch=True):
        if not diff.b_path.endswith(".lock"):
            line_count = 0
            if diff.new_file:
                lines_in_new_file = len(diff.diff.decode("utf-8").split("\n"))
                changes.append(f"New File {diff.b_path}, {lines_in_new_file} lines")
            for line in diff.diff.decode("utf-8").split("\n"):
                line_count += 1
                if line_count < 6:
                    if line.startswith("+") or line.startswith("-"):
                        changes.append(line)

    print(f"Author: {author.name} <{author.email}>")
    print("Date: %s" % date)
    print("Full Comment: %s" % message)
    for change in changes:
        if change.startswith("+") or change.startswith("-"):
            print("    %s" % change[1:])
        else:
            print("     " + change)
    print("\n")
