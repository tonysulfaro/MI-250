import sys
import requests
from csv import *


class Module3:
    """Module 3 Questions"""

    '''
        18. Define a function which extracts the high temperature out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        high temperature \u2013 just the numerical value not including the units or spaces.

        Here is a small extract example of what the HTML file looks like
        <div id="todayData" style="display:none;">
            <!-- TODAY DATA STRUCTURE DEMO -->
            <!-- HEADER: Sat, Sep 1 -->
            <!-- TIMESTAMP: 50m -->
            <div>temp: 69&deg;</div>
            <div>iconCode: 
                <div class="weather weather-21"></div>
            </div>
            <div>feelsLike: 69&deg;</div>
            <div>hiTemp: 82&deg;</div>
            <div>lowTemp: 66&deg;</div>
            <div>precipChance: 10%</div>
            <div>wind: S at 10 mph</div>
            <div>dayPhrase: Night: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>nightPhrase: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>sunrise: 7:01 AM</div>
            <div>sunset: 8:13 PM</div>
            <div>pressure: 30.1 in.</div>
            <div>dewPoint: 66&deg;</div>
            <div>visibility: 10 mi.</div>
            <div>humidity: 90%</div>
            <div>precip: 0.0 in.</div>
            <div>uvIndex: 0</div>
            <div>uvDescription: Low</div>
        </div>
    '''

    @staticmethod
    def find_days_high(filename):

        with open(filename, 'r') as file:

            data = file.read()
            file.close()

            start = data.find('hiTemp:')
            end = data.find('&deg;', start)

            return int(data[start+len('hiTemp:'):end])


    '''
        21. Define a function which extracts the sunset time out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        sunset time \u2013 the numerical value and either AM or PM.

        Here is a small extract example of what the HTML file looks like
        <div id="todayData" style="display:none;">
            <!-- TODAY DATA STRUCTURE DEMO -->
            <!-- HEADER: Sat, Sep 1 -->
            <!-- TIMESTAMP: 50m -->
            <div>temp: 69&deg;</div>
            <div>iconCode: 
                <div class="weather weather-21"></div>
            </div>
            <div>feelsLike: 69&deg;</div>
            <div>hiTemp: 82&deg;</div>
            <div>lowTemp: 66&deg;</div>
            <div>precipChance: 10%</div>
            <div>wind: S at 10 mph</div>
            <div>dayPhrase: Night: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>nightPhrase: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>sunrise: 7:01 AM</div>
            <div>sunset: 8:13 PM</div>
            <div>pressure: 30.1 in.</div>
            <div>dewPoint: 66&deg;</div>
            <div>visibility: 10 mi.</div>
            <div>humidity: 90%</div>
            <div>precip: 0.0 in.</div>
            <div>uvIndex: 0</div>
            <div>uvDescription: Low</div>
        </div>
    '''

    @staticmethod
    def find_sunset(filename):

        with open(filename, 'r') as file:
            data = file.read()
            file.close()

            start = data.find('sunset:')
            end = data.find('</div>', start)

            return data[start+len('sunset: '):end]

    '''
        46. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE/ 
        and use your previous function to extract and return the days highest temperature
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_days_high
    '''
    @staticmethod
    def find_highest_temp_for_zip(zipcode):
        # The save_url_to_file wasn't in my problemset so I made one.

        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        filename = 'low_temp.html'
        save_url_to_file(url, filename)

        # it couldn't see the find_days_low function within the same class so i
        # made an instance of it and used it that way. Kinda Effective
        test = Module3()
        return test.find_days_high(filename)

    '''
        29. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the name of the state/district which has the smallest population estimation.

        Be aware of the CSV header line
    '''

    @staticmethod
    def smallest_state(filename):

        with open(filename) as file:
            file.readline()

            # find lowest population

            lowest = file.readline().split(',')

            for line in file:

                line = line.strip().split(',')

                if int(line[1]) <= int(lowest[1]):
                    lowest = line

            return lowest[0]

    '''
        31. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        create a new CSV file that contains the name and population of all states/districts 
        which have a population below 3 million.

        Include the CSV header information
    '''

    @staticmethod
    def states_under_three_million(openfile, savefile):

        open_file = open(openfile, 'r')
        header = open_file.readline()

        save_file = open(savefile, 'w')
        save_file.write(header)

        for line in open_file:
            line = line.strip().split(',')

            if int(line[1]) <= 3000000:
                temp = line[0]+','+line[1]+'\n'
                save_file.write(temp)

        open_file.close()
        save_file.close()

    '''
        14. Using file and string functions, write your own function to open a file.
        For each line in the file, search for the text "REPLACE ME" and 
        replace it with the persons name provided as a parameter.

        Finally, save the changes to the savefile location
    '''

    @staticmethod
    def modify_text_file_lines(openfile, savefile, name):
        # assumes that REPLACE ME is actually in there

        # here is my method
        readfile = open(openfile, 'r')
        file_data = readfile.read()

        file_data = file_data.replace('REPLACE ME', name)

        readfile.close()

        # write string to file
        outfile = open(savefile, 'w')
        outfile.write(file_data)
        outfile.close()

        return None

    '''
        28. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the name of the state/district which has the largest population estimation.

        Be aware of the CSV header line
    '''

    @staticmethod
    def largest_state(filename):

        with open(filename) as file:
            file.readline()

            # find lowest population

            highest = file.readline().split(',')

            for line in file:

                line = line.strip().split(',')

                if int(line[1]) >= int(highest[1]):
                    highest = line

            return highest[0]

    '''
        43. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE
        and extract the humidity level.
        
        The ZIP code will be passes in as a parameter value, the function should simply return the
        humidity level \u2013 the numerical value and the % sign

        Here is a small extract example of what the HTML file looks like
        <div id="todayData" style="display:none;">
            <!-- TODAY DATA STRUCTURE DEMO -->
            <!-- HEADER: Sat, Sep 1 -->
            <!-- TIMESTAMP: 50m -->
            <div>temp: 69&deg;</div>
            <div>iconCode: 
                <div class="weather weather-21"></div>
            </div>
            <div>feelsLike: 69&deg;</div>
            <div>hiTemp: 82&deg;</div>
            <div>lowTemp: 66&deg;</div>
            <div>precipChance: 10%</div>
            <div>wind: S at 10 mph</div>
            <div>dayPhrase: Night: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>nightPhrase: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</div>
            <div>sunrise: 7:01 AM</div>
            <div>sunset: 8:13 PM</div>
            <div>pressure: 30.1 in.</div>
            <div>dewPoint: 66&deg;</div>
            <div>visibility: 10 mi.</div>
            <div>humidity: 90%</div>
            <div>precip: 0.0 in.</div>
            <div>uvIndex: 0</div>
            <div>uvDescription: Low</div>
        </div>
    '''
    @staticmethod
    def find_humidity_for_zip(zipcode):

        # The save_url_to_file wasn't in my problemset so I made one.

        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'

        page = requests.get(url).text

        start = page.find('humidity: ')
        end = page.find('%', start)

        humid = page[start+len('humidity: '):end]+'%'
        return humid

    '''
        23. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the total population of a state/district passed in as a parameter.

        Be aware of white spaces and capitalization.
    '''

    @staticmethod
    def get_state_population(filename, state):

        fp = open(filename, 'r')
        fp.readline()

        total = 0

        for line in fp:
            line = line.strip().split(',')

            if state.lower() == line[0].lower():
                total += int(line[1])

        return total


    '''
        37. Given a URL, use string functions to extract and return the domain component

        E.g. www.google.com, d2l.msu.edu
    '''

    @staticmethod
    def extract_url_domain(url):

        start = url.find('://')
        end = url.find('/', start+3)

        print(start, end)

        if end == -1:
            return url[start+3:]

        return url[start+3:end]
