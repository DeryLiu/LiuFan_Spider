from Tools import ALL_CONFIG
import os
import copy

def deal_group_info(info):
    # print info
    if info != []:
        if info[0][6] == 'Order':
            if info[0][15] == 'AFN':
                principal = float(info[0][14])
                if info[1][13] == 'Shipping':
                    shipping = float(info[1][14])
                    # print 'AFN Shipping XXX: ',shipping
                else:
                    shipping = 0.0

                new_shipping = (principal + shipping) * 0.5            # new_shipping = (float(principal) + float(shipping)) * 0.5
                if new_shipping*1000%10 == 5:
                    if new_shipping < 0:
                        new_shipping = new_shipping - 0.001
                    else:
                        new_shipping = new_shipping+0.001
                    new_shipping = round(new_shipping,2)

                new_fba_fee = new_shipping - shipping
                if new_fba_fee*1000%10 == 5:
                    if new_fba_fee < 0:
                        new_fba_fee = new_fba_fee - 0.01
                    else:
                        new_fba_fee = new_fba_fee+0.001
                    new_fba_fee = round(new_fba_fee,2)

                if new_fba_fee < 0:
                    # print 'AFN new_fba_fee',new_fba_fee,info[-2][13]
                    if info[-2][13] == 'FBAWeightBasedFee':
                        # fba_fee = float(info[-2][14]) + float(info[-3][14]) + float(info[-4][14])
                        info[-2][14] = float(info[-2][14])+new_fba_fee
                        print ('has FBAWeightBasedFee: ',info[-2][14])
                    else:
                        # fba_fee = float(info[-2][14]) + float(info[-3][14])
                        fbaWeightBasedFee = copy.deepcopy(info[0])
                        fbaWeightBasedFee[13]= 'FBAWeightBasedFee'
                        fbaWeightBasedFee[14] = new_fba_fee
                        print ('This is AFN fbaWeightBasedFee: ',fbaWeightBasedFee)
                        info.insert(-2,fbaWeightBasedFee)

                if new_shipping < 0.0:
                    print ('new_shipping',new_shipping,info[1][13])
                    if info[1][13] == 'Shipping':
                        info[1][14] = float(info[1][14])+new_shipping
                        print ('has shipping: ',info[1][14])
                    else:
                        Shipping = copy.deepcopy(info[0])
                        Shipping[13] = 'Shipping'
                        Shipping[14] = new_shipping
                        print ('This is AFN Shipping: ',Shipping)
                        info.insert(1,Shipping)

            elif info[0][15] == 'MFN':
                principal = float(info[0][14])
                # shipping_list = [ship[14] for ship in info if ship[13] == 'Shipping']
                # # print type(shipping_list)
                # # shipping = '\t'.join(shipping_list)
                # print 'lalala',shipping_list

                if info[1][13] == 'Shipping':
                    shipping = info[1][14]
                else:
                    shipping = 0

                new_shipping = (float(principal) + float(shipping)) * 0.5
                if new_shipping*1000%10 == 5:
                    new_shipping = new_shipping + 0.001
                    new_shipping = round(new_shipping,2)

                new_fba_fee = new_shipping - float(shipping)
                if new_fba_fee*1000%10 == 5:
                    new_fba_fee = new_fba_fee+0.001
                    new_fba_fee = round(new_fba_fee,2)

                if new_shipping < 0:
                    print ('new_shipping_MFN: ',new_shipping,info[1][13])

                    if 'Shipping' in (infship[13] for infship in info):
                        for infoship in info:
                            if infoship[13] == 'Shipping':
                                infoship[14] = float(infoship[14])+new_shipping
                    else:
                        Shipping = copy.deepcopy(info[0])
                        Shipping[13] = 'Shipping'
                        Shipping[14] = float(new_shipping)
                        info.insert(1, Shipping)
                        print ('this is MFN shipping: ',Shipping)

                if new_fba_fee < 0:
                    print ('AFN not equal 0: ',new_fba_fee)
                    fbaWeightBasedFee = copy.deepcopy(info[0])
                    fbaWeightBasedFee[13] = 'FBAFee'
                    fbaWeightBasedFee[14] = round(new_fba_fee,2)
                    info.append(fbaWeightBasedFee)
            else:
                print ('xxxx')
        else:
            print ('xxxx')
    else:
        pass

    # print info

    with open(ALL_CONFIG.REPORT_NEW_INFO_FILE,'a') as new_info:
        for i in info:
            print (i)
            new_info.write('\t'.join(str(s) for s in i))

def deal_file():
    # read the report data
    with open(ALL_CONFIG.REPORT_FILE,'r') as weekinfo:
        deal_list = []
        insert = []
        # go through the file
        for info in weekinfo.readlines():
            info_alone_list = info.split(',')
            deal_list.append(info_alone_list)
            try:
                # print info_alone_list[13]
                if info_alone_list[13] == 'Principal':
                    deal_group_info(insert)
                    # re_list = deal_group_info(insert)
                    # deal_list.extend(re_list)
                    insert = [info_alone_list] # the one who info_alone_list[13] == 'Principal'
                else:
                    insert.append(info_alone_list)
            except Exception as e:
                pass
        deal_group_info(insert)

if __name__ == '__main__':
    deal_file()