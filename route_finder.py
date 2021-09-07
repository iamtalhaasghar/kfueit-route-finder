#
# A simple Image to Text Conversion Program to demonstrate the Capabilites of PyTesseract
# 
# The code was last updated on May, 2019


def getBusesNames(routesPath):
    import os
    files = list()
    
    for i in os.listdir(routesPath):
        if(i.endswith('.txt')):
            files.append('%s/%s' % (routesPath, i))

    busesNames = dict()
    prohibited = ['/','\\','|','?','*',':','\"','<','>']
    for f in files:
        with open(f) as t:
            for line in t:
                if(line.startswith('HINO') or line.startswith('COASTER') or line.startswith('BUS')):
                    temp = os.path.basename(f).split('.')[0]
                    line = line.strip()
                    for c in prohibited:
                        if(c in line):
                            line = line.replace(c, '')
                    busesNames[temp] = line
    return busesNames


def renameFiles(folderPath,extension, newNames):
    import os
    files = list()
    for f in os.listdir(folderPath):
        if(f.endswith(extension)):
            files.append('%s/%s' %(folderPath, f))

    for i in files:
        temp = os.path.basename(i).split('.')[0]
        os.rename(i, '%s/%s%s' %(folderPath,newNames.get(temp,temp),extension) )
    
    

def searchStopName(stopName, routesPath):
    import os
    busesFound = list()
    allBuses = list()
    for file in os.listdir(routesPath):
        if(file.endswith('.txt')):
            
            allBuses.append(file.split('.txt')[0])
            file = '%s/%s' % (routesPath,file)
            with open(file, 'r') as f:
                for line in f:
                    if(stopName.lower() in line.lower()):
                        bus = os.path.basename(file).split('.txt')[0]
                        busesFound.append(bus)
                        break;

    notGoing = [allBuses[i] for i in range(len(allBuses)) if allBuses[i] not in busesFound]
    print('Stop Name: ',stopName)
    print('Going: ',busesFound)
    print('Not: ',notGoing)
    return busesFound

def getAllBusesRoutesPath():
    import os
    pathList = list()
    p = '%s/%s' % (os.getcwd(), 'routes')
    for f in os.listdir(p):
        if f.endswith('.jpg'):
            pathList.append('%s/%s'%(p,f))
    return pathList


def startOcrScan(imagesList):
    from PIL import Image
    import pytesseract
    import os

    p = '%s/%s' %(os.getcwd(),'scan_results')
    total = len(imagesList)
    print('Total images: %s' % len(imagesList))
    if(not os.path.exists(p)):
        os.mkdir(p)
    for img in imagesList:
        print('Images to Scan : %s' % total)
        print('Scanning : %s ...'% os.path.basename(img))
        i = Image.open(img)
        text = pytesseract.image_to_string(i)
        print('Saving ocr scanned text...')
        f = open('%s/%s.txt' % (p, os.path.basename(img).split('.jpg')[0]), 'w')
        f.write(text)
        f.close()
        total -= 1


if __name__ == "__main__":
    import os
    
    routes = getAllBusesRoutesPath()
    startOcrScan(routes)
    buses = getBusesNames('%s/%s' % (os.getcwd(), 'scan_results'))
    renameFiles('%s/%s' % (os.getcwd(), 'scan_results'), '.txt', buses)
    renameFiles('%s/%s' % (os.getcwd(), 'routes'), '.jpg', buses)
    

    s = input('Enter stop name: ')
    t = searchStopName(s,'%s/%s' % (os.getcwd(), 'scan_results'))

