#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyh import *
from amazonwrapper import *
import sys
import amazonglobal

class AmazonGUI():
    def __init__(self):
        pass

    def create_page(self, country, node, node_name, type, css_file, data, output):
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
        head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('限购')
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
            limited = data[index][11]
            if country == 'jp':
                tmp_data = [rank, asin, img_src, ('￥ ' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            elif country == 'us':
                tmp_data = [rank, asin, img_src, ('$' + str(price)), review, rate, qa, shipping, seller, avg_sale,
                            limited]
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
    country = sys.argv[1]
    condition = 'length(node)>4'
    if country == 'us':
        table_array = get_all_data(amazonglobal.db_name_task, amazonglobal.table_sale_task_us, 'node', False)
    elif country == 'jp':
        table_array = get_all_data(amazonglobal.db_name_task, amazonglobal.table_sale_task_jp, 'node', False)
    for node in table_array:
        print(node[0], flush=True)
        table_name = node[0] + '_BS'
        condition = 'avg_sale>0'
        data = get_all_data('data_us', table_name, False, condition)
        if data != False:
            if isDigit(node[0]):
                node_name = get_node_name_from_all('node_info_us', node[0], 'us')
                if node_name != False:
                    print(node_name.replace(' & ', '_'), flush=True)
                    if country == 'us':
                        amazongui.create_page('us', node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page/')
                    elif country == 'jp':
                        amazongui.create_page('jp', node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page_jp/')

            else:
                if country == 'us':
                    amazongui.create_page('us', node[0], node[0], 'BS', 'amazongui.css', data, '../html_page/')
                elif country == 'jp':
                    amazongui.create_page('us', node[0], node[0], 'BS', 'amazongui.css', data, '../html_page_jp/')

