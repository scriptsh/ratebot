import requests
from bs4 import BeautifulSoup
import time
import os

dir_files = 'files'
doll_txt = dir_files + '/doll.txt'
euro_txt = dir_files + '/euro.txt'
dir_st = 'statictics'
st_doll = dir_st + '/st_doll.txt'
st_euro = dir_st + '/st_euro.txt'
yest_doll = dir_st + '/yest_doll.txt'
yest_euro = dir_st + '/yest_euro.txt'

def create_file_if_not_exist(name):
    if os.path.exists(name) == False:
        file = open(name, 'w')
        file.close()

def create_dir_if_not_exist(name):
    if os.path.exists(name) == False:
        os.mkdir(name)

def read_file(name):
    file = open(name, 'r')
    s = file.read()
    file.close()
    
    return s

def write_in_file(name, text):
    file = open(name, 'w')
    file.write(text)
    file.close()

create_dir_if_not_exist(dir_files)
create_dir_if_not_exist(dir_st)

create_file_if_not_exist(st_doll)
create_file_if_not_exist(st_euro)
create_file_if_not_exist(yest_doll)
create_file_if_not_exist(yest_euro)

# endless cycle which will update values of rate every 10 seconds
while True:

    #links to pages of real rates 
    page_doll_ru = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    page_doll_ukr = 'https://www.google.com/search?q=доллар+к+гривне&sxsrf=APq-WBth2GLgI7narVnKW9DluHMeO5B3Xw%3A1648293075646&ei=0_Q-YvLxJoP-rgTy9ofoCg&ved=0ahUKEwiyp4ma0uP2AhUDv4sKHXL7Aa0Q4dUDCA0&uact=5&oq=доллар+к+гривне&gs_lcp=Cgdnd3Mtd2l6EAMyCQgjECcQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMggIABCABBDJAzIFCAAQgAQyBQgAEIAEMgUIABCABDoHCAAQRxCwAzoKCAAQRxCwAxDJAzoHCAAQsAMQQzoECCMQJzoNCAAQgAQQhwIQsQMQFDoLCAAQgAQQsQMQgwE6BAgAEEM6BwgAELEDEEM6BwgAEMkDEEM6CAgAEIAEELEDOgcIABCABBAKOgcILhCABBAKOgoIABCxAxCDARBDOgoIABCABBCHAhAUOgcIIxCxAhAnOgQIABAKOgcIABDJAxAKSgQIQRgASgQIRhgAUPMIWP4rYLUtaANwAXgAgAGtAYgB-hOSAQQwLjE3mAEAoAEByAEKwAEB&sclient=gws-wiz'
    page_doll_by = 'https://www.google.com/search?q=доллар+к+белорусскому+рублю&sxsrf=APq-WBtqylXSbQq9I2hhnF7IKogaSYfiuQ%3A1648293150580&ei=HvU-YtaKI438rgTO2LzADg&oq=доллар+к+беллорус&gs_lcp=Cgdnd3Mtd2l6EAEYADIJCAAQChBGEIICMgQIABAKMgQIABAKMgQIABAKMgQIABAKMgQIABAKMgQIABAKMgQIABAKMgQIABAKMgQIABAKOgcIIxCwAxAnOgcIABBHELADOgoIABBHELADEMkDOgcIABCwAxBDOgQIIxAnOgoIABCABBCHAhAUOgUIABCABDoICAAQgAQQyQM6CQgjECcQRhCCAjoOCAAQgAQQsQMQgwEQyQM6CAgAEIAEELEDSgQIQRgASgQIRhgAUNoDWOwWYLEgaAFwAXgAgAGkAYgBohCSAQQwLjE0mAEAoAEByAEKwAEB&sclient=gws-wiz'
    page_doll_kz = 'https://www.google.com/search?q=доллар+к+тенге&sxsrf=APq-WBuUpez97AuzAKg6rLFUqNEmI4uYTA%3A1648293177314&ei=OfU-YsnXErGnrgTDlZ2ACg&ved=0ahUKEwiJ2MbK0uP2AhWxk4sKHcNKB6AQ4dUDCA0&uact=5&oq=доллар+к+тенге&gs_lcp=Cgdnd3Mtd2l6EAMyDQgAEIAEELEDEEYQggIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEEcQsAM6BwgAELADEEM6BAgjECc6CQgjECcQRhCCAjoKCAAQgAQQhwIQFDoNCAAQgAQQhwIQsQMQFDoOCAAQgAQQsQMQgwEQyQM6CAgAEIAEELEDSgQIQRgASgQIRhgAUK8GWKAWYNUXaAFwAXgAgAGhAYgBmg2SAQQwLjEymAEAoAEByAEKwAEB&sclient=gws-wiz'
    page_doll_mdl = 'https://www.google.com/search?q=доллар+к+лею&sxsrf=APq-WBsCdyNCXGX13smBDfZ_F7RHzGirzQ%3A1650809243056&ei=m1llYtTcArHMrgT2z77wBA&ved=0ahUKEwiUlpjU76z3AhUxposKHfanD04Q4dUDCA0&uact=5&oq=доллар+к+лею&gs_lcp=Cgdnd3Mtd2l6EAMyCAgAEIAEEMkDMgUIABCABDIFCAAQgAQyBQgAEMsBMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46CggAEEcQsAMQyQM6BwgAEEcQsAM6BwgAELADEEM6BAgjECc6DQgAEIAEEIcCELEDEBQ6CQgjECcQRhCCAjoICAAQgAQQsQM6CwgAEIAEELEDEMkDOgoIABCABBCHAhAUOgcIABCABBAKOg0IABCABBCHAhDJAxAUOgcIABDJAxANOgQIABANOggIABANEAUQHjoICAAQCBANEB5KBAhBGABKBAhGGABQ_QpYlDFgwztoA3ABeACAAXGIAecHkgEDNS41mAEAoAEByAEKwAEB&sclient=gws-wiz'
    page_doll_pln = 'https://www.google.com/search?q=доллар+к+польскому+злотому&sxsrf=APq-WBsvsvjGvbYuGF5SkUzxZkfXuo4PkQ%3A1650809252601&ei=pFllYumGJJPfrgSGzK6QCg&oq=доллар+к+gjkm&gs_lcp=Cgdnd3Mtd2l6EAEYADIECAAQDTIECAAQDTIECAAQDTIECAAQDTIICAAQDRAFEB4yCAgAEA0QBRAeMggIABANEAUQHjIICAAQCBANEB4yCAgAEAgQDRAeOgcIABBHELADOgcIABCwAxBDOgcIIxDJAxAnOgQIABBDOgUIABCABDoFCAAQywE6BwgAEIAEEAo6BAgjECc6CAgAEIAEELEDOg0IABCABBCHAhCxAxAUOgYIABAWEB46BggAEA0QCjoICAAQFhAKEB5KBAhBGABKBAhGGABQzARYtBhg1SNoAXABeACAAYgBiAHuBZIBAzIuNZgBAKABAcgBCsABAQ&sclient=gws-wiz'

    page_euro_ru = 'https://www.google.com/search?q=евро+к+рублю&sxsrf=APq-WBvNlAmGMARVsrbfOTBbStb2CSODNQ%3A1648293208628&ei=WPU-YtyAJoaUrwTGkbzgDA&oq=евро+к+ру&gs_lcp=Cgdnd3Mtd2l6EAEYADIJCCMQJxBGEIICMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgcIIxDqAhAnOgQIIxAnOg0IABCABBCHAhCxAxAUOgoIABCABBCHAhAUOggIABCABBCxAzoOCC4QgAQQsQMQxwEQowI6BAgAEEM6BwgAELEDEEM6CwgAEIAEELEDEIMBOgsIABCABBCxAxDJAzoICAAQgAQQyQM6BwgAEIAEEApKBAhBGABKBAhGGABQpg5Y9Rdg1SBoAXABeACAAaYBiAHECpIBAzAuOZgBAKABAbABCsABAQ&sclient=gws-wiz' 
    page_euro_ukr = 'https://www.google.com/search?q=евро+к+гривне&sxsrf=APq-WBth2GLgI7narVnKW9DluHMeO5B3Xw%3A1648293075646&ei=0_Q-YvLxJoP-rgTy9ofoCg&oq=евро+к+гривне&gs_lcp=Cgdnd3Mtd2l6EAEYADINCAAQgAQQsQMQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQyQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCCMQsAMQJzoHCAAQRxCwAzoKCAAQRxCwAxDJAzoHCAAQsAMQQzoJCCMQJxBGEIICOg0IABCABBCHAhCxAxAUOggIABCABBCxAzoSCAAQgAQQhwIQsQMQFBBGEIICOgoIABCABBCHAhAUSgQIQRgASgQIRhgAUJYEWOgZYJIlaAFwAXgAgAGlAYgBvgySAQQwLjExmAEAoAEByAEKwAEB&sclient=gws-wiz'
    page_euro_by = 'https://www.google.com/search?q=евро+к+белорусскому+рублю&sxsrf=APq-WBvuDL_aWlRRvZjaQu7rkdC93SfyAA%3A1648293283112&ei=o_U-YpO-Br6GwPAP3Lix2Aw&oq=евро+к+бел&gs_lcp=Cgdnd3Mtd2l6EAEYADIKCAAQgAQQhwIQFDIFCAAQgAQyBQgAEIAEMgoIABCABBCHAhAUMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCAAQRxCwAzoKCAAQRxCwAxDJAzoICAAQkgMQsAM6BwgAELADEEM6BAgjECc6CAgAEIAEEMkDOgkIIxAnEEYQggI6CAgAEIAEELEDSgQIQRgASgQIRhgAUOkDWLYaYLIiaAFwAXgAgAGWAYgB5wmSAQMwLjmYAQCgAQHIAQrAAQE&sclient=gws-wiz' 
    page_euro_kz = 'https://www.google.com/search?q=евро+к+тенге&sxsrf=APq-WBs9DSpesdhk6r3wVqwqp2s7A4EogA%3A1648293323892&ei=y_U-YouUNuyHwPAPz9KS6Ac&ved=0ahUKEwjLpbmQ0-P2AhXsAxAIHU-pBH0Q4dUDCA0&uact=5&oq=евро+к+тенге&gs_lcp=Cgdnd3Mtd2l6EAMyCggAEIAEEEYQggIyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEEcQsAM6BwgAELADEEM6BAgjECc6BAgAEEM6BggAEBYQHjoJCCMQJxBGEIICOgoIABCABBCHAhAUOggIABCABBCxAzoICAAQgAQQyQNKBAhBGABKBAhGGABQqANYnxZgtRdoAXABeACAAZ4BiAHBD5IBBDAuMTSYAQCgAQHIAQrAAQE&sclient=gws-wiz' 
    page_euro_mdl = 'https://www.google.com/search?q=евро+к+лею&sxsrf=APq-WBuqcz8Ikprj8eagB8rjrrxnZbSUJQ%3A1650809281375&ei=wVllYv-2FqWsrgSL-IVw&ved=0ahUKEwi_m7vm76z3AhUllosKHQt8AQ4Q4dUDCA0&uact=5&oq=евро+к+лею&gs_lcp=Cgdnd3Mtd2l6EAMyDQgAEIAEEMkDEEYQggIyBQgAEIAEMgUIABCABDIFCAAQgAQyBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB46BwgAEEcQsAM6CggAEEcQsAMQyQM6BwgAELADEEM6BggAEAcQHjoICAAQBxAFEB46BAgAEA06CQgAEEMQRhCCAjoGCAAQBRAeOgoIABCABBCHAhAUOgcIIxCxAhAnOgQIABAKOgQIIxAnOgQIABBDOggIABCABBCxAzoQCAAQgAQQhwIQsQMQyQMQFDoICAAQgAQQyQM6BwgAEIAEEApKBAhBGABKBAhGGABQ1gtY9C1gwy9oAnABeACAAZ4BiAHYFJIBBDUuMjCYAQCgAQHIAQrAAQE&sclient=gws-wiz'
    page_euro_pln = 'https://www.google.com/search?q=евро+к+польскому+злотому&sxsrf=APq-WBt5IasMauFzzMlip8Babf17cfzzUA%3A1650809308520&ei=3FllYp-yH8WqrgS317boDQ&oq=евро+к+gjkm&gs_lcp=Cgdnd3Mtd2l6EAEYADIECAAQDTIECAAQDTIECAAQDTIICAAQDRAFEB4yCAgAEA0QBRAeMggIABANEAUQHjIICAAQDRAFEB4yCAgAEA0QBRAeMggIABANEAUQHjIICAAQCBANEB46BwgAEEcQsAM6CggAEEcQsAMQyQM6BwgAELADEEM6BwgjEMkDECc6BQgAEIAEOgoIABCABBCHAhAUOgcIABCABBAKOgQIABBDOgwIIxDJAxAnEEYQggI6BAgjECc6CAgAEIAEELEDOg0IABCABBCHAhCxAxAUOggIABAWEAoQHjoGCAAQFhAeSgQIQRgASgQIRhgAUNsDWLgLYJ8XaAFwAXgAgAFtiAG4BZIBAzUuMpgBAKABAcgBCsABAQ&sclient=gws-wiz'

    arr = [page_doll_ru, page_doll_ukr, page_doll_by, page_doll_kz, page_doll_mdl, page_doll_pln, \
         page_euro_ru, page_euro_ukr, page_euro_by, page_euro_kz, page_euro_mdl, page_euro_pln]

    #my user agent. perhaps, you have another one. you can find it in google page
    #when you enter in the search line 'my user agent'
    headers = '"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.42'
    
    to_doll = ''
    to_euro = ''

    beautiful = True
    eur = False

    count = 0
    for i in arr:

        if count == len(arr) / 2:
            eur = True
        full_page = ''
        try:
            full_page = requests.get(i, headers)
        except Exception:
            print('problem')

        if full_page:
            soup = BeautifulSoup(full_page.content, 'html.parser')
            convert = soup.findAll("div", {"class": "BNeawe", "class": "iBp4i", "class": "AP7Wnd"})

            if convert == []:
                print('problems with converting')
                beautiful = False
                break
            else:
                j = 0
                while convert[0].text[j] != ' ':
                    j = j + 1

                if eur == False:
                    to_doll = to_doll + convert[0].text[:j] + '\n'
                else:
                    to_euro = to_euro + convert[0].text[:j] + '\n'
                #print('ok')
        else:
            print('full_page not found. time: ' + time.ctime(time.time()))

        time.sleep(1)
        count = count + 1
                
    if beautiful == False or to_doll == '' or to_euro == '':
        print('no ok, end:' + time.ctime(time.time()))
    else:
        write_in_file(doll_txt, to_doll + str(int(time.time())))
        write_in_file(euro_txt, to_euro)

    #########################################################################################
    t = time.time()
    #t = t + 3600
    t = int(t)

    s_t = time.ctime(t)
    #print(s_t)
    s_t = s_t.split(' ')

    stat = read_file(st_doll)
    stat = stat.split('\n')
    #print(s_t[4][:5])
    if ((s_t[4][:5] == '10:40' or read_file(st_doll) == '' or read_file(st_euro) == '') and t - int(stat[0]) > 120) or (t - int(stat[0]) > 90000):
        #записываем данные прошлые данные на вчера
        write_in_file(yest_doll, read_file(st_doll))
        write_in_file(yest_euro, read_file(st_euro))
        #записываем сегодняшие данные на сегодня
        write_in_file(st_doll, str(t) + '\n'+ to_doll)
        write_in_file(st_euro, str(t) + '\n'+ to_euro)
        print('new data in statistics: ' + time.ctime(t))
    time.sleep(10)

    
