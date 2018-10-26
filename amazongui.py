#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyh import *
from amazonwrapper import *
import sys
import amazonglobal
import pandas as pd

class AmazonGUI():
    def __init__(self):
        pass

    def get_unexpected_err(self, data):
        sale_data_array = []
        for index in range(len(data)):
            # print(data[index][0], flush=True)
            sale_data_array.append(int(data[index][0]))
        four = pd.Series(sale_data_array).describe()
        Q1 = four['25%']
        Q3 = four['75%']
        IQR = Q3 - Q1

        upper = Q3 + 1.5 * IQR
        lower = Q1 - 1.5 * IQR

        return [upper, lower]

    def check_unexpected_err(self, data, err_range):
        count = 0

        for index in range(len(data)):
            # if int(data[index][0]) > ((err_range[1] + err_range[0])/2):
            if int(data[index][0] > err_range[0]):
                count += 1
        # print(count, flush=True)
        return count

    def create_sale_inventory_page(self, country, asin):
        # get sale data
        # get inventory data
        # generate last 15 days date
        # generate sale data of last 15 days
        # generate inventory data of last 15 days
        # generate line image
        days_data_array = get_days_array_of_day(15, -1)
        sale_data_array = []
        inventory_data_array = []
        amazondata = AmazonData()
        if country == 'us':
            db_name_data = amazonglobal.db_name_data_us
        elif country == 'jp':
            db_name_data = amazonglobal.db_name_data_jp
        status = amazondata.connect_database(db_name_data)
        if status == False:
            print("connect in failure..", flush=True)
        else:
            table_sale = 'SALE_' + asin
            table_inventory = 'INVENTORY_' + asin
            sale_array = get_all_data(db_name_data, table_inventory, False, False)
            if sale_array == False:
                print("get all data in failure", flush=True)
            else:
                for index in range(15):
                    flag = False
                    for i in range(len(sale_array)):
                        if sale_array[i][0].strftime('%Y-%m-%d') == days_data_array[index]:
                            print(days_data_array[index], flush=True)
                            print(sale_array[i][0], flush=True)
                            sale_data_array.append(int(sale_array[i][1]))
                            flag = True
                            break
                    if flag == False:
                        sale_data_array.append(0)
                print(days_data_array, flush=True)
                print(sale_data_array, flush=True)

            amazondata.disconnect_database()

    def collect_page_together(self, country, node, node_name, type, data, check_err):
        maindiv = div()
        if country == 'jp':
            if type == 'BS':
                maintitlelink = 'https://www.amazon.co.jp/gp/bestsellers/electronics/' + node
            elif type == 'NR':
                maintitlelink = 'https://www.amazon.co.jp/gp/new-releases/electronics/' + node
        elif country == 'us':
            if type == 'BS' or type == 'SL':
                maintitlelink = 'https://www.amazon.com/gp/bestsellers/electronics/' + node
            elif type == 'NR':
                maintitlelink = 'https://www.amazon.com/gp/new-releases/electronics/' + node
        maintitle_a = a(node_name, href=maintitlelink, target ="_blank")
        maintitle = h4()
        maintitle << maintitle_a
        maindiv << maintitle
        info_table = table(cellspacing='1')
        maindiv << info_table
        head_row =  tr()
        thead_row = thead()
        thead_row << head_row
        info_table << thead_row
        head_row << th('排名') + th('ASIN') + th('主图') +th('单价') + th('评论')
        if check_err == '0':
            head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('限购')
        elif check_err == '1':
            head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('校验')
        tbody_row = tbody()
        info_table << tbody_row
        for index in range(len(data)):
            tmp_tr = tr()
            rank = data[index][0]
            asin = data[index][1]
            img_src = data[index][12]
            price = data[index][3]
            review  = data[index][4]
            rate = data[index][5]
            qa  = data[index][6]
            shipping = data[index][7]
            seller = data[index][8]
            avg_sale = data[index][9]

            if country == 'jp':
                db_name_sale = amazonglobal.db_name_data_jp
            elif country == 'us':
                db_name_sale = amazonglobal.db_name_data_us
            if check_err == '0':
                limited = data[index][11]
            elif check_err == '1':
                sale_data_array = get_all_data(db_name_sale, 'SALE_' + asin, 'sale', False)
                err_value = self.get_unexpected_err(sale_data_array)
                err_count = self.check_unexpected_err(sale_data_array, err_value)
                check_status = str(((err_value[1] + err_value[0])/2)) + '_' + str(err_count)
                limited = check_status
            if country == 'jp':
                tmp_data = [rank, asin, img_src, ('￥ ' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            elif country == 'us':
                tmp_data = [rank, asin, img_src, ('$' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            for i in range(0, 11):
                if i == 1:
                    if country == 'jp':
                        asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    elif country == 'us':
                        asin_link = 'https://www.amazon.com/dp/' + tmp_data[1]
                    asin_a  = a(asin,  href=asin_link, target ="_blank")
                    tmp_td = td()
                    tmp_td << asin_a
                elif i == 2:
                    if country == 'jp':
                        asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    elif country == 'us':
                        asin_link = 'https://www.amazon.com/dp/' + tmp_data[1]
                    img_a = a(href=asin_link, target ="_blank")
                    if country == 'jp':
                        img_src = 'https://images-na.ssl-images-amazon.com/images/I/'+ tmp_data[2] + '._SL500_SR160,160_.jpg'
                    elif country == 'us':
                        img_src = 'https://images-na.ssl-images-amazon.com/images/I/' + tmp_data[2] + '._AC_UL200_SR200,200_.jpg'
                    img_img = img(border="0", src=img_src)
                    img_a << img_img
                    tmp_td = td()
                    tmp_td << img_a
                else:
                    tmp_td = td(str(tmp_data[i]))

                tmp_tr << tmp_td

            tbody_row << tmp_tr

        return maindiv

    def create_page_together(self, table_array, country, avg_sale, price, type, css_file, output, check_err):
        page_name = "Potential Product"
        mainpage = PyH(page_name)
        mainpage.addCSS(css_file)
        for node in table_array:
            if is_in_task_delete_data(country, node[0]) == False:
                table_name = node[0] + '_BS'
                condition = 'avg_sale>=' + avg_sale + ' and price>=' + price
                data = get_all_data(db_name_data, table_name, False, condition)
                if data != False:
                    if isDigit(node[0]):
                        node_name = get_node_name_from_all(db_name_node, node[0], country)
                        if node_name == False:
                            print("get node name in failure.", flush=True)
                    else:
                        node_name = node[0]

                    maindiv = self.collect_page_together(country, node[0], node_name, type, data, check_err)
                    mainpage << maindiv
            else:
                continue
        filename = output + page_name + '.html'
        mainpage.printOut(filename)

    def create_page(self, country, node, node_name, type, css_file, data, output, check_err):
        page_name =  node_name.split('/')[len(node_name.split('/')) - 1]
        mainpage = PyH(page_name)
        mainpage.addCSS(css_file)
        maindiv = div()
        mainpage <<  maindiv
        if country == 'jp': #
            if type == 'BS':
                maintitlelink = 'https://www.amazon.co.jp/gp/bestsellers/electronics/' + node
            elif type == 'NR':
                maintitlelink = 'https://www.amazon.co.jp/gp/new-releases/electronics/' + node
        elif country == 'us':
            if type == 'BS' or type == 'SL':
                maintitlelink = 'https://www.amazon.com/gp/bestsellers/electronics/' + node
            elif type == 'NR':
                maintitlelink = 'https://www.amazon.com/gp/new-releases/electronics/' + node
        maintitle_a = a(node_name, href=maintitlelink, target ="_blank")
        maintitle = h4()
        maintitle << maintitle_a
        maindiv << maintitle
        info_table = table(cellspacing='1')
        maindiv << info_table
        head_row =  tr()
        thead_row = thead()
        thead_row << head_row
        info_table << thead_row
        head_row << th('排名') + th('ASIN') + th('主图') +th('单价') + th('评论')
        if check_err == '0':
            head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('限购')
        elif check_err == '1':
            head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('校验')
        tbody_row = tbody()
        info_table << tbody_row
        for index in range(len(data)):
            tmp_tr = tr()
            rank = data[index][0]
            asin = data[index][1]
            img_src = data[index][12]
            price = data[index][3]
            review  = data[index][4]
            rate = data[index][5]
            qa  = data[index][6]
            shipping = data[index][7]
            seller = data[index][8]
            avg_sale = data[index][9]

            if country == 'jp':
                db_name_sale = amazonglobal.db_name_data_jp
            elif country == 'us':
                db_name_sale = amazonglobal.db_name_data_us
            if check_err == '0':
                limited = data[index][11]
            elif check_err == '1':
                sale_data_array = get_all_data(db_name_sale, 'SALE_' + asin, 'sale', False)
                err_value = self.get_unexpected_err(sale_data_array)
                err_count = self.check_unexpected_err(sale_data_array, err_value)
                check_status = str(((err_value[1] + err_value[0])/2)) + '_' + str(err_count)
                limited = check_status
            if country == 'jp':
                tmp_data = [rank, asin, img_src, ('￥ ' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            elif country == 'us':
                tmp_data = [rank, asin, img_src, ('$' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            for i in range(0, 11):
                if i != 1 and i != 2:
                    tmp_td = td(str(tmp_data[i]))
                elif i == 1:
                    if country == 'jp':
                        asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    elif country == 'us':
                        asin_link = 'https://www.amazon.com/dp/' + tmp_data[1]
                    asin_a  = a(asin,  href=asin_link, target ="_blank")
                    tmp_td = td()
                    tmp_td << asin_a
                elif i == 2:
                    if country == 'jp':
                        asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    elif country == 'us':
                        asin_link = 'https://www.amazon.com/dp/' + tmp_data[1]
                    img_a = a(href=asin_link, target ="_blank")
                    if country == 'jp':
                        img_src = 'https://images-na.ssl-images-amazon.com/images/I/'+ tmp_data[2] + '._SL500_SR160,160_.jpg'
                    elif country == 'us':
                        img_src = 'https://images-na.ssl-images-amazon.com/images/I/' + tmp_data[2] + '._AC_UL200_SR200,200_.jpg'
                    img_img = img(border="0", src=img_src)
                    img_a << img_img
                    tmp_td = td()
                    tmp_td  << img_a

                tmp_tr << tmp_td

            tbody_row << tmp_tr
        filename = output + page_name + '-'  +node + '.html'
        mainpage.printOut(filename)


if __name__ == "__main__":
    amazongui = AmazonGUI()
    amazongui.create_sale_inventory_page('us', 'B07JMSWCGD')
    exit()
    task_type = sys.argv[1]
    country = sys.argv[2]
    avg_sale = sys.argv[3]
    price = sys.argv[4]
    check_err = sys.argv[5]
    if country == 'us':
        table_array = get_all_data(amazonglobal.db_name_task, amazonglobal.table_sale_task_us, 'node', False)
        db_name_data = amazonglobal.db_name_data_us
        db_name_node = amazonglobal.db_name_node_info_us
    elif country == 'jp':
        table_array = get_all_data(amazonglobal.db_name_task, amazonglobal.table_sale_task_jp, 'node', False)
        db_name_data = amazonglobal.db_name_data_jp
        db_name_node = amazonglobal.db_name_node_info_jp
    if task_type == 'single':
        for node in table_array:
            print(node[0], flush=True)
            table_name = node[0] + '_BS'
            condition = 'avg_sale>' + avg_sale + ' and price>=' + price
            data = get_all_data(db_name_data, table_name, False, condition)
            if data != False:
                if isDigit(node[0]):
                    node_name = get_node_name_from_all(db_name_node, node[0], country)
                    if node_name != False:
                        print(node_name.replace(' & ', '_'), flush=True)
                        if country == 'us':
                            amazongui.create_page(country, node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page/', check_err)
                        elif country == 'jp':
                            amazongui.create_page(country, node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page_jp/', check_err)

                else:
                    if country == 'us':
                        amazongui.create_page(country, node[0], node[0], 'BS', 'amazongui.css', data, '../html_page/', check_err)
                    elif country == 'jp':
                        amazongui.create_page(country, node[0], node[0], 'BS', 'amazongui.css', data, '../html_page_jp/', check_err)
    elif task_type == 'total':
        if country == 'us':
            amazongui.create_page_together(table_array, country, avg_sale, price, 'BS', 'amazongui.css', '../html_page/', check_err)
        elif country == 'jp':
            amazongui.create_page_together(table_array, country, avg_sale, price, 'BS', 'amazongui.css', '../html_page_jp/', check_err)

