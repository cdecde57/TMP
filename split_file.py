import os
import sys
import glob

# Max bytes per chunk. 24 * 1000 * 1000 stays under a 24 MB cap either way
# (decimal MB or MiB). Bump to 24 * 1024 * 1024 to pack tighter if your limit
# is really 24 MiB.
MAX_BYTES = 24 * 1000 * 1000


def split(path):
    stem, ext = os.path.splitext(path)
    size = os.path.getsize(path)
    parts = -(-size // MAX_BYTES)  # ceiling division
    width = max(3, len(str(parts)))
    made = []
    with open(path, "rb") as f:
        i = 1
        while True:
            chunk = f.read(MAX_BYTES)
            if not chunk:
                break
            out = "{}_part{:0{w}d}{}".format(stem, i, ext, w=width)
            with open(out, "wb") as o:
                o.write(chunk)
            made.append(out)
            print("wrote {}  ({:,} bytes)".format(out, len(chunk)))
            i += 1
    print("\nsplit {} into {} part(s)".format(path, len(made)))


def join(a_part, output):
    stem = a_part.split("_part")[0]
    ext = os.path.splitext(a_part)[1]
    parts = sorted(glob.glob("{}_part*{}".format(stem, ext)))
    if not parts:
        print("no parts found matching {}_part*{}".format(stem, ext))
        return
    with open(output, "wb") as o:
        for p in parts:
            with open(p, "rb") as f:
                o.write(f.read())
            print("added", p)
    print("\njoined {} part(s) into {}".format(len(parts), output))


def main():
    args = sys.argv[1:]
    if args and args[0] == "--join":
        if len(args) < 3:
            print("usage: python split_file.py --join <any_part_file> <output_file>")
            return
        join(args[1], args[2])
        return
    path = args[0] if args else input("File to split: ").strip().strip('"')
    if not os.path.isfile(path):
        print("no such file:", path)
        return
    split(path)


if __name__ == "__main__":
    main()
