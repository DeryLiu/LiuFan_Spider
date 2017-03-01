import datetime

def filter_new_asin(filename):
    
    print ("filter_new_asin start:" , datetime.datetime.now())
    asins_file=open(filename)
    asins_lines=asins_file.readlines()
    asins={}
    for asins_line in asins_lines:
        asins[asins_line]=""
        
    allasins_file=open("./update/isbn/allasins.txt")
    allasins_lines=allasins_file.readlines()
    allasins={}
    for allasins_line in allasins_lines:
        allasins[allasins_line]=""
        
    newasins_file=open("./snatch/asin/asins.csv","w")
    count=0
    for key in asins:
        if key not in allasins:
            newasins_file.write(key)
            count+=1
    print ("newasins numbers:",count)
    print ("filter_new_asin end:" , datetime.datetime.now())
    
    
if __name__=="__main__":
    id="10955"
    filter_new_asin("./asin_result/"+id+"/asins_more.txt")