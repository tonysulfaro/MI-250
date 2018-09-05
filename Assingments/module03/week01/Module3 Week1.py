import sys
import requests
from csv import *
from lxml import html
from bs4 import BeautifulSoup


class Module3:
    """Module 3 Questions"""

    '''
        22. Define a function which extracts the geographic location and ZIP code out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        geographic location and ZIP code. To make this task slightly harder, return the ZIP code first 
        followed by the name of the city.

        Eg.
        48823: East Lansing, MI
        20003: Washington, DC

        Here is a small extract example of what the HTML file looks like
        <div class="pull-xs-left padded left-pane">
            <div class="location center-text-xs margin-bottom"><strong>East Lansing, MI &nbsp; 48823</strong></div>
            <div class="center-text-xs pull-md-left margin-bottom">
                <div class="tempurature large-temperature pull-xl-left">69</div>
                <div class="margin-top large hidden-lg-down pull-xl-left weather weather-21" style="width: 3rem;"></div>
                <div class="clearfix"></div>
                <div class="font-nav uppercase feels-like">Feels like <span class="temperature">69</span></div>
            </div>
            <div class="center-text-xs pull-md-right margin-bottom">
                <div><strong>High:</strong> <span class="temperature">82</span> | <strong>Low:</strong> <span class="temperature">66</span></div>
                <div><strong>Chance of rain:</strong> 10%</div>
                <div><strong>Wind:</strong> S at 10 mph</div>
            </div>
            <div class="clearfix"></div>
            <p>
                Night: A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</p>
            <p>
                <span><strong>Tonight:</strong></span>
                A few passing clouds. Low 66F. Winds SSE at 5 to 10 mph.</p>
        </div>
    '''

    @staticmethod
    def find_geography(filename):
        '''#location data is in the div containers
            <div> class = location center-text-xs margin-bottom -> <strong> (location)'''

        response = requests.get(filename)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        location = html_soup.find_all('div', class_ = 'location')[0]


        print(response)
        print(location)
        print(location.div)

        return filename

    '''
        38. Given a URL, use string functions to extract and return the path and filename components

        E.g. /images/profile.jpg
    '''

    @staticmethod
    def extract_url_path(url):
        return url

    '''
        17. Define a function which extracts the the name of the meteorologist out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        name of the meteorologist.

        Here is a small extract example of what the HTML file looks like
        <div class="met-name">
            <div class="affiliate-logo">
                <img src="/rw/PortalConfig/np-free/assets/ajc/images/weatherlogo-affiliate.png" />
            </div>
            <div class="met-title-text-1">FORECAST BY</div>
            <div class="met-title-text-2">METEOROLOGIST</div>
            <div class="met-name-text">Brad Nitz</div>
        </div>
    '''

    @staticmethod
    def find_meteorologist(filename):
        return filename

    '''
        33. HARD - Create a new CSV file which contains the name of each state and the corresponding population
        sorted from smallest to largest population.

        Hint: You may want to create a few different functions or use some of the other functions
        for this function to call!
    '''

    @staticmethod
    def sort_states_ascending(openfile, savefile):
        #open file to read in data
        readfile = open(openfile, 'r')
        readfile.readline()

        output_list = []

        #load to list sorted
        for line in readfile:

            line = line.strip('\n').strip()
            line = line.split(',')

            state = line[0]
            population = line[1]
            state_tup = (state, int(population))

            output_list.append(state_tup)

        readfile.close()

        output_list.sort(key=lambda x: x[1])

        #write to outfile
        
        outfile = open(savefile, 'w')

        for element in output_list:
            write_string = element[0]+','+str(element[1])+'\n'
            outfile.writelines(write_string)

        outfile.close()

        return None

    '''
        15. Define a function which extracts the the current temperature out of an HTML file.
        The file name will be passed in as the parameter value, the function should simply return the
        current temperature \u2013 just the numerical value not including the units.

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
    def find_current_temperature(filename):
        return filename

    '''
        40. Given a URL, open the webpage and return only the title of the webpage.
        Some websites may use capitals for html tags and some maynot.
        If no tag exists, return None
        For the purpose of this task, convert everything to lowercase to avoid this issue.

        Hint: calling read() on a connection returns utf8 encoded bytes,
            you will also need to decode these to convert it into a normal string
    '''

    @staticmethod
    def extract_url_title(url):
        return url

    '''
        35. Given a URL, open the webpage and save the HTML to a given file path.

        Hint: calling read() on a connection returns utf8 encoded bytes,
            you will also need to decode these to convert it into a normal string
    '''

    @staticmethod
    def save_url_to_file(url, savefile):
        return url

    '''
        12. Using file and string functions, write your own function to open a file.
        Once you have the content of the file, search for the text "REPLACE ME" and 
        replace it with the persons name provided as a parameter.

        Finally, save the changes to the savefile location.
    '''

    @staticmethod
    def modify_text_file(openfile, savefile, name):
        #assumes that REPLACE ME is actually in there
        
        #here is my method
        '''
        readfile = open(openfile, 'r')
        output = []

        for line in readfile:
            
            line = line.split()

            print(line)
            
            output.extend(line)

        print(output)
        r_index = output.index('REPLACE')

        if r_index != -1:
            if output[r_index+1] == 'ME':
                output.pop(r_index)
                output.pop(r_index)
                output.insert(r_index, name)

        readfile.close()

        #write string to file
        outfile = open(savefile, 'w')

        for element in output:
            outfile.write(element+' ')
        '''

        #aaand then stackoverflow
        #attribution: https://stackoverflow.com/a/17141572

        # Read in the file
        with open(openfile, 'r') as filee:
            filedata = filee.read()

        # Replace the target string
        filedata = filedata.replace('REPLACE ME', name)

        # Write the file out again
        with open(savefile, 'w') as filee:
            filee.write(filedata)


    '''
        27. Given a file (structured the same as census-state-populations.csv but not necessarily real states) 
        return the total population estimation sum across all states and districts
        that start with the letter M.
    '''

    @staticmethod
    def total_population_for_m_states(filename):

        population_total = 0
        readfile = open(filename, 'r')
        readfile.readline()

        for line in readfile:
            line = line.strip('\n').strip()
            line = line.split(',')

            region = line[0]
            population = int(line[1])

            region = region.lower()
            if region[0] == 'm':
                population_total += population

        readfile.close()

        if(population_total > 0):
            return population_total
        return -1

    '''
        8. Using file and string functions, write your own function to determine the first position of a
        character (provided as a parameter) within a file based on a filepath. You will need to open the file
        and then determine the index of the character within the text file.
    '''

    @staticmethod
    def first_index_in_file(filepath, character):

        index = 0

        readfile = open(filepath, 'r')

        for line in readfile:
            line = line.strip('\n').strip()

            for char in line:
                print(char)
                index +=1

                if char == character:
                    return index

        readfile.close()

        return -1 #char does not exist in file

def main():
    output = Module3()
    #output.find_geography('https://weather.com/weather/today/l/East+Lansing+MI+48823:4:US')

    #output.sort_states_ascending('/Users/tonysulfaro/Documents/GitHub/MI-250/Assingments/module03/data/census-state-populations.csv','/Users/tonysulfaro/Documents/GitHub/MI-250/Assingments/module03/data/sorted_states_ascending.csv')
    print(output.modify_text_file('/Users/tonysulfaro/Documents/GitHub/MI-250/Assingments/module03/data/lorem_1.txt', '/Users/tonysulfaro/Documents/GitHub/MI-250/Assingments/module03/data/lorem_1_out.txt', 'replaced'))

if __name__ == "__main__":
    main()