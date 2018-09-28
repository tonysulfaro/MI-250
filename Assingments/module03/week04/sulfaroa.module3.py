import sys
import requests
from csv import *


class Module3:
    """Module 3 Questions"""

    '''
        42. HARD: Given a URL, open the webpage and return the first image source url (img src).
        Some websites may use capitals for html tags and some may not.
        For the purpose of this task, convert everything to lowercase to avoid this issue.
        If no tag exists, return None

        Hint: calling read() on a connection returns utf8 encoded bytes,
            you will also need to decode these to convert it into a normal string.
    '''

    @staticmethod
    def extract_url_img_src(url):
        return url

    '''
        5. Refresher Question: Return the number of words in a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_word_count(filepath):
        return -1

    '''
        9. Using file and string functions, write your own function to determine the last position of a
        character (provided as a parameter) within a file based on a filepath. You will need to open the file
        and then determine the index of the character within the text file.
    '''

    @staticmethod
    def last_index_in_file(filepath, character):
        return -1

    '''
        3. Refresher Question: Return the number of characters in a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_character_count(filepath):
        return -1

    '''
        25. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the number of states/districts which have a population reported.

        Be aware of the CSV header line
    '''

    @staticmethod
    def populations_reported(filename):
        return -1

    '''
        1. Refresher Question: Return the contents of a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_contents(filepath):
        return filepath

    '''
        26. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the total population estimation sum across all states and districts.

        Be aware of the CSV header line
    '''

    @staticmethod
    def total_population(filename):
        return -1

    '''
        16. Define a function which extracts the 'feels like' temperature out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        'feels like' temperature \u2013 just the numerical value not including the units or spaces.

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
    def find_feels_like_temperature(filename):
        return filename

    '''
        30. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        create a new CSV file that contains the name and population of all states/districts 
        which have a population over 2 million.

        Include the CSV header information
    '''

    @staticmethod
    def states_over_two_million(openfile, savefile):
        return None

    '''
        20. Define a function which extracts the sunrise time out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        sunrise time \u2013 the numerical value and either AM or PM.

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
    def find_sunrise(filename):
        return filename

    