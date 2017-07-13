
file_name = './error.txt'
result_name = './Result/new_asin.txt'

# file_name = './error.txt'
# result_name = './new_asin.txt'

result_file = open(result_name,'w')

error_asin = []
for error_file in open(file_name,'r').readlines():
    error_file = error_file.split('[')[1]
    error_file = error_file.split(']')[0]
    error_file =  error_file.replace('\\n','')
    error_file = error_file.replace(',','\n')
    error_file = error_file.replace("'","").replace('"','').replace(' ','')
    print (error_file)
    result_file.write('\n'+error_file)