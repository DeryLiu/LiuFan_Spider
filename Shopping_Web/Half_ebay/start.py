import config
import os
import reload
import select

def modify_config(opt):
    f=open('config.py')
    lines=f.readlines()
    f.close()
    lines[1]="opt='"+opt[0].replace('&amp;','').replace(',','').replace(' ','')+"|"+opt[1]+"'\n"
#     lines[2]="page="+page+"\n"
    f=open('config.py','w')
    f.writelines(lines)
    f.flush()
    f.close()
    reload(config)
    command="sed -n '2,6p' config.py"
    lines=os.popen(command).read()
    print (lines)

def modify_page_config(begin,end):
    f=open('config.py')
    lines=f.readlines()
    f.close()
    lines[3]="begin_num='"+begin+"'\n"
    lines[4]="end_num='"+end+"'\n"
    f=open('config.py','w')
    f.writelines(lines)
    f.flush()
    f.close()
    reload(config)
    command="sed -n '2,6p' config.py"
    lines=os.popen(command).read()
    print (lines)
'''
    选择判断
'''
def judge(input_num):
    if input_num=='':
        exit()
    input_num=int(input_num)
    if input_num in range(1,3):
        return 1
    else:
        return 0
def select_program():
    print ("1 get_book_listing.py\n2 get_book_html.py")
    num = input('Select program:')
    if judge(num):
        return num
    else:
        print ('Input number is not legal, please re-enter.')
        select_program()
    
if __name__ == '__main__':
#     start=select_program()
#     if start=='1':   
#         opt=select.select_category()
#         page=raw_input('input page number:')
#         print 'have selected:',opt[0],page
#         choice=raw_input('execute(y/n)?\n')
#         if choice=='y':
#             modify_config(opt,page)
#             os.system('nohup python get_book_listing.py &')
#     else:
#         numbers=select.input_num()
#         print numbers
#         modify_page_config(numbers[0],numbers[1])
#         os.system('nohup python get_book_html.py &')

    opt=select.select_category()
    print ('have selected:',opt[0])
    choice = input('execute(y/n)?\n')
    if choice=='y':
        modify_config(opt)
        os.system('nohup python get_book_url.py &')
