import pyperclip,sys,csv,pprint

CSV_path = r'D:\coding\allcodes\codes\py_all\password_recorder\pwd_list.csv'
pwd_config = open(CSV_path,'r')
pwd_data_config = list(csv.reader(pwd_config))
pwd_data = [i for i in pwd_data_config if len(i) == 2] # 这一步的操作清空了原始数据中的空行等内容，使其每一项都是有意义的数据
pwd_config.close()
yes = ('y','yes','yes.')
keyphrase = sys.argv[1].upper() if len(sys.argv) >=2 else None
app,pwd = [e[0].strip() for e in pwd_data],[e[1].strip() for e in pwd_data]

# 处理csv
def open_csv_a(index0,index1):
    with open(CSV_path, 'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([index0, index1])

def open_csv_w():
    with open(CSV_path, 'w') as f:
        writer = csv.writer(f)
        for i in range(len(pwd_data)):
            writer.writerow([pwd_data[i][0],pwd_data[i][1]])

# 主要逻辑
# 允许用户通过'pwd app save password'的形式快速存储密码，若输入的app已存在，则提示用户是否覆盖原密码
def add_pwd():
    if keyphrase not in app:
        open_csv_a(keyphrase,sys.argv[3])
        pyperclip.copy(sys.argv[3])
        print('Successfully saved and copied.')
    elif keyphrase in app:
        answer = input('The account is saved.Replace it?(y/n)')
        if answer in yes:
            pwd_data[app.index(keyphrase)][1] = sys.argv[3]
            open_csv_w()
            pyperclip.copy(sys.argv[3])
            print('Successfully replaced!')
            print(f'I\'ve copy this for you,you can paste it in which you want,and what I copy is {sys.argv[3]}.')

# 在用户使用指令但是不对应任何有意义的操作时
def forced_to_add_pwd():
    answer = input('The account isn\'t in your password book yet.Would you like to save it?(y/n)').lower()
    if answer in yes:
        new_pwd = input(f'Enter password for {keyphrase}: ')
        open_csv_a(keyphrase,new_pwd)
        app.append(keyphrase)
        pwd.append(new_pwd)# 添加新密码
        pyperclip.copy(pwd[app.index(keyphrase)])
        print(f'Successfully saved!\nI\'ve copy this for you,you can paste it in which you want,and what I copy is {pwd[app.index(keyphrase)]}.')

def change_pwd():
    if keyphrase in app:
        pwd_data[app.index(keyphrase)][1] = sys.argv[3]# 更改密码本的数据，以便重写密码本
        open_csv_w()
        pyperclip.copy(sys.argv[3])
        print(f'Successfully replaced!\nI\'ve copy this for you,you can paste it in which you want,and what I copy is {sys.argv[3]}.')
    else:
        answer = input('The account isn\'t in your password book yet.Would you like to save it?(y/n)').lower()
        if answer in yes:
            open_csv_a(keyphrase,sys.argv[3])
            pyperclip.copy(sys.argv[3])
            print(f'Successfully saved!\nI\'ve copy this for you,you can paste it in which you want,and what I copy is {pwd[app.index(keyphrase)]}.')

# 执行删除部分代码的操作
def delete():
    if keyphrase in app:
        pwd_data.remove(pwd_data[app.index(keyphrase)])
        open_csv_w()
        print('Successfully deleted!')
    else:
        print(f'There\'s no {keyphrase} in the password book.')

length = len(sys.argv)

# 主程序逻辑
if length <=1:
    print('Sorry,you didn\'t tell me what to do!')
elif length >= 4 and sys.argv[2] == 'save':
    add_pwd()
elif length >= 4 and sys.argv[2] == 'change':
    change_pwd()
elif keyphrase == 'LIST':
    pprint.pprint(pwd_data)
    print('Here is all.')
elif length >= 3 and sys.argv[2] == 'delete':
    delete()
elif keyphrase in app:
    pyperclip.copy(pwd[app.index(keyphrase)])
    print(f'I\'ve copy this for you,you can paste it in which you want,and what I copy is {pwd[app.index(keyphrase)]}.')
else:
    forced_to_add_pwd()
