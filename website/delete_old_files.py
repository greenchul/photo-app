from sys import path
import time
import os


def delete_old_files(path, seconds):
    for filename in os.listdir(path):
        # print(filename)
        token = "seconds_"
        starts_at = filename.find(token)
        if starts_at > -1:
            end_token = "_"
            ends_at = filename[starts_at+len(token):].find(end_token)
            # print(ends_at)
            if ends_at > -1:
                file_seconds = filename[starts_at + len(token): starts_at + len(token) + ends_at]
                # print(file_seconds)
                if int(file_seconds) < time.time()-seconds:
                    print(f"Deleting this file {file_seconds}")
                    os.remove(os.path.join(path, filename))


if __name__ == "__main__":
    path_to_dir = os.path.join(".","output_no_git")
    path = os.path.join(path_to_dir, f"test_seconds_{int(time.time())}_.png")
    print(path)
    with open(path, "w") as writer:
        writer.write("hello world")
    delete_old_files(path_to_dir, 10)