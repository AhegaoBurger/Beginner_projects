from datetime import datetime

command = input('Are you in: ')
if command == 'Yes':
    start = open('D:\\Artur\\Database\\logins.csv', 'a')
    start.write('in,%s\n' % (datetime.now()))
    start.close()

elif command == 'No':
    end = open('D:\\Artur\\Database\\logins.csv', 'r')
    lines = end.readlines()
    date_login = lines[-1].replace('\n', '').split(',')[1]
    now = datetime.now()
    duration = now - datetime.strptime(date_login, '%Y-%m-%d %H:%M:%S.%f')
    print(duration)
    out = open('D:\\Artur\\Database\\logins.csv', 'a')
    out.write('out,%s\n' % str(now))
    out.close()
    # print(lines[-2].replace('\n', '').split(',')[1], lines[-1].replace('\n', '').split(',')[1])
    # date_login = lines[-2].replace('\n', '').split(',')[1]
    # date_logout = lines[-1].replace('\n', '').split(',')[1]
    # print(datetime.strptime(date_logout, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(date_login, '%Y-%m-%d %H:%M:%S.%f'))

    # end.write('out,%s\n' % (datetime.now()))
    # exit = end.write(str(datetime.now()))
    # timing = open('D:\\Artur\\Database\\text.txt', 'rb')
    # print(datetime.combine(date.today(), exit) - datetime.combine(date.today(), enter))
    # timing.close()
    end.close

    
# print(datetime.combine(date.today(), exit) - datetime.combine(date.today(), enter))
# answer = open('D:\\Artur\\Database\\text.txt', 'r')
# print(answer.readlines())
# answer.close()