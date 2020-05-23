import argparse
import sqlite3
from pathlib import Path


def clean_files(cursor, threshold, input_root, output_root=None):
    for file_reference, rating in cursor.execute('SELECT file_reference, rating FROM ratings WHERE rating <= ?', (threshold,)):
        path = input_root / file_reference
        if path.exists():
            if rating == 3:
                print(path)
            if output_root is not None:
                new_location = output_root / file_reference
                new_location.parent.mkdir(parents=True, exist_ok=True)
                print('\t', new_location)
                path.replace(new_location)
            # else:
                # path.unlink()
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean up undesired pictures')
    parser.add_argument('db', type=sqlite3.connect, help='SQLite Database of ratings')
    parser.add_argument('root', type=Path, help='Directory root where images are stored')
    parser.add_argument('--destination', 
                        help='Directory root where images are to be moved to (default is to delete)')
    parser.add_argument('--threshold', default=2, type=int,
                        help='Ratings at or below this value are to be cleaned')

    args = parser.parse_args()
    
    c = args.db.cursor()
    destination = None if args.destination is None else Path(args.destination)
    clean_files(c, args.threshold, args.root, destination)
    
    args.db.close()
