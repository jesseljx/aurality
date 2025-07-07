import unittest
import subprocess
import ProductionCode.datasource as ds
import command_line as cl
import csv
import math

class Test_ProductionCode(unittest.TestCase):
    '''
    Unit tests for the ProductionCode module using unittest.
    '''

    def test_parse_search_substr(self):
        """Checks if the parse_search_substr in command_line.py is working properly"""

        reference = [] 
        reference.append(("song:Love",("Love", "track_name"), "1")) 
        reference.append(("song:Memories",("Memories", "track_name"),"2")) 
        reference.append(("artist:Katy Perry",("Katy Perry", "artist"),"3"))
        reference.append(("songname:Never Really Over - R3HAB Remix",("Never Really Over - R3HAB Remix", "songname"),"5"))
        reference.append(("artist:Avicii",("Avicii", "artist"),"6"))
        
        for i in range(len(reference)):
            self.assertEqual(cl.parse_search_substr(reference[i][0]), reference[i][1], reference[i][2])

    def test_check_search_substr(self):
        """Checks if the check_search_substr in command_line.py is working properly"""

        reference = []

        #Standard cases
        reference.append(("song:Love",True,"song valid"))
        reference.append(("artist:Blah",True,"artist valid"))
        reference.append(("song:",True,"empty song"))
        reference.append(("artist:",True,"empty artist"))
    
        #Edge cases
        reference.append(("songLove",False,"no colon 1"))
        reference.append(("songg:Love",False,"song misspelled 1"))
        reference.append(("Song:Love",False,"song misspelled 2"))
        reference.append(("Artist:bob",False,"artist mispelled"))
        reference.append(("",False,"empty string"))
        
        for i in range(len(reference)):
            self.assertEqual(cl.check_search_substr(reference[i][0]), reference[i][1],reference[i][2])

    def test_usage_msg(self):
        """Test that usage_msg() returns the expected usage string when called with no arguments."""
        expected_output = """python3 command_line.py [-h] [-k [0|1|2|3|4|5|6|7|8|9|10|11]] [-m [0|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION] [-d MIN_DURATION] [-g GENRE] [-s SONG] [-i ID] [-r ARTIST]
                       [-y MIN_YEAR] [-Y MAX_YEAR] [-p MIN_POPULARITY] [-P MAX_POPULARITY] [-b MIN_DANCEABILITY] [-B MAX_DANCEABILITY] [-e MIN_ENERGY] [-E MAX_ENERGY]
                       [-l MIN_LOUDNESS] [-L MAX_LOUDNESS] [-v MIN_VALENCE] [-V MAX_VALENCE] [-S SEARCH_SUBSTR]\nHelp: python3 command_line.py -h\n\n"""
        self.assertEqual(cl.usage_msg(), expected_output)
        self.assertEqual(cl.usage_msg("test"), expected_output)

        
    def test_main(self):
        '''
        Arguments: None
        Return: None
        Purpose: Tests the main function from the command_line.py file for valid and invalid command line arguments
        '''
        
        usage = """python3 command_line.py [-h] [-k [0|1|2|3|4|5|6|7|8|9|10|11]] [-m [0|1]] [-T MAX_TEMPO] [-t MIN_TEMPO] [-D MAX_DURATION] [-d MIN_DURATION] [-g GENRE] [-s SONG] [-i ID] [-r ARTIST]
                       [-y MIN_YEAR] [-Y MAX_YEAR] [-p MIN_POPULARITY] [-P MAX_POPULARITY] [-b MIN_DANCEABILITY] [-B MAX_DANCEABILITY] [-e MIN_ENERGY] [-E MAX_ENERGY]
                       [-l MIN_LOUDNESS] [-L MAX_LOUDNESS] [-v MIN_VALENCE] [-V MAX_VALENCE] [-S SEARCH_SUBSTR]\n"""

        reference = []
        reference.extend([
            #key edge
            (["-k", "-1"], usage, "edge"),
            (["-k", "4.5"], usage, "edge"), 
            (["-k", "0", "2"], "", "edge"), 

            #mode edge
            (["-m", "-1"], usage, "edge"),
            (["-m", "1.5"], usage, "edge"), 
            (["-m", "12"], usage, "edge"),
            (["-m" ,"0", "0"], "", "edge"), 

            #MAX_TEMPO edge
            (["-T", "ninety"], usage, "edge"), 
            (["-T", "100", "20"], "", "edge"), 

            #MIN_TEMPO edge
            (["-t", "ninety"], usage, "edge"), 
            (["-t", "100", "20"], "", "edge"), 

            #MAX_DURATION edge
            (["-D", "fake song name"], usage, "edge"),
            (["-D", "NOTArealALbumName"], usage, "edge"),
            (["-D", "100000", "fake arg"], "", "edge"), 
        
            #MIN_DURATION edge
            (["-d", "notANarTist"], usage, "edge"), 
            (["-d", "100000", "fake arg"], "", "edge"), 

            #SEARCH_SUBSTR edge
            (["-S", "NOTArealSubstr"], usage, "edge"),
            (["-S", ""], usage, "edge"),
            (["-S", "song:Love", "fake arg"], "", "edge")
        ])

        ##Add standard cases for when we expect our functions to return an empty list
        with open('Tests/sample_songs.csv', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        for i in range(len(rows)):
            rows[i] = self.row_to_args(rows[i])
           
            reference.append((rows[i],[rows[i][5]],"normal")) #Everything
            reference.append((rows[i][6:],[rows[i][5]],"normal")) #Everything but song name, artist, and ID
            reference.append((rows[i][:4],[rows[i][5]],"normal")) #Just song name and artist

        prefix = ["python3" , "-u" ,"command_line.py"]
    
        for i in range(0,len(reference)):
            # print("\nPrefix: " + str(prefix + reference[i][0])+"\n") #Debug
            code = subprocess.Popen(prefix + reference[i][0],stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
           
            output, err = code.communicate()
            
            if reference[i][2] == "edge":
                self.assertIn(reference[i][1], output.strip()) 
            else:
                output = output.strip()
    
                for song_id in reference[i][1]:
                    self.assertIn(song_id, output) #Check if expected song ID is in output
                self.assertIn(str(len(reference[i][1])) + " rows", output) #Check if numRows in output = num of expected songs
            
            code.terminate()
        
        f.close()

    def row_to_args(self, row : list):
        args = []
        all_args = ["-r", "-s", "-i" ,"-p" , "-P" , "-y", "-Y", "-g", "-b", "-B", "-e", "-E", "-k", "-l", "-L", "-m", "-v", "-V", "-t", "-T", "-d", "-D"]
        bounds = ["-p", "-y", "-b", "-e", "-l", "-v", "-t", "-d"]
        decimals_lb = ["-b", "-e", "-v"]
        decimals_ub = ["-B",  "-E", "-V"]
        counter = 0
        for i in range(len(all_args)):
            if all_args[i] in bounds:
                num_to_append = row[counter]

                if all_args[i] in decimals_lb:
                    num_to_append = round(float(num_to_append),3)
                    num_to_append = str(num_to_append)

                if all_args[i] in decimals_ub:
                    num_to_append = math.ceil(num_to_append * 1000) / 1000.0
                    num_to_append = str(num_to_append)

                args.append(all_args[i])
                args.append(num_to_append)
            else:
                args.append(all_args[i])
                args.append(row[counter])
                counter += 1
        
        return args

if __name__ == '__main__':
    unittest.main()