#Starmerx_Spider
####需求说明：
1. 抓取Amazon某一类的热销排行
2. 把图片上传到S3服务器

####代码结构说明：
- 抓取Amazon某一类的热销排行
    1. amazon_spider.py
    2. json2xls.py

- Ebay爬虫代码
	- **spider.py**——爬虫的基类，定义一些爬虫的基本操作
	- **ebay_spider.py**——ebay爬虫的具体实现
	- **amazon_spider.py**——亚马逊爬虫的具体实现，用于获取热销的产品
	- **.conf**——爬虫的配置文件
	- **header.txt**——爬虫的header的配置文件
	- **proxy.txt**——爬虫的代理的配置文件
	- **ua.txt**——爬虫的ua的配置文件
	- **pool.py**——线程池的一个实现
	- **category_ids.txt**——需要抓取的品类id的文件
	- **product_ids.txt**——需要抓取的产品id的文件
	- **json2xls.py**——亚马逊热销产品json文件转为xlsx文件
    
- 把图片上传到S3服务器
    1. PicResize/S3.py

- 文档：
    - * celery.pptx
    - * Celery分布式环境测试.docx
    - * 爬虫管理系统功能设计方案.docx
    - * 数据库详细设计说明文档.doc
    - * 基于Celery的分布式爬虫流程.dia
    - * 爬虫处理流程.dia
    - * 爬虫管理系统er图.dia
    - * 爬虫管理系统系统架构图.dia
    - * 星商选品系统.dia
    - * 爬虫原型图.ep
    - * Toys&Games.txt
    - * Toys&Games.xlsx

####服务器：
- ssh zhaolei@54.208.83.161
- ssh zhaolei@54.211.80.208       
- ssh zhaolei@54.211.156.194   
- ssh gaomon@54.173.252.17
- 密码：Tianhu2016

[Amazon所有的热销的品类链接地址](https://www.amazon.com/gp/bestsellers/
)


####热销商品格式
```
	{
    	"star": "4.0",		# 评分
    	"name": "Calico Critters Treehouse Gift Set",		# 产品名称
    	"url": "https://www.amazon.com/Calico-Critters-Treehouse-Gift-Set/dp/B00FB5VP5S/",		# 产品链接
    	"brand": "Calico Critters",		产品品牌
    	"other_ranks": [		# 产品在叶子分类中的排名情况
        {
            "path": "Toys & Games > Preschool > Toddler Toys > Pretend Play > Toy Figure Playsets",		＃ 品类路径
            "rank": 36		＃ 叶子分类排名
        },
        {
            "path": "Toys & Games > Preschool > Pre-Kindergarten Toys > Pretend Play > Toy Figure Playsets",
            "rank": 72
        },
        {
            "path": "Toys & Games > Action & Toy Figures > Playsets & Vehicles > Playsets",
            "rank": 95
        }
    	],
    	"rank": 5335,		# 产品在当前分类中的排名
    	"sellers": [
        {
            "url": "www.amazon.com/shops/A8JLX967PP2F",		#　卖家店铺链接
            "name": "Peanuts Toy Barn"		# 卖家店名
        },
        {
            "url": "www.amazon.com/shops/A1JP9BEFA6KKRE",
            "name": "The Corner Toy Store"
        },
        {
            "url": "www.amazon.com/shops/A24C01ES5MR37O",
            "name": "American Premium Store"
        },
        {
            "url": "www.amazon.com/shops/AMYWEK8M9TLQG",
            "name": "Educational Toys Planet"
        },
        {
            "url": "www.amazon.com/shops/A3LAZMIHXKTKT",
            "name": "Small Town Toy"
        },
        {
            "url": "www.amazon.com/shops/A1Y4GWDLS1THE8",
            "name": "LaToys Etcetera"
        },
        {
            "url": "www.amazon.com/shops/AQNU03YZFZQ4H",
            "name": "Kiddie Collection, Inc."
        },
        {
            "url": "www.amazon.com/shops/AT947EFSBP07C",
            "name": "thetargetbuys"
        },
        {
            "url": "www.amazon.com/shops/A1FPS52GNYUG5P",
            "name": "sushka"
        },
        {
            "url": "www.amazon.com/shops/A3M46K8KE1WDTV",
            "name": "The Hobby Shop, Aberdeen NJ"
        },
        {
            "url": "www.amazon.com/shops/A1NZEJZ10332NK",
            "name": "Toys & Co."
        },
        {
            "url": "www.amazon.com/shops/A2MUX0PLSCVXNV",
            "name": "Oakridge Hobbies & Toys"
        },
        {
            "url": "www.amazon.com/shops/A2WZFZGZNTENC7",
            "name": "E-MAGINE TOYS"
        },
        {
            "url": "www.amazon.com/shops/A23M9QXIF0J7JZ",
            "name": "PUZZLEZOO"
        },
        {
            "url": "www.amazon.com/shops/A14GF2KQTXEUIZ",
            "name": "Adventure Hobbies & Toys"
        },
        {
            "url": "www.amazon.com/shops/A3Q8WBFJ8B1NMZ",
            "name": "Really Great Toys"
        },
        {
            "url": "www.amazon.com/shops/A118MFVTOVHS2M",
            "name": "Totally Thomas"
        },
        {
            "url": "www.amazon.com/shops/A225ZHOYG8CLUO",
            "name": "Neat Toys"
        },
        {
            "url": "www.amazon.com/shops/ATK4T3E83Q514",
            "name": "Toys & Playtime Oasis"
        },
        {
            "url": "www.amazon.com/shops/A1A3JQLHV3ZO05",
            "name": "Best Brands Toys"
        },
        {
            "url": "www.amazon.com/shops/A33L73DVE1785U",
            "name": "Specialty Toy Store"
        },
        {
            "url": "www.amazon.com/shops/A31Q3R4VEAJYPZ",
            "name": "Wild Kingdom of Toys"
        },
        {
            "url": "www.amazon.com/shops/A38LPEX1R76E9P",
            "name": "Wall of Fame"
        }
    	],
    	"images": [		# 产品图片
        	"https://images-na.ssl-images-amazon.com/images/I/41Y%2By3F5KxL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61fxCq6IcZL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/41wG0cFfnzL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/514dmcHcKlL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61%2Boqwzq1zL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61fWEO6tJdL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/410htAiqIyL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/41Y%2By3F5KxL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61fxCq6IcZL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/41wG0cFfnzL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/514dmcHcKlL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61%2Boqwzq1zL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/61fWEO6tJdL.jpg",
        	"https://images-na.ssl-images-amazon.com/images/I/410htAiqIyL.jpg"
    	]
	}
```