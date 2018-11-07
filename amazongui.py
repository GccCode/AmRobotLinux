#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyh import *
from amazonwrapper import *
import sys
import amazonglobal
import pandas as pd
from pyecharts import Overlap, Bar, Line, Grid
from sqlmgr import SqlMgr

""" 
线性表结构
"""


class LinearMap(object):

    def __init__(self):
        self.items = []

    # 往表中添加元素
    def add(self, k, v):
        self.items.append((k, v))

    # 线性方式查找元素
    def get(self, k):
        for key, value in self.items:
            if key == k:  # 键存在，返回值，否则抛出异常
                return value
        return False


'''
我们可以在使用add添加元素时让items列表保持有序，而在使用get时采取二分查找方式，时间复杂度为O(log n)。 
然而往列表中插入一个新元素实际上是一个线性操作，所以这种方法并非最好的方法。
同时，我们仍然没有达到常数查找时间的要求。
'''

'''
将总查询表分割为若干段较小的列表，比如100个子段。
通过hash函数求出某个键的哈希值，再通过计算，得到往哪个子段中添加或查找。
相对于从头开始搜索列表，时间会极大的缩短。
'''


class BetterMap(object):
    # 利用LinearMap对象作为子表，建立更快的查询表
    def __init__(self, n=100):
        self.maps = []  # 总表格
        for i in range(n):  # 根据n的大小建立n个空的子表
            self.maps.append(LinearMap())

    def find_map(self, k):  # 通过hash函数计算索引值
        index = hash(k) % len(self.maps)
        return self.maps[index]  # 返回索引子表的引用

    # 寻找合适的子表（linearMap对象）,进行添加和查找
    def add(self, k, v):
        m = self.find_map(k)
        m.add(k, v)

    def get(self, k):
        m = self.find_map(k)
        return m.get(k)


class HashMap(object):
    def __init__(self):
        # 初始化总表为，容量为2的表格（含两个子表）
        self.maps = BetterMap(2)
        self.num = 0  # 表中数据个数
        self.repeat_find = 0

    def get(self, k):
        return self.maps.get(k)

    def add_repeat_find(self):
        self.repeat_find += 1

    def add(self, k, v):
        # 若当前元素数量达到临界值（子表总数）时，进行重排操作
        # 对总表进行扩张，增加子表的个数为当前元素个数的两倍！
        if self.num == len(self.maps.maps):
            self.resize()

        # 往重排过后的 self.map 添加新的元素
        self.maps.add(k, v)
        self.num += 1

    def resize(self):
        # 重排操作，添加新表, 注意重排需要线性的时间
        # 先建立一个新的表,子表数 = 2 * 元素个数
        new_maps = BetterMap(self.num * 2)

        for m in self.maps.maps:  # 检索每个旧的子表
            for k, v in m.items:  # 将子表的元素复制到新子表
                new_maps.add(k, v)

        self.maps = new_maps  # 令当前的表为新表


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

    def create_sale_inventory_page(self, sqlmgr, asin):
        days_data_array = get_days_array_of_day(29, -1)
        sale_data_array = []
        inventory_data_array = []

        table_sale = 'SALE_' + asin
        table_inventory = 'INVENTORY_' + asin
        sale_array = get_all_data(sqlmgr.ad_sale_data, table_sale, False, False)
        if sale_array == False:
            print("get all data in failure", flush=True)
        else:
            for index in range(30):
                flag = False
                for i in range(len(sale_array)):
                    if sale_array[i][0].strftime('%Y-%m-%d') == days_data_array[index]:
                        sale_data_array.append(int(sale_array[i][1]))
                        flag = True
                        break
                if flag == False:
                    sale_data_array.append(0)
        inventory_array = get_all_data(sqlmgr.ad_sale_data, table_inventory, False, False)
        if inventory_array == False:
            print("get all data in failure", flush=True)
        else:
            for index in range(30):
                flag = False
                for i in range(len(inventory_array)):
                    if inventory_array[i][0].strftime('%Y-%m-%d') == days_data_array[index]:
                        inventory_data_array.append(int(inventory_array[i][1]))
                        flag = True
                        break
                if flag == False:
                    inventory_data_array.append(0)

        grid = Grid()

        bar = Bar(title="过去15天历史销量与库存", title_pos="30%")
        bar.add(
            "库存",
            days_data_array,
            inventory_data_array,
            yaxis_max=1200,
            legend_pos="85%",
            legend_orient="vertical",
            legend_top="45%",
        )
        line = Line()
        line.add("销量", days_data_array, sale_data_array, mark_point=["max"], mark_line=["average"], yaxis_max=500)
        overlap = Overlap(width=1200, height=600)
        overlap.add(bar)
        overlap.add(line, is_add_yaxis=True, yaxis_index=1)

        grid.add(overlap, grid_right="20%")
        filename = '../html_page/daily_sale/' + asin + '.html'
        grid.render(filename)


    def collect_page_together(self, sqlmgr, asin_maps, node, node_name, type, data, check_err):
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
            head_row << th('评分') + th('QA') + th('物流') + th('卖家数') + th('平均日销量') + th('尺寸')
        tbody_row = tbody()
        info_table << tbody_row
        for index in range(len(data)):
            tmp_tr = tr()
            rank = data[index][0]
            asin = data[index][1]
            if asin_maps.get(asin) is not False:
                asin_maps.add_repeat_find()
                continue
            else:
                asin_maps.add(asin, asin_maps.num)
            img_src = data[index][12]
            price = data[index][3]
            review  = data[index][4]
            rate = data[index][5]
            qa  = data[index][6]
            shipping = data[index][7]
            seller = data[index][8]
            avg_sale = data[index][9]

            self.create_sale_inventory_page(sqlmgr, asin)

            if check_err == '0':
                limited = data[index][11]
            elif check_err == '1':
                # sale_data_array = get_all_data(db_name_sale, 'SALE_' + asin, 'sale', False)
                # err_value = self.get_unexpected_err(sale_data_array)
                # err_count = self.check_unexpected_err(sale_data_array, err_value)
                # check_status = str(((err_value[1] + err_value[0])/2)) + '_' + str(err_count)
                # limited = check_status
                limited = data[index][15]
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
                elif i == 9:
                    avg_sale_link = './daily_sale/' + asin + '.html'
                    avg_sale_a = a(avg_sale,  href=avg_sale_link, target="_blank")
                    tmp_td = td()
                    tmp_td << avg_sale_a
                else:
                    tmp_td = td(str(tmp_data[i]))

                tmp_tr << tmp_td

            tbody_row << tmp_tr

        return maindiv

    def create_page_together(self, sqlmgr, table_array, avg_sale, price, type, css_file, output, check_err):
        page_name = "Potential Product"
        mainpage = PyH(page_name)
        mainpage.addCSS(css_file)
        asin_maps = HashMap()
        count = 0
        for node in table_array:
            if is_in_task_delete_data(sqlmgr.ad_sale_task, node[0]) == False:
                table_name = node[0] + '_BS'
                condition = 'limited=\'no\' and avg_sale>=' + avg_sale + ' and price>=' + price
                data = get_all_data(sqlmgr.ad_sale_data, table_name, False, condition)
                if data != False:
                    if isDigit(node[0]):
                        node_name = get_node_name_from_all(sqlmgr.ad_node_info, node[0])
                        if node_name == False:
                            print("get node name in failure.", flush=True)
                    else:
                        node_name = node[0]

                    maindiv = self.collect_page_together(sqlmgr, asin_maps, node[0], node_name, type, data, check_err)
                    mainpage << maindiv
                    count += len(data)
            else:
                continue
        filename = output + page_name + '.html'
        mainpage.printOut(filename)
        print("Total - Repeat: " + str(count) + ' - ' + str(asin_maps.repeat_find), flush=True)

    def create_page(self, sqlmgr, node, node_name, type, css_file, data, output, check_err):
        page_name = node_name.split('/')[len(node_name.split('/')) - 1]
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
        head_row = tr()
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

            if check_err == '0':
                limited = data[index][11]
            elif check_err == '1':
                sale_data_array = get_all_data(sqlmgr.ad_sale_data, 'SALE_' + asin, 'sale', False)
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
    # amazongui.create_sale_inventory_page('us', 'B07JMSWCGD')
    # exit()
    task_type = sys.argv[1]
    country = sys.argv[2]
    avg_sale = sys.argv[3]
    price = sys.argv[4]
    check_err = sys.argv[5]

    sqlmgr = SqlMgr(country)
    if sqlmgr.start() == False:
        print("SqlMgr initialized in failure", flush=True)
        exit()

    if country == 'us':
        table_array = get_all_data(sqlmgr.ad_sale_task, amazonglobal.table_sale_task_us, 'node', False)
    elif country == 'jp':
        table_array = get_all_data(sqlmgr.ad_sale_task, amazonglobal.table_sale_task_jp, 'node', False)

    if task_type == 'single':
        for node in table_array:
            print(node[0], flush=True)
            table_name = node[0] + '_BS'
            condition = 'limited=\'no\' and avg_sale>' + avg_sale + ' and price>=' + price
            data = get_all_data(sqlmgr.ad_sale_data, table_name, False, condition)
            if data != False:
                if isDigit(node[0]):
                    node_name = get_node_name_from_all(sqlmgr.ad_node_info, node[0], country)
                    if node_name != False:
                        print(node_name.replace(' & ', '_'), flush=True)
                        if country == 'us':
                            amazongui.create_page(sqlmgr, node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page/', check_err)
                        elif country == 'jp':
                            amazongui.create_page(sqlmgr, node[0], node_name.replace(' & ', '_'), 'BS', 'amazongui.css', data, '../html_page_jp/', check_err)

                else:
                    if country == 'us':
                        amazongui.create_page(sqlmgr, node[0], node[0], 'BS', 'amazongui.css', data, '../html_page/', check_err)
                    elif country == 'jp':
                        amazongui.create_page(sqlmgr, node[0], node[0], 'BS', 'amazongui.css', data, '../html_page_jp/', check_err)
    elif task_type == 'total':
        if country == 'us':
            amazongui.create_page_together(sqlmgr, table_array, avg_sale, price, 'BS', 'amazongui.css', '../html_page/', check_err)
        elif country == 'jp':
            amazongui.create_page_together(sqlmgr, table_array, avg_sale, price, 'BS', 'amazongui.css', '../html_page_jp/', check_err)


    sqlmgr.stop()
