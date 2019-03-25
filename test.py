arguments = "synth dx7 -f -s Alpha -l VANCOUVER -p 200-300"

arg = arguments.split(" ")

print(arg)

sortType = "LowPrice"
filterLocation = ""
filterPrice = ""
filterFree = False

while (("-s" in arg) or ("-l" in arg) or ("-f" in arg) or ("-p" in arg)):
    for x in range(len(arg)):
        #print ("X: " + str(x))
        checked = False
        ## SORT
        try:
            if (('-s' in arg[x]) and (not checked)):
                #print(arg[x+1])
                sortType = arg.pop(x+1)
                arg.pop(x)
                checked = True
        except:
            pass

        ## FILTER LOCATION
        try:
            if (('-l' in arg[x]) and (not checked)):
                #print (arg[x+1])
                filterLocation = arg.pop(x+1)
                arg.pop(x)
                checked = True
        except:
            pass

        ## FILTER PRICE
        try:
            if (('-p' in arg[x]) and (not checked)):
                #print (arg[x+1])
                filterPrice = arg.pop(x+1)
                arg.pop(x)
                checked = True
        except:
            pass

        ## FILTER FREE
        try:
            if (('-f' in arg[x]) and (not checked)):
                #print(arg[x])
                filterFree = True
                arg.pop(x)
                checked = True
        except:
            pass


    ## Everything should be popped and only keywords left over
print ("-------------------------------------")
print(arg)
print ("-------------------------------------")
print ("Sort: " + sortType)
print ("FilterLocation: " + filterLocation)
print ("FilterPrice: " + filterPrice)
print ("FilterFree: " + str(filterFree))
print ("Keywords: " + str(arg))
