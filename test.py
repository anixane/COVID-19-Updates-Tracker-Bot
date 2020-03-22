import pymsteams
import json2table

# declare here or rather import from a file
DEFAULT_TEAMS_WEBHOOK = ''


jsoninfo = {
    'Developer': 'Animesh',
    'Project': 'Corona Updates'
}

build_direction = "LEFT_TO_RIGHT"
table_attributes = {"style": "width:100%"}
txt = json2table.convert(jsoninfo,
                         build_direction=build_direction,
                         table_attributes=table_attributes)

myTeamsMessage = pymsteams.connectorcard(DEFAULT_TEAMS_WEBHOOK)
myTeamsMessage.text(str(txt))
myTeamsMessage.send()
