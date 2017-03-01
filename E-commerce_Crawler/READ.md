# 项目讲解

##**1688**
####需求说明：
1. 抓取1688上商铺的公司信息
2. 抓取1688上店铺的产品信息

####代码结构说明：
- 商品信息的抓取文档
    1. bussiness_info.py

- 用于公司信息的抓取
    1. company_info.py
           
- 用于处理1688店铺的url
    1. file_tool.py
    
- 用于破解1688验证码的机器学习库
    1. iconset
    
    
##**Amazon**
####需求说明：
1. Camel_getUPCnEAN，获取asin在camel上的UPC和EAN码
2. 抓取Amazon的商品信息
3. 按组抓取信息以及按公有DB格式保存

####代码结构说明：
- 获取asin在camel上的UPC和EAN码
    1. Camel_getUPCnEAN/get_detail.py 

- 抓取Amazon的商品信息
    1. get_group_url.py
    2. get_group_asin.py
    3. get_group_info.py
    4. ProApiandERPGateway
- 抓取代码
    1. get_asin.py 获取品类页面的url
    2. get_api_file 根据api获取信息
    3. get_item_info.py 获取信息
- Amazon的API
    1. ProApiandERPGateway

- amazon抓取书籍的代码:
    1. books_china_has.py
    2. buybox_book_us.py

###抓取流程：
- get_asin.py 获取品类页面的url
- get_api_file 根据api获取信息
- get_item_info.py 获取信息

##**BestBuy**
####需求说明：
1. 用于抓取BesBuy网站上的商品数据
2. 获取距离某商品最近的店铺信息

####代码结构说明：
- 抓取商品信息：
    1. get_html.py
    2. get_id.py
    3. get_info.py
 
- 最近店铺信息： 
    1.get_store.py

##**Half.ebay**
####需求说明：
1. 抓取half_ebay上的商品信息
2. 每日更新已抓到的half_ebay商品的价格数据

####代码结构说明：
- 用于抓取half_ebay上的数据
    1. 代码： snatch_half_book_info.py
    2. 文件：./Data/snatch/total_asin_offshelf_*.txt    

- 用于更新价格数据
    1. 代码：update_half_book_info.py
    2. 文件：./update/isbn/asins_*.csv 
            ./update/isbn/even_compare*.csv

- 用于把抓取到的数据合并，去重和获得未抓的数据asin
    1. file_os.py

- 用来处理获得的数据，并匹配sku
    1. 代码：deal_update_file.py
    1. 生成：even_compare*.csv和asins_*.csv文件，用于更新操作

####文件说明：
- asin_result是从amazon市场抓下来的所有信息，子文件夹是以品类id命名的，每个子文件夹下的asins_more.txt记录的是品类下的ASIN
- get_price_url.py 和 get_asins.py 是抓取脚本
- categorys.txt 是amazon市场书籍品类信息
- filter_new_asin.py的脚本是用来asin_result文件夹下各个子文件夹的ASIN要跟业务已上架的ASIN去重的
- half.ebay/update/isbn/isbn_result.csv 已上架的ISBN
- 再就是amazon市场抓取的是ASIN，但是给的已上架的信息是13位ISBN这之间要做转换才能去重，
- 建议是统一为13位ISBN,因为我用ASIN跑价格自动更新程序抓不到的ASIN很多，但是ISBN不会。

###现在要做的就是对这些ASIN去重
1. asin_result文件夹下各个子文件夹下的ASIN要相互去重，
2. asin_result文件夹下各个子文件夹的ASIN要跟业务已上架的ASIN去重。
    - filter_new_asin.py的脚本是用来asin_result文件夹下各个子文件夹的ASIN要跟业务已上架的ASIN去重的，你可以参考一下。
    - 已上架的ISBN我也已经转换成csv格式，是half.ebay/update/isbn/isbn_result.csv。
    - amazon市场抓取的是ASIN，但是给的已上架的信息是13位ISBN这之间要做转换才能去重,建议是统一为13位ISBN,因为我用ASIN跑价格自动更新程序抓不到的ASIN很多，但是ISBN不会。
    
3. snatch_half_book_info.py
   update_half_book_info.py
   抓取和更新添加过滤条件的脚本

4. 将业务提供的asin分店铺建文件保存，sun_finish.txt even_finish.txt,还有死账号的asin文件 账号名_finish.txt
5. 每天提取sun_finish.txt和even_finish.txt中的asin进行更新，按照更新的模板shell脚本自动跑，根据经验出单集中在下午和晚上，可以在中午12点前跑完提供给苗苗，我。


## **Newegg**
1. 运行run.sh删除杂余文件
2. 在get_items.py中替换抓取URl以及页码，运行get_items.py抓取产品id
3. 运行get_info.py抓取产品信息

####需求说明：
1. 抓取Newegg的商品信息
2. 按组信息以及按公有DB格式保存

####代码结构说明：
- 抓取Newegg的商品信息
    1. get_items.py
    2. get_info_ca.py or get_info.py

- 按组信息以及按公有DB格式保存
    1. get_group_info.py
    2. get_info_db.py

##项目12：Pro_Finance
####需求说明：
1. 从Amazon的MWS上获取Amazon的Finance报表
2. 从Amazon的MWS上获取Amazon的Report报表
[在线测试网址](https://mws.amazonservices.com/scratchpad/index.html)

####代码结构说明：
- Finance报表
    1. get_groupid_list.py
    2. get_order_xml.py
    3. get_info_save.py
    4. detele_repeat_xml.py

- Report报表
    1. get_request_id.py -> get_request_obj() 把request.xml文件保存到Report_xml/文件夹下，命名为店铺名+.xml
    2. get_request_id.py -> get_request_id（） 从Report_xml/store_name.xml中解析出report-id，保存到Result_data/request_id.txt
    3. get_report_file.py -> download_request_file() 从Result_data/request_id.txt中读取report-id，提交请求并保存数据。
    4. get_report_file.py -> spilt_report_file() 把保存下来的report数据按市场和时间分开。
    5. get_report_file.py -> delet_file() 删除未处理前的数据。
    6. get_info_save.py -> deal_file() 是之前处理report数据的代码，与下载数据无关，暂不用。

##S3_Image
####需求说明：
- 根据URL从S3服务器上把图片取下来  

####代码结构说明：
- 根据URL从S3服务器上把图片取下来
    1. save_image_from_s3.py

## **Walmart**
####需求说明：
1. 根据[walmart](www.walmart.com)上要抓取的品类url抓取品类下condition 为new价格不低于50的商品id，再利用walmart的api抓取商品信息  
2. 按组信息以及按公有DB格式保存###文件说明：

####代码结构说明：
- 抓取Walmart上的商品信息
    1. get_[品类名]_list.py	根据url拆分获得商品数量小于1000的价格区间url	输出文件：list.txt
    2. get_items_id.py	获取商品id	输入文件：list.txt	输出文件：itemsId_last.txt
    3. get_items_info.py	解析商品信息	输入文件：itemsId_last.txt	输出文件：items.csv
    4. result文件夹	保存结果信息

- 按组信息以及按公有DB格式保存
    1. get_items_db.py

- 保留（代码还未仔细看，现进行的抓取未用到）：
 get_category.py
 get_items_id.py
 get_items_info.py
 get_items_list.py

- category文件夹
- result文件夹	记录结果记录

###运行说明：
- 注：这是个人习惯，不习惯可以按自己风格来
- 每个品类建立一个文件夹：[品类名]，将该品类的url写入get_[品类名]_list.py的url变量中。
- 依次运行：
    1. python get_[品类名]_list.py
    2. python get_items_id.py
    3. python get_items_info.py

##bhphoto
####需求说明：
- BH网站的商品信息抓取

####代码结构说明：
- 商品抓取
    1. get_info.py

##项目6：FRYs
####需求说明：
- FRYs网站的商品信息抓取

####代码结构说明：
- 商品抓取
    1. get_info.py

##productinfo
####需求说明：
1. Amazon的API测试
2. 把asin转换成isbn

####代码结构说明：
- 把asin转换成isbn
    1. test.py
- Amazon的API测试
    1. test1.py