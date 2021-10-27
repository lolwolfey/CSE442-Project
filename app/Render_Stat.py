"""
Uses the templet (TemStats.html) to change the id on the statistics page to the current youtuber the user is seeing on the statistics page
    
    - Opens the html file and reads it line by line and replaces the placeholder text {{Youtube_Id}} with the youtuber's id
    - It then replaces the current Stats page to teh new one for the user

"""


def Render_Stat_Page(ID):
    template = open('/Users/ryano/source/repos/CSE442-Project/app/templates/TempStats.html', "r")
    page = ""
    for line in template:
        if '{{Youtube_Id}}' in line:
            page = page + line.replace("{{Youtube_Id}}", ID)
        else:
            page = page + line
    template.close()
    
    new = open("/Users/ryano/source/repos/CSE442-Project/app/templates/Stats.html", "w")
    new.write(page)
    new.close()

if __name__ == "__main__":
    Id = 'UCupvZG-5ko_eiXAupbDfxWw'
    Render_Stat_Page(Id)