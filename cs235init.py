from movie.util.movie_reader import MovieFileCSVReader
def main():
    filename = 'movie/adapters/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    movie_file_reader.read_csv_file()


if __name__ == "__main__":
    main()