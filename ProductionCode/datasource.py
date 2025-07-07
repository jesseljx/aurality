import psycopg2
import pandas as pd
import ProductionCode.psqlConfig as config

class DataSource:

    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.
        '''

        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def get_songs_by_attributes(self, attr_dict : dict, sort_results_by: str):
        """Sends sn SQL query to filter the dataset according to the attribute values specified by the user.
        
        attr_dict
            -- attr_dict: a dict {attr1 : val1, attr2 : val2, ...} to filter the songs. See homepage for more details.
            -- search_by: what attribute to perform substring matching on. See homepage for more details.
        Output
            -- returns the filtered table as a pandas Dataframe
        """
        try:
            # set up a cursor
            cursor = self.connection.cursor()

            # Set up the query string
            psql_query = DataSource.get_filter_data_query_str(attr_dict, sort_results_by)
            print(psql_query)
            if psql_query == None:
                return None
            
            # Queries the database
            cursor.execute(psql_query)

            # Formats the result as a dict
            attribute_names = [column[0] for column in cursor.description]
            result_dict = [dict(zip(attribute_names, list(row))) for row in cursor.fetchall()]
            result_dataframe = pd.DataFrame.from_dict(result_dict)
            
            cursor.close()
            print(type(result_dataframe))
            return result_dataframe

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
    
    def get_filter_data_query_str(attr_dict : dict, sort_results_by: str):
        """
        Returns a pSQL query string based on the input arguments

        attr_dict
            -- attr_dict: a dict {attr1 : val1, attr2 : val2, ...} to filter the songs. See homepage for more details.
            -- search_by: what attribute to perform substring matching on. See homepage for more details.
        Output
            -- a psql query string based on the inputs (attr_dict)
        """

        psql_query = "SELECT * FROM songs WHERE " #loop through (dict but take out search_by and substr)
        starting_query_length = len(psql_query)

        for attr_name, attr_val in attr_dict.items(): #loop through dict. Get attr and val. Add attr and val to query.
            if attr_val is None or attr_val == "":
                continue

            attr_type = DataSource.get_attribute_type(attr_name)
            if attr_type == "search" and attr_val[0] is not None and attr_val[0] != "" and attr_val[1] is not None and attr_val[1] != "":
                if "'" in attr_val[1]:
                    attr_val[1] = attr_val[1].replace("'", "''")
                psql_query += f"{attr_val[0]} ~* \'.*({attr_val[1]}).*\' AND "
            elif attr_type == "str":
                psql_query += f"{attr_name} = \'{attr_val}\' AND "
            elif attr_type == "multiple":
                psql_query += f"{attr_name} ~ \'{attr_val}\' AND "
            elif attr_type == "bound":
                lb = attr_val[0]
                ub = attr_val[1]

                if lb is not None and lb != "":
                    psql_query += f"{attr_name} >= {lb} AND "
                if ub is not None and ub != "":
                    psql_query += f"{attr_name} <= {ub} AND "

            elif attr_type == "single":
                psql_query += f"{attr_name} = {attr_val} AND "
                
            else:
                continue

        if len(psql_query) <= starting_query_length:
            psql_query = "SELECT * FROM songs ORDER BY " + sort_results_by + " DESC;"
            return psql_query
        else:
            psql_query = psql_query[:-5] + " ORDER BY " + sort_results_by + " DESC;"
            return psql_query
    
    def get_attribute_type(attr):
        """Returns the 'type' of the attribute.
        Two attributes with the same type have the same query string structure.
        'Type' is NOT the same as types in pSQL.

        Output
            - "str" if substring matching makes sense for the attr
            - "multiple" for attributes where user can select multiple categories
            - "bound" for int or numeric attributes where lower and upper bound makes sense
            - "single" for attributes where user can only filter by one value
            - None if attr is not an attribute in our database
        """

        if attr in ["artist", "track_name", "track_id"]:
            return "str"
        elif attr in ["genre"]:
            return "multiple"
        elif attr in ["popularity" , "year_released" , "danceability" , "energy" , "loudness" , "valence" , "tempo" , "duration_ms"]:
            return "bound"
        elif attr in ["key","mode"]:
            return "single"
        elif attr == "search":
            return "search"
        else:
            return None
    
    def get_unique_artists(self):

        """Returns a list of all unique artists in our database, or None if query fails"""

        try:
            cursor = self.connection.cursor()
            query = "SELECT DISTINCT artist FROM songs ORDER BY artist;"
            cursor.execute(query)

            result = cursor.fetchall()

            cursor.close()

            return [artist for nested_lst in result for artist in nested_lst]

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            
            return None
