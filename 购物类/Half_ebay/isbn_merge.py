from fileinput import filename



def merge(filename1,filename2):
    file1=open(filename1)
    file2=open(filename2)
    isbnList1=file1.readlines()
    isbnList2=file2.readlines()
    isbnDict1={}
    isbnDict2={}
    for isbn in isbnList1:
        isbnDict1[isbn]=""
    for isbn in isbnList2:
        isbnDict2[isbn]=""
    for key in isbnDict1:
        isbnDict2[key]=""
    result_file=open("./update/isbn/isbns_result.csv","w")
    for key in isbnDict2:
        result_file.write(key)
        


if __name__=="__main__":
    merge("./update/isbn/isbns_0926.csv", "./update/isbn/isbns.csv")