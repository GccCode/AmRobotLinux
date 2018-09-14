#!/usr/bin/env python
# -*- coding:utf-8 -*-

from selenium.webdriver.common.by import By


class AmazonPageLocator(object):
    LOGO = (By.ID, 'nav-logo')
    ACCOUNT = (By.ID, 'nav-link-accountList')
    SIGNIN = (By.XPATH, '//*[@id=\'nav-flyout-ya-signin\']/a[position()=1]')
    SIGNOUT = (By.ID, 'nav-item-signout-sa')
    STARTHERE = (By.XPATH, '//*[@id=\'nav-flyout-ya-newCust\']/a')
    CREATEACCOUNTSUBMIT = (By.ID, 'createAccountSubmit')
    SEARCH = (By.ID, 'twotabsearchtextbox')
    SUBMITKEYWORD = (By.XPATH, '//*[@id=\'nav-search\']/form/div[position()=2]/div/input')
    PRIME = (By.ID, "nav-link-prime")
    PRIMEFREETRIAL = (By.ID, 'prime-header-CTA')
    PRIMESTARTTRIAL = (By.ID, 'a-autoid-0')
    CART = (By.ID, "nav-cart")
    ORDERS = (By.ID, "nav-orders")
    WISHLIST = (By.XPATH, '//*[@id=\'nav-flyout-wl-items\']/div/a[position()=1]/span')


class AmazonAccountPageLocator(AmazonPageLocator):
    YOURADDRESS_US = (By.XPATH, '//*[@id=\'a-page\']/div[position()=3]/div/div[position()=2]/div[position()=1]/a/div/div/div')
    YOURADDRESS_JP = (By.XPATH, '//*[@id=\'a-page\']/div[position()=2]/div/div[position()=3]/div[position()=1]/a/div/div/div')
    PAYMENTOPTIONS_US = (By.XPATH, '//*[@id=\'a-page\']/div[position()=3]/div/div[position()=2]/div[position()=2]/a/div/div/div')
    PAYMENTOPTIONS_JP = (By.XPATH, '//*[@id=\'a-page\']/div[position()=2]/div/div[position()=3]/div[position()=2]/a/div/div/div')
    ADDADDRESS = (By.ID, 'ya-myab-plus-address-icon')
    WALLETTITLE = (By.ID, 'walletTitleRow')


class AmazonAsinPageLocator(AmazonPageLocator):
    ADDCARTBUTTON = (By.ID, 'add-to-cart-button')
    ADDWISHLISTSUBMITBUTTON = (By.ID, 'add-to-wishlist-button-submit')
    CREATELISTBUTTON = (By.XPATH, '//*[@id=\'WLNEW_cancel\']/../../span[3]/span/span')
    WISHLISTSELETE = (By.XPATH, '//*[@id=\'WLNEW_list_type_WL\']/../span')
    WISHLISTCONTINUE = (By.ID, 'WLHUC_continue')
    WISHLISTCONTINUE1 = (By.XPATH, '//*[@id=\'wl-huc-post-create-msg\']/div/div[position()=2]/span[position()=2]/span/span/button')
    QATEXT = (By.XPATH, '//*[@id=\'ask-dp-search_feature_div\']/div/div/div/div/form/span[position()=1]/span/span/span/span/span/div/input')
    QAENTRYBUTTON_US = (By.CSS_SELECTOR, '[value=\'Ask the Community\']')
    QAENTRYBUTTON_JP = (By.CSS_SELECTOR, '[value=\'コミュニティに尋ねる\']')
    QAPOSTBUTTON = (By.CSS_SELECTOR, '[data-action=\'ask-dpsearch-desktop-post-question\']')
    REVIEWALL = (By.ID, 'dp-summary-see-all-reviews')
    REVIEWPAGE_SYMBOL = (By.ID, 'cm_cr-buy_box')


class AmazonCartPageLocator(AmazonPageLocator):
    LOGO = 0


class AmazonPaymentPageLocator(AmazonPageLocator):
    CARDHOLDER_US = (By.XPATH, '//input[contains(@id, \'-24\')]')
    CARDHOLDER_JP = (By.XPATH, '//input[contains(@id, \'-22\')]')
    CARDNUMBER_US = (By.XPATH, '//input[contains(@id, \'-25\')]')
    CARDNUMBER_JP = (By.XPATH, '//input[contains(@id, \'-23\')]')
    VALIDMON_US = (By.XPATH, '//select[contains(@id, \'-27\')]')
    VALIDMON_JP = (By.XPATH, '//select[contains(@id, \'-25\')]')
    VALIDYEAR_US = (By.XPATH, '//select[contains(@id, \'-29\')]')
    VALIDYEAR_JP = (By.XPATH, '//select[contains(@id, \'-27\')]')
    ADDCARD_US = (By.XPATH, '//span[contains(@id, \'-32\')]/span/input[position()=1] ')
    ADDCARD_JP = (By.XPATH, '//span[contains(@id, \'-30\')]/span/input[position()=1] ')
    USETHISADDRESS_US = (By.XPATH, '//div[contains(@id, \'-21\')]/div/div[position()=2]/form/div/div/div/div/div/span[position()=2]/span/input[position()=1]')
    USETHISADDRESS_JP = (By.XPATH, '//div[contains(@id, \'-19\')]/div/div[position()=2]/form/div/div/div/div/div/span[position()=2]/span/input[position()=1]')

class AmazonSearchPageLocator(AmazonPageLocator):
    ASINRESULTS = (By.XPATH, '//li[contains(@id, \'result_\')]')
    ## usa
    ASINIMAGE_US_BS = (By.XPATH, './/div/div[position()=2]/div/div[position()=1]/div/div')
    ASINIMAGE_US_AC = (By.XPATH, './/div/div[position()=2]/div/div[position()=1]/div/div')
    ASINIMAGE_US = (By.XPATH, './/div/div/div/div[position()=1]/div/div')

    ASINTITLE_US_BS = (By.XPATH, './/div/div[position()=2]/div/div[position()=2]/div[position()=1]/div[position()=1]/a/h2')
    ASINTITLE_US_AC = (By.XPATH, './/div/div[position()=2]/div/div[position()=2]/div[position()=1]/div[position()=1]/a/h2')
    ASINTITLE_US_SP = (By.XPATH, './/div/div/div/div[position()=2]/div[position()=2]/div[position()=1]/a/h2')
    ASINTITLE_US = (By.XPATH, './/div/div/div/div[position()=2]/div[position()=1]/div[position()=1]/a/h2')

    ## usa small
    # ASINIMAGE_US_BS_S = (By.XPATH, './/div/div[position()=2]/div/div[position()=1]/div/div')
    # ASINIMAGE_US_AC_S = (By.XPATH, './/div/div[position()=2]/div/div[position()=1]/div/div')
    ASINIMAGE_US_S = (By.XPATH, './/div/div[position()=2]/div/a')

    # ASINTITLE_US_BS_S = (By.XPATH, './/div/div[position()=2]/div/div[position()=2]/div[position()=1]/div[position()=1]/a/h2')
    # ASINTITLE_US_AC_S = (By.XPATH, './/div/div[position()=2]/div/div[position()=2]/div[position()=1]/div[position()=1]/a/h2')
    ASINTITLE_US_SP_S = (By.XPATH, './/div/div[position()=4]/div[position()=1]')
    ASINTITLE_US_S = (By.XPATH, './/div/div[position()=3]/div[position()=1]')


    # jp
    # ASINIMAGE_BS_JP = (By.XPATH, './')
    # ASINIMAGE_SP_JP = (By.XPATH, './')
    # ASINIMAGE_AC_JP = (By.XPATH, './')
    ASINIMAGE_JP = (By.XPATH, './/div/div[position()=2]/div/div')
    ASINTITLE_SP_JP = (By.XPATH, './/div/div[position()=4]/div[position()=1]/a/h2')
    ASINTITLE_JP = (By.XPATH, './/div/div[position()=3]/div[position()=1]/a/h2')

    PAGENEXTSTRING = (By.ID, 'pagnNextString')



class AmazonRegisterPageLocator(AmazonPageLocator):
    USERENAME = (By.ID, 'ap_customer_name')
    PRONUNCIATION = (By.ID, 'ap_customer_name_pronunciation')
    EMAILNAME = (By.ID, 'ap_email')
    PASSWORD = (By.ID, 'ap_password')
    PASSWORDCHECK = (By.ID, 'ap_password_check')
    CONTINUESUBMIT = (By.ID, 'continue')


class AmazonAddressPageLocator(AmazonPageLocator):
    ADDADDRESS = (By.ID, 'ya-myab-plus-address-icon')
    FULLNAME = (By.ID, 'address-ui-widgets-enterAddressFullName')
    ADDRESSPHONE = (By.ID, 'address-ui-widgets-enterAddressPhoneNumber')
    ADDRESSLINE1 = (By.ID, 'address-ui-widgets-enterAddressLine1')
    ADDRESSLINE2 = (By.ID, 'address-ui-widgets-enterAddressLine2')
    ADDADDRESSSUBMIT = (By.XPATH, '//*[@id=\'address-ui-widgets-enterAddressFormContainer\']/span[position()=1]/span/input[position()=1]')
    ## US
    ADDRESSCITY = (By.ID, 'address-ui-widgets-enterAddressCity')
    ADDRESSSTATE = (By.ID, 'address-ui-widgets-enterAddressStateOrRegion')
    ADDRESSPOSTALCODE = (By.ID, 'address-ui-widgets-enterAddressPostalCode')
    ## JP
    ADDRESSPOSTALCODEONE = (By.ID, 'address-ui-widgets-enterAddressPostalCodeOne')
    ADDRESSPOSTALCODETWO = (By.ID, 'address-ui-widgets-enterAddressPostalCodeTwo')
    COUNTRYSELECT = (By.ID, 'address-ui-widgets-countryCode-dropdown-nativeId')
    UNITEDSTATEINDEX = 217
    ADDRESSSTATESELECT = (By.ID, 'address-ui-widgets-enterAddressStateOrRegion-dropdown-nativeId')
    ADDRESSSTATEOPTIONS_ZH = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', \
                              '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', \
                              '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', \
                              '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', \
                              '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
    ADDRESSSTATEOPTIONS_EN = ['Hokkaido', 'Aomori', 'Iwate', 'Miyagi', 'Akita', 'Yamagata', 'Fukushima', 'Ibaraki', 'Tochigi', 'Gunma', \
                              'Saitama', 'Chiba', 'Tokyo', 'Kanagawa', 'Niigata', 'Toyama', 'Ishikawa', 'Fukui', 'Yamanashi', 'Nagano', \
                              'Gifu', 'Shizuoka', 'Aichi', 'Mie', 'Shiga', 'Kyoto', 'Osaka', 'Hyogo', 'Nara', 'Wakayama', \
                              'Tottori', 'Shimane', 'Okayama', 'Hiroshima', 'Yamaguchi', 'Tokushima', 'Kagawa', 'Ehime', 'Kochi', 'Fukuoka', \
                              'Saga', 'Nagasaki', 'Kumamoto', 'Oita', 'Miyazaki', 'Kagoshima', 'Okinawas']

class AmazonSignInPageLocator(AmazonPageLocator):
    EMAILNAME = (By.ID, 'ap_email')
    CONTINUE = (By.XPATH, '//div[@id=\'authportal-main-section\']/div[position()=2]/div/div[position()=1]\
                        /form/div/div/div/div[position()=2]/span[position()=1]/span/input[position()=1]')
    PASSWORD = (By.ID, 'ap_password')
    SIGNINSUBMIT = (By.ID, 'signInSubmit')
    ACCOUNTSWITCHER = (By.XPATH, '//*[@id="ap-account-switcher-container"]/div[1]/div/div/div[2]/div[1]/div[2]/a/div')
