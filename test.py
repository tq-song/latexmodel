import os
import filecmp


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def compare_files(file1, file2):
    lines1 = read_file(file1)
    lines2 = read_file(file2)

    diff = []
    for i, (line1, line2) in enumerate(zip(lines1, lines2)):
        if line1 != line2:
            diff.append((i, line1, line2))

    return diff


def compare_directories(dir1, dir2):
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))

    common_files = files1 & files2
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1

    # Compare common files
    for file_name in common_files:
        file1 = os.path.join(dir1, file_name)
        file2 = os.path.join(dir2, file_name)

        if os.path.isfile(file1) and os.path.isfile(file2):
            if not filecmp.cmp(file1, file2, shallow=False):
                diffs = compare_files(file1, file2)
                if diffs:
                    print(f"Differences found in file: {file_name}")
                    for line_num, line1, line2 in diffs:
                        print(f"Line {line_num + 1}:")
                        print(f"File1: {line1.strip()}")
                        print(f"File2: {line2.strip()}")
                        print()
        else:
            print(f"Skipping non-file: {file_name}")

    # Display files only in dir1
    if only_in_dir1:
        print("Files only in directory 1:")
        for file_name in only_in_dir1:
            print(file_name)

    # Display files only in dir2
    if only_in_dir2:
        print("Files only in directory 2:")
        for file_name in only_in_dir2:
            print(file_name)

    # Check for files with different names
    if only_in_dir1 or only_in_dir2:
        print("Files with different names between the directories:")
        for file_name in only_in_dir1:
            print(f"Only in {dir1}: {file_name}")
        for file_name in only_in_dir2:
            print(f"Only in {dir2}: {file_name}")


if __name__ == "__main__":
    dir1 = "informs/MNSC-style-file-2023"
    dir2 = "informs/MSOM-style-file-2023"

    compare_directories(dir1, dir2)
