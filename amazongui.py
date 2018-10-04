#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyh import *
from amazondata import AmazonData
from amazonwrapper import *

class AmazonGUI():
    def __init__(self):
        pass

    def create_page(self, node, node_name, type, css_file, data, output):
        page_name =  node_name.split('/')[len(node_name.split('/')) - 1]
        mainpage = PyH(page_name)
        mainpage.addCSS(css_file)
        maindiv = div()
        mainpage <<  maindiv
        if type == 'BS':
            maintitlelink = 'https://www.amazon.co.jp/gp/bestsellers/electronics/' + node
        elif type == 'NR':
            maintitlelink = 'https://www.amazon.co.jp/gp/new-releases/electronics/' + node
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
            tmp_data = [rank, asin, img_src, ('￥ ' + str(price)), review, rate, qa, shipping, seller, avg_sale, limited]
            for i in range(0, 11):
                if i != 1 and i != 2:
                    tmp_td = td(str(tmp_data[i]))
                elif i == 1:
                    asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    asin_a  = a(asin,  href=asin_link, target ="_blank")
                    tmp_td = td()
                    tmp_td << asin_a
                elif i == 2:
                    asin_link = 'https://www.amazon.co.jp/dp/' + tmp_data[1]
                    img_a = a(href=asin_link, target ="_blank")
                    img_src = 'https://images-na.ssl-images-amazon.com/images/I/'+ tmp_data[2] + '._SL500_SR160,160_.jpg'
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
    data = get_all_data('amazondata', '5662827051_BS', False)
    if data != False:
        node_name = get_node_name('node_info', 'health', '5662827051')
        if node_name != False:
            amazongui.create_page('5662827051', node_name[0][1], 'BS', 'amazongui.css', data, '../')
            amazondata = AmazonData()

