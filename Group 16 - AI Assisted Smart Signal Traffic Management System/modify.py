import random
import xml.etree.ElementTree as ET

# Load the routes file
tree = ET.parse('yourRoutes.rou.xml')
root = tree.getroot()

# Iterate over flow elements and change the begin and end attributes randomly
for flow in root.findall('flow'):
    begin = random.randint(0, 250)  # Random begin time between 0 and 250 (seconds)
    end = random.randint(begin + 1, 250)  # Random end time after the begin time
    
    flow.set('begin', str(begin))
    flow.set('end', str(end))

# Save the modified routes file
tree.write('modified_routes.xml')
