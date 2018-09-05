"""
sulfaroa
9/5/18
In-Class Exercise
"""

import math

def print_wave(num_rows, num_cols):

    outfile = open('./Assingments/module03/week01/sulfaroa.inclass.output.csv', 'w')

    for x in range(num_rows):
        x_location = math.sin(math.radians(x/num_rows)*360)

        #find x location in columns
        tmp_location = int(x_location*(num_cols/2)+(num_cols/2))

        line = ''

        #generate row with x in place
        for y in range(num_cols):
            if y == tmp_location:
                line+= 'X,'
            else:
                line += ','

        line += '\n'

        outfile.write(line)

    outfile.close()
        
def main():
    print_wave(31,60)

if __name__ == "__main__":
    main()