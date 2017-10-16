import itertools
import re

if __name__ == "__main__":
    inputInteger = input()
    ipAddressArray = []
    outputArray = []

    # RegEx pattern for valid IP address
    pattern = re.compile('''
            ^
            ([2][0-5][0-5]|^[1]{0,1}[0-9]{1,2})     
            \.                                      
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})    
            \.                                      
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})    
            \.                                      
            ([0-2][0-5][0-5]|[1]{0,1}[0-9]{1,2})
            $
            ''', re.VERBOSE)
    
    noOfDigits = len(inputInteger)

    # Check if no of digits is min 4 and max 12
    # Smallest IP address has 4 digits eg. 1.1.1.1
    # Largest IP address has 12 digits eg. 255.255.255.255
    if 4 <= noOfDigits <= 12:
        # Array containing valid indices
        indexArray = range(1,noOfDigits)

        # Generates non-repetitive combinations of 3 indices where '.' can be inserted
        indexCombinationsArray = list(itertools.combinations(indexArray,3))
        
        # Uncomment following lines to print index combinations array
        #print(indexCombinationsArray)
        #print("")

        # Insert 3 '.' between digits of the input number to generate IP addresses
        for indexList in indexCombinationsArray:
            count = 0
            ipAddress = inputInteger
            for index in indexList:
                ipAddress = ipAddress[:index+count] + "." + ipAddress[index+count:]
                count += 1
            ipAddressArray.append(ipAddress)

        # Uncomment following lines to print all valid and invalid IP address
        #print(ipAddressArray)
        #print("")

        # Compaare list of all IP addresses to valid pattern to seperate valid IP addresses 
        for ipAddress in ipAddressArray:
            if re.match(pattern,ipAddress):
                outputArray.append(ipAddress)

        print(outputArray)
    else:
        print(outputArray)
