import os
import shutil
import subprocess 
import random
import PyPDF2
from argparse import ArgumentParser
from pathlib import Path

random.seed(1234)

def choose_random_files(pdf_dir: Path, n: int):
    files = os.listdir(pdf_dir)
    num_sample = min(n, len(files))
    choices = random.sample(files, k=num_sample)
    return [Path(pdf_dir, f) for f in choices]

def choose_random_pages(file: Path, n: int):
    reader = PyPDF2.PdfReader(str(file))
    num_pages = len(reader.pages)
    num_sample = min(n, num_pages)
    return random.sample(list(range(num_pages)), k=num_sample)


def create_random_selection(pdf_dir, n_books: int, pages_per_book: int):
    files = choose_random_files(pdf_dir, n_books)
    for file in files:
        try:
            print(f"Chose {file}")
            pages = choose_random_pages(file, pages_per_book)
            yield (file, pages)
        except Exception as e:
            print(f"Failed to read {file} because: {e}")


def process(file, pages, output_dir):
    for page in pages:
        cmd = f"nougat --checkpoint nougat-base/ -o '{output_dir}' '{file}' --pages {page}"
        print(f'running: {cmd}')
        output = subprocess.getoutput(cmd)
        dest_file = Path(output_dir) / Path(file).with_suffix('.mmd').name
        renamed_dest_file = Path(dest_file).with_suffix(f'.p{page}.mmd')
        shutil.move(dest_file, renamed_dest_file)
        print(f"Saved file to {renamed_dest_file}")

if __name__ == '__main__':
    parser = ArgumentParser('page processor')
    parser.add_argument('--pdf_dir', type=str, help='path to pdf dir')
    parser.add_argument('--n_books', type=int, help='number of books')
    parser.add_argument('--pages', type=int, help='pages per book')
    parser.add_argument('--output_dir', type=str, help='path to output mmd dir')

    args = parser.parse_args()

    Path(args.output_dir).mkdir(exist_ok=True, parents=True)

    for file, pages in create_random_selection(args.pdf_dir, n_books=args.n_books, pages_per_book=args.pages):
        output = process(file, pages, args.output_dir)

    print('All done!')
