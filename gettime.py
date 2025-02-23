from bs4 import BeautifulSoup
import json
import os

# opens the folder directory that holds the ASPX files of interest
directory = "/Users/beaumaldonado/Desktop/course info"
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        # takes the name of the file for ease of reassigning later on
        fileReassign = filename[:-5]
        # joins the file name and type with the directory path.
        filePath = os.path.join(directory, filename)
        # the raw HTML data read from the ASPX file, raw HTML files range from ~1500 lines to ~30000 lines long.
        with open(filePath) as fp:
            soup = BeautifulSoup(fp, features="html.parser")

        j = 1
        courseidlist = list()
        coursetimelist = list()
        coursedaylist = list()
        CourseIdTime = list()
        courseid = soup.find_all(id="CourseTitle")
        coursetime = soup.find_all(lambda tag: tag.has_attr('style') and "padding-left: 5px;" in tag['style'])
        courseday = soup.find_all(
            lambda tag: tag.has_attr('style') and 'text-align: left; vertical-align: middle;' in tag['style'])
        # looping over just the course IDs and Times because they have less raw attributes.
        for i in range(len(courseid)):
            courseidlist.append(courseid[i].text[29:42].replace("\n", ''))
            coursetimelist.append(coursetime[i].text[29:46].replace("\n", ''))
        # messier raw data means the days must be looped over by themselves.
        for i in range(len(courseday)):
            while j < len(courseday):
                coursedaylist.append(courseday[j].text.strip())
                j += 3
        # merges the three lists into one single list.
        for i in range(len(coursetimelist)):
            CourseIdTime.append(courseidlist[i].replace(' ', '') + " " +
                                coursedaylist[i].replace(' ', '') + " " +
                                coursetimelist[i].replace(' ', ''))
        # for i in range(len(CourseIdTime)):
        #     print(fileReassign, filePath)
        print(filePath, fileReassign)

        # coverts the list into a structured and cleaned json file.
        # filepath = fileReassign + '.json'
        # with open(filepath, 'w') as outputfile:
        #     json.dump(CourseIdTime, outputfile, indent=2)


# with open("/Users/beaumaldonado/Desktop/course info/Anthro.aspx") as fp:
#     soup = BeautifulSoup(fp, features="html.parser")

# j = 1
# days = ['M', 'T', 'W', 'R', 'F']
# courseidlist = list()
# coursetimelist = list()
# coursedaylist = list()
# CourseIdTime = list()
# courseid = soup.find_all(id="CourseTitle")
# coursetime = soup.find_all(lambda tag: tag.has_attr('style') and "padding-left: 5px;" in tag['style'])
# courseday = soup.find_all(lambda tag: tag.has_attr('style') and 'text-align: left; vertical-align: middle;' in tag['style'])
# for i in range(len(courseid)):
#     courseidlist.append(courseid[i].text[29:42].replace("\n", ''))
#     coursetimelist.append(coursetime[i].text[29:46].replace("\n", ''))
# for i in range(len(courseday)):
#     while j < len(courseday):
#         coursedaylist.append(courseday[j].text.strip())
#         j += 3

# for i in range(len(coursetimelist)):
#     CourseIdTime.append(courseidlist[i].replace(' ', '') + " " +
#                         coursedaylist[i].replace(' ', '') + " " +
#                         coursetimelist[i].replace(' ', ''))
#
# for i in range(len(CourseIdTime)):
#     print(CourseIdTime[i])


# with open(File_Path, 'w') as outputfile:
#     json.dump(CourseIdTime, outputfile, indent=2)
