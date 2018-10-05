"""
Tony Sulfaro
Module 03 Week 05
Problem set
"""

import sys
import requests
from csv import *


class Module3:
    """Module 3 Questions"""

    '''
        34. HARD - Create a new CSV file which contains the name of each state and the corresponding population
        sorted from largest to smallest population.

        Hint: You may want to create a few different functions or use some of the other functions
        for this function to call!
    '''

    @staticmethod
    def sort_states_descending(openfile, savefile):

        open_fp = open(openfile, 'r')
        save_fp = open(savefile, 'w')

        header = open_fp.readline()
        save_fp.write(header)

        data = []

        for line in open_fp:
            line = line.strip().split(',')
            data_tup = (line[0], int(line[1]))
            data.append(data_tup)

        data = sorted(data, key=lambda x: x[1])

        for item in data:
            line = item[0] + ',' + str(item[1]) + '\n'
            save_fp.write(line)

        open_fp.close()
        save_fp.close()

    '''
        48. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE/ 
        and use your previous function to extract and return the sunrise time
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_sunrise
    '''

    @staticmethod
    def find_sunrise_for_zip(zipcode):

        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        save_url_to_file(url, 'weather.html')

        return find_sunrise('weather.html')

    '''
        49. Given a ZIP code, pull the current weather from XXXX 
        and use your previous function to extract city and ZIP code
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_geography
    '''

    @staticmethod
    def find_geography_for_zip(zipcode):
        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        save_url_to_file(url, 'geography.html')

        return find_geography('geography.html')

    '''
        45. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE/ 
        and use your previous function to extract and return the current temperature
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_current_temperature
    '''

    @staticmethod
    def find_current_temp_for_zip(zipcode):
        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        save_url_to_file(url, 'weather.html')

        return find_current_temperature('weather.html')

    '''
        2. Refresher Question: Return the number of lines in a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_line_count(filepath):

        fp = open(filepath, 'r')

        count = 0
        for line in fp:
            count += 1
        return count

    '''
        50. Given a ZIP code, pull the current weather from XXXX 
        and use your previous function to extract the feels like temperature
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_feels_like_temperature
    '''

    @staticmethod
    def find_feels_like_temp_for_zip(zipcode):
        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        save_url_to_file(url, 'weather.html')

        return find_feels_like_temperature('weather.html')

    '''
        32. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        create a new CSV file that contains the name and population of all states/districts 
        which have a name starting with the letter "m"

        Include the CSV header information
    '''

    @staticmethod
    def extract_m_states(openfile, savefile):

        open_fp = open(openfile, 'r')
        save_fp = open(savefile, 'w')

        header = open_fp.readline()
        save_fp.write(header)

        for line in open_fp:
            data = line.strip().split(',')

            if data[0].lower() == 'm':
                save_fp.writeline(line)

        open_fp.close()
        save_fp.close()

    '''
        24. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the name of the state/district which has a total population passed in as a parameter.

        Be aware of white spaces and capitalization.
    '''

    @staticmethod
    def get_state_name(filename, population):

        fp = open(filename, 'r')

        for line in fp:
            data = line.strip().split(',')

            if int(data[1]) == population:
                return data[1]

    '''
        39. Given a URL, use string functions to extract and return the protocol component

        E.g. http, https, ftp
    '''

    @staticmethod
    def extract_url_protocol(url):

        found = url.find(':')
        return url[:found]

    '''
        41. HARD: Given a URL, open the webpage and return the first anchor link url (a href).
        Some websites may use capitals for html tags and some maynot.
        If no tag exists, return None
        For the purpose of this task, convert everything to lowercase to avoid this issue.
        In addition, you should only extract absolute URLs (ones starting with http...) and not relative ones.

        Hint: calling read() on a connection returns utf8 encoded bytes,
            you will also need to decode these to convert it into a normal string.
    '''

    @staticmethod
    def extract_url_link(url):

        pass


def save_url_to_file(url, filename):
    page = requests.get(url).text
    fp = open(filename, 'wb')
    fp.write(page.encode())
    fp.close()


def find_sunrise(filename):
    fp = open(filename, 'r', encoding='utf-8')

    data = fp.read()

    start = data.find('sunrise:')
    end = data.find('</', start)

    return data[start + len('sunrise: '):end]


def find_geography(filename):
    fp = open(filename)
    fp = fp.read()

    start_tag = 'class="location center-text-xs margin-bottom"'
    content_index_start = fp.find(start_tag)  # find inner container start
    content_index_end = fp.find('</strong>', content_index_start)  # inner container end
    zip_code = fp[content_index_end - 5:content_index_end]  # get zip through slicing
    city = fp[content_index_start + len(start_tag) + len(
        '<strong> '):content_index_end - 12]  # get location through more slicing

    location = zip_code + ': ' + city[:-1]

    return location


def find_current_temperature(filename):
    fp = open(filename, 'r', encoding='UTF-8')
    fp = fp.read()

    start_tag = 'temp: '
    # find start of content and end of container
    content_index_start = fp.find(start_tag)
    content_index_end = fp.find('</div>', content_index_start)

    # slice out temp and return it
    temperature = fp[content_index_start + len(start_tag):content_index_end - 5]

    return temperature


def find_feels_like_temperature(filename):
    fp = open(filename, 'r', encoding='UTF-8')

    data = fp.read()

    start = data.find('feelsLike:')
    end = data.find('</', start)

    return int(data[start + len('feelsLike:'):end - 5])


def main():
    test = Module3()

    zipp = 48734

    test.sort_states_descending('data.csv', 'data_sorted.csv')
    print(test.extract_url_protocol('https://ww.google.com'))
    print(test.find_sunrise_for_zip(zipp))
    print(test.find_geography_for_zip(zipp))
    print(test.find_current_temp_for_zip(zipp))
    print(test.find_feels_like_temp_for_zip(zipp))


if __name__ == '__main__':
    main()
