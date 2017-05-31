import time, DAN, requests, random, DogFrequency, json
from datetime import datetime #In case we want to show current time 
from optparse import OptionParser

ServerIP = '127.0.0.1' #Change to your IoTtalk IP or None for autoSearching
addr =  '%030x' % random.randrange(16**30)
#print(addr)
Reg_addr=addr # if None, Reg_addr = MAC address_from=''
_from=''
_to=''
_id=''

class json_data(object):
    def __init__(self, TrackerID, N, E, time):
        self.TrackerID = 0
        self.N = "0"
        self.E = "0"
        self.Time = "0"   

def new_submit(submit):
    if _from==['from'] and _to==['to']:
        return True
    else:
        return False

def Push_Data(args):   
    if args['id']==0:
        queryResult = DogFrequency.getLatLngOrder('Tracker_0035', args)
    elif args['id']==2:
        queryResult = DogFrequency.getLatLngOrder('追蹤器_34', args)
    i = 0
    while True:
        try:	#2017-05-25T14:55:13.000Z
		#2017/05/01 02:37
            #Pull data from a device feature called "Dummy_Control"            
            control = DAN.pull('AskForDogData-O')
            control = control[0];
            args['From'] = control['From'][0:4]+'-'+control['From'][5:7]+'-'+control['From'][8:10]+'T'+control['From'][11:16]+':00.00Z'
            _from=args['From']
            args['To'] = control['To'][0:4]+'-'+control['To'][5:7]+'-'+control['To'][8:10]+'T'+control['To'][11:16]+':00.00Z'
            _to=args['To']
            if new_submit(control):
                Push_Data(args)
            if i < len(queryResult):
                jsonData = {}
                if args['id']==0:
                    tempID = str(0)
                else:
                    tempID = str(2)
                if args['mode'] == 0:
                    tempID = tempID + "0"
                else:
                    tempID = tempID + "1"
                jsonData['TrackerID'] = tempID
                jsonData['N'] = queryResult[i][1]
                jsonData['E'] = queryResult[i][2]
                jsonData['Time'] = queryResult[i][0]
                print("Pushing Data...")
                print(jsonData)
                DAN.push ('DogData-I', jsonData)
                i = i + 1
            else :
                i = 0
                jsonData = {}
                if args['id']==0:
                    jsonData['TrackerID'] = 0
                else:
                    jsonData['TrackerID'] = 2
                jsonData['N'] = queryResult[i][1]
                jsonData['E'] = queryResult[i][2]
                jsonData['Time'] = queryResult[i][0]
                print("Pushing Data...")
                print(jsonData)
                DAN.push ('DogData-I', jsonData)
                i = i + 1        
        except Exception as e:
            print(e)
            DAN.device_registration_with_retry(ServerIP, Reg_addr)

        if args['speed'] != None:
            time.sleep(args['speed'])
        else:
            time.sleep(1) 

        
        
    

def main():
    DAN.profile['dm_name']='SensorSystem'
    DAN.profile['df_list']=['DogData-I','AskForDogData-O']
    DAN.profile['d_name']= None # None for autoNaming
    DAN.device_registration_with_retry(ServerIP, Reg_addr)
    Dog_options, Dog_args = parse_args()
    if Dog_options.verbose:
        print (Dog_options.greeting % Dog_options.who + '\nTry -h to get more information.')
        print (datetime.now().strftime('%I:%M:%S %p'))
        Push_Data(Dog_args)
    #elif Dog_options.help():
    #    print (Dog_options.greeting % Dog_options.who )
    else:
        print (Dog_options.greeting % Dog_options.who + '\nTry -h to get more information.')  #In pythin3, "print" must follow "()"
        Push_Data(Dog_args)

def parse_args():
    usageStr = """
    %prog [OPTIONS] [WHO]
    Eat some shit bro
    """
    versionStr = """
    Dogdata 1.0
    """
    parser = OptionParser(usage=usageStr , version=versionStr)
    parser.add_option('-g', '--greeting', dest='greeting',    #Say hellow
                      default="Hi there! %s!",
                      help='Print "%default".',
                      metavar='MESSAGE')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',    #Current time
                      default=False,
                      help='Current time')
    parser.add_option('-s', '--speed',type = 'float', dest='speed',    #How fast we gona push the input data
                      default=1, #normal
                      help='How fast you want to push the input data? (Default = %default)')
    parser.add_option('-n', '--number',type = 'int', dest='number',    #How many data we want
                      default=100, 
                      help='How many data you want to push? (Default = %default)')
    parser.add_option('-m', '--mode',type = 'int', dest='mode',    #Which kind of data we want? sort by timestemp, frequence etc.
                      default=1, # (1: timestemp) (2:frequence)
                      help='1: Draw Line, 0: Do not Draw Line \n ')
                      #help='How kind of data you want? \n    1:Sort by timestemp(Default) \n    2:Sort by frequence')
    parser.add_option('-i', '--id',type = 'int', dest='id',    #How many data we want
                      default=0, 
                      help='Which dog you want to track?(Default:0)')
    parser.add_option('-f', '--from',type = 'str', dest='From',    
                      default=None, 
                      help='Get data from which index')
    parser.add_option('-t', '--to',type = 'str', dest='To',   
                      default=None, 
                      help='Get data till which index')
    
    options, args = parser.parse_args()

    if '%s' not in options.greeting:
        parser.error('-g options requires a placeholder %s in it.')
    #if len(args) > 1:
    #    parser.error('Error: Too many arguments.')
    options.who = 'Kaboo' #if len(args) == 0 else args[0]    # "who" is the person we want to talk to
    
    args = dict()
    args['speed'] = options.speed
    args['number'] = options.number
    args['mode'] = options.mode
    args['id'] = options.id
    args['From'] = options.From
    args['To'] = options.To
    #args['xx'] == options.xx

    if args['speed'] != None:
            speed_default = args['speed']

    if args['id'] != None:
            id_default = args['id']
        
    
    return options, args

if __name__ == '__main__':
    main()
