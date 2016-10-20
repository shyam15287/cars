import xlrd
from data_object import DataObject

class DataReader(object):
  RATING_COLUMNS = {
      'user_id': 0, 'movie_id': 1, 'rating': 2, 'social': 12 }

  USER_COLUMNS = {'id': 0, 'age': 3, 'gender': 4, 'city': 5, 'country': 6, }
  MOVIE_COLUMNS = {'id': 1, 'director': 19, 'country': 20, 'language': 21, 'year': 22, 'genre':23, 'budget': 27 }
  MOVIE_METADATA_COLUMNS = {'id': 0, 'field_id': 1, 'value': 2 }
 
  def __init__(self, file_path="../dataset/ldos/LDOS-CoMoDa_small.xls"):
    self.dataset_path = file_path
    self.work_book = xlrd.open_workbook(filename=self.dataset_path)

  # TODO Get movies content MetaData
  # TODO Use pandas directly
  def load(self):
    sheet = self.work_book.sheet_by_name('Sheet1')
    user_data = []
    movie_data = []
    rating_data = []
    for row in range(1, sheet.nrows):
      rating_data.append(self.__read_xls_columns(sheet, row, self.RATING_COLUMNS))
      user_data.append(self.__read_xls_columns(sheet, row, self.USER_COLUMNS))
      movie_data.append(self.__read_xls_columns(sheet, row, self.MOVIE_COLUMNS))

    return DataObject(user_data, movie_data, rating_data, movie_metadata=self.get_movies_metadata())

  def get_movies_titles(self):
    sheet = self.work_book.sheet_by_name('Sheet2')
    movies_titles = {}
    for row in range(0, sheet.nrows):
      movies_titles[sheet.cell_value(row, 0)] = sheet.cell_value(row, 1)
    return movies_titles

  """
  Function
  --------
  get_movies_metadata

  Parameters
  ----------
  Returns
  --------
  A hash
    Of movies metadata.
    key: movie id,
    values: hash movie metadata including movie id (id)
    ex.
    1: {
        id: 1,
        country: 'Greece',
        genre: Comedy
        ....
    }
  """
  def get_movies_metadata(self):
    movies_titles = self.get_movies_titles()
    fields_names = {1: 'director',
        2:  'country',
        3:      'language',
        4:      'year',
        5:      'genre',
        11: 'budget'
        }
    ws = self.work_book.sheet_by_name('Sheet3')
    movies_data = {}
    for movie_id in movies_titles:
        movies_data.setdefault(movie_id, {'id': movie_id})['title'] = movies_titles[movie_id]
    for row in range(0, ws.nrows):
      movie_id = ws.cell_value(row, 0)
      field_id = ws.cell_value(row, 1)
      if field_id in fields_names:
        field_name = fields_names[field_id]
        if movie_id in movies_titles.keys():
            movies_data[movie_id][field_name] = ws.cell_value(row, 2)
    return movies_data

  def persist_to_db(self):
    raise NotImplemented
  
  def __read_xls_columns(self, sheet, row, columns_names):
      fields = {col_name: sheet.cell_value(row, columns_names[col_name]) for col_name in columns_names}
      return fields