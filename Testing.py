def get_parent_path(file_path):
    return file_path[:file_path.rfind("/")]

test_path = "/folder/subfolder/file.png"

folder = get_parent_path(test_path)
print(folder)

print(get_parent_path(folder))

long_str = "The quick brown fox jumped over the lazy dog"
short_str = "Lorem Ipsum"

print(short_str.zfill(50))


list = [50, 30, '-', 40]

for i in list:
    if not i.isnumeric():
        i = 0

print(list)


print(f"{short_str.ljust(20)} {long_str}")