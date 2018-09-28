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

        fp = open(filepath, 'r', encoding="utf-8-sig")

        data = fp.read()
        fp.close()

        data = data.split()

        return len(data)

    '''
        9. Using file and string functions, write your own function to determine the last position of a
        character (provided as a parameter) within a file based on a filepath. You will need to open the file
        and then determine the index of the character within the text file.
    '''

    @staticmethod
    def last_index_in_file(filepath, character):

        fp = open(filepath, 'r', encoding="utf-8-sig")

        last = -1
        position = 0

        for line in fp:
            for char in line:
                if char == character:
                    last = position
                position += 1

        fp.close()
        return last

    '''
        3. Refresher Question: Return the number of characters in a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_character_count(filepath):

        fp = open(filepath, 'r', encoding="utf-8-sig")

        count = 0

        for line in fp:
            for char in line:
                count += 1
        return count

    '''
        25. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the number of states/districts which have a population reported.

        Be aware of the CSV header line
    '''

    @staticmethod
    def populations_reported(filename):

        fp = open(filename, 'r')

        fp.readline() # get past header

        count = 0

        for line in fp:
            line = line.strip().split(',')

            if line[1] is not '':
                count += 1

        return count

    '''
        1. Refresher Question: Return the contents of a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_contents(filepath):

        fp = open(filepath, 'r', encoding='utf-8-sig')
        data = fp.read()
        fp.close()

        return data

    '''
        26. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the total population estimation sum across all states and districts.

        Be aware of the CSV header line
    '''

    @staticmethod
    def total_population(filename):

        fp = open(filename, 'r')

        fp.readline()

        total = 0

        for line in fp:
            line = line.strip().split(',')

            if line[1] is not '':
                total += int(line[1])

        return total

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

        fp = open(filename, 'r', encoding='utf-8')

        data = fp.read()

        start = data.find('feelsLike:')
        end = data.find('</', start)

        return int(data[start+len('feelsLike:'):end-1])



    '''
        30. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        create a new CSV file that contains the name and population of all states/districts 
        which have a population over 2 million.

        Include the CSV header information
    '''

    @staticmethod
    def states_over_two_million(openfile, savefile):

        fp_read = open(openfile, 'r')
        fp_write = open(savefile, 'w')

        header = fp_read.readline()
        fp_write.write(header)

        for line in fp_read:

            data = line.strip().split(',')

            if data[1] is not '':
                population = int(data[1])

                if population >= 2000000:
                    fp_write.write(line)

        fp_read.close()
        fp_write.close()

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

        fp = open(filename, 'r', encoding='utf-8')

        data = fp.read()

        start = data.find('sunrise:')
        end = data.find('</', start)

        return data[start + len('sunrise: '):end]


def main():
    test = Module3()
    #print(test.file_character_count('sample_text.txt'))
    #print(test.total_population('census-state-populations.csv'))
    #print(test.states_over_two_million('census-state-populations.csv','census-state-populations-filtered.csv'))
    print(test.find_sunrise('ELweather.html'))


if __name__ == '__main__':
    main()