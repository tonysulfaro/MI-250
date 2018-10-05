import os
from PIL import Image


def generate_page(directory):
    fp = open('sulfaroa.inclass-test.html', 'w', encoding='UTF-8')

    content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Photos from Some Place</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
          integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
</head>

<body>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"
        integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49"
        crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"
        integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy"
        crossorigin="anonymous"></script>

<div class="row">
    <div class="col">
        <h1>
            Picture Library
        </h1>
        <p>
            Pictures from -> ''' + os.getcwd() + '''
        </p>
    </div>
</div>'''
    fp.writelines(content)

    # generate image containers now
    # image_dir = '/Users/tonysulfaro/Documents/GitHub/MI-250/Assingments/module03/week05/wednesday/inclass_images/'
    fp.writelines('<div class="row">')
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):

            im = Image.open(directory + '/' + filename)
            width, height = im.size
            info_header = '<p>' + directory + '/' + filename + ' ' + str(width) + 'x' + str(height) + '</p>'

            if count < 4:
                fp.writelines('''<div class="col-md-3">''' + info_header + '''
            <a href="''' + '' + os.path.join(directory, filename) + '''">
                <img src="''' + os.path.join(directory, filename) + '''" width="200px">
            </a>
        </div>''')
                count += 1

            else:
                fp.writelines('</div>')
                fp.writelines('<div class="row">')
                count = 0

            fp.writelines('\n')

            print(os.path.join(directory, filename))

    fp.writelines('</div>')
    end_tags = '''</body>
</html>'''
    fp.writelines(end_tags)


def main():
    generate_page('inclass_images')


if __name__ == '__main__':
    main()
