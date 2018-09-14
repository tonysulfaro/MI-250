import sys
import requests
from csv import *
from bs4 import BeautifulSoup


class Module3:
    """Module 3 Questions"""

    '''
        13. Using file and string functions, write your own function to open a CSV file and determine how many columns
        of data are in the file

        Note: The CSV files have been randomly generated from https://www.mockaroo.com/
    '''

    @staticmethod
    def csv_column_count(openfile):

        fp = open(openfile)
        line = fp.readline()

        if line: # if there is data
            return line.count(',')+1 # plus one is for offset from csv, one comma means two columns

        return -1

    '''
        7. Given a string, write a function that returns the original string and ensures the number of characters is 
        always 50. It should do this by adding a symbol (provided as a parameter) as many times as necessary to the
        END of the string to make the total character count 50.

        Example:
        Module3.right_pad("Hi there, this should have X's on the right", 'X') 
        returns
        "Hi there, this should have X's on the rightXXXXXXX"

        Module3.right_pad("This should have X's on the right", 'X') 
        returns
        "This should have X's on the rightXXXXXXXXXXXXXXXXX"
    '''

    @staticmethod
    def right_pad(text, symbol):

        size = len(text)

        if size >= 50:
            return text[:50] # if its longer than 50

        return text + ((50-size)*symbol) # shorter than 50 fill in to right

    '''
        11. Using file and string functions, write your own function to open a file and copy the
        content into a new file. Both file locations will be given as parameters.
    '''

    @staticmethod
    def copy_file(openfile, savefile):

        # 90% sure you just save a file to a new location??
        old_data = open(openfile, 'r')
        file_data = old_data.read()
        old_data.close()

        new_data = open(savefile, 'w')
        new_data.write(file_data)
        new_data.close()

        return None

    '''
        10. Using file functions, save the text provided in the first parameter to the file location 
        provided in the second parameter
    '''

    @staticmethod
    def save_file(text, savefile):

        # pipe string to text file
        fp = open(savefile, 'w')
        fp.write(text)
        fp.close()

        return None

    '''
        6. Given a string, write a function that returns the original string and ensures the number of characters is 
        always 50. It should do this by adding a symbol (provided as a parameter) as many times as necessary to the
        BEGINNING of the string to make the total character count 50.

        Example:
        Module3.left_pad("Hello there, this should have dashes on the left", '\u2013') 
        returns
        "--Hello there, this should have dashes on the left"

        Module3.left_pad("This should have dashes on the left", '\u2013') 
        returns
        "---------------This should have dashes on the left"
    '''

    @staticmethod
    def left_pad(text, symbol):

        size = len(text)

        if size >= 50:  # larger than 50 chop it. Says that its always 50.
            return text[50:]

        return ((50-size)*symbol) + text  # add symbol to left to make it 50

    '''
        4. Refresher Question: Return the number of comma's in a text file given the filepath as a parameter
    '''

    @staticmethod
    def file_comma_count(filepath):

        # read in file data then just do a count on the number of commas
        fp = open(filepath, 'r')
        data = fp.read()
        count = data.count(',')
        fp.close()

        return count

    '''
        36. Given a URL, open the webpage and save the CSV to a given file path.
    '''

    @staticmethod
    def save_url_to_csv_file(url, savefile):

        file = requests.get(url).text
        fp = open(savefile, 'w')
        fp.write(file)
        fp.close()

        return url

    '''
        19. Define a function which extracts the low temperature out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        low temperature \u2013 just the numerical value not including the units or spaces.

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
    def find_days_low(filename):

        # basically im going to get that container by id and then im going to
        # have to slice it because the temperature div doesnt have any unique attributes.
        # so get the container then slice it out. Jank but works.

        soup = BeautifulSoup(open(filename), "html.parser")
        weather_data = str(soup.find("div", {"id": "todayData"}))

        # find index of container beginning and end
        index = weather_data.find('lowTemp:')
        end = weather_data.find('</div>', index)

        return weather_data[end-3:end-1]  # slice to get content of container out

    '''
        44. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE
        and extract the chance of rain.
        
        The ZIP code will be passes in as a parameter value, the function should simply return the
        chance of rain \u2013 the numerical value and the % sign

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
    def find_rain_chance_for_zip(zipcode):

        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")  # parse page
        weather_data = str(soup.find("div", {"id": "todayData"}))  # get div by id

        # find index of container beginning and end
        index = weather_data.find('precipChance:')
        end = weather_data.find('</div>', index)

        return weather_data[end - 3:end]  # slice to get content of container out

    '''
        47. Given a ZIP code, pull the current weather from https://www.ajc.com/weather/ZIPCODE/ 
        and use your previous function to extract and return the days lowest temperature
        
        Hint: the other functions require files, you will need to save the HTML as a temp file
        then process it.
        
        Dependencies: Module3.save_url_to_file, Module3.find_days_low
    '''
    @staticmethod
    def find_lowest_temp_for_zip(zipcode):

        # The save_url_to_file wasn't in my problemset so I made one.

        url = 'https://www.ajc.com/weather/' + str(zipcode) + '/'
        filename = 'low_temp.html'
        save_url_to_file(url, filename)

        # it couldn't see the find_days_low function within the same class so i
        # made an instance of it and used it that way. Kinda Effective
        test = Module3()
        return test.find_days_low(filename)


def save_url_to_file(url, filename):

    page = requests.get(url).text
    fp = open(filename, 'w')
    fp.write(page)
    fp.close()


def main():

    test = Module3()

    # print(test.csv_column_count('data.csv'))

    # right_pad_result = test.right_pad("This should have X's on the right", 'X')
    # assert right_pad_result == "This should have X's on the rightXXXXXXXXXXXXXXXXX")

    # left_pad_result = test.left_pad('this is some text','-')
    # print(left_pad_result, len(left_pad_result))

    #test.find_lowest_temp_for_zip(48823)
    # test.save_url_to_csv_file('http://cognosis.cas.msu.edu/public/mi250/module3/attachments/census-state-populations.csv','data.csv')

    # print(test.file_comma_count('data.csv'))

    #print(test.find_days_low('weather_low.html'))

    #print(test.find_lowest_temp_for_zip(48823))


if __name__ == '__main__':
    main()
