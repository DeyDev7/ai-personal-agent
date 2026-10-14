from functions.write_to_files import write_to_file

print(write_to_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_to_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_to_file("calculator", "/tmp/temp.txt", "this should not be allowed"))