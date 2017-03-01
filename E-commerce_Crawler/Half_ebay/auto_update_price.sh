#!/bin/sh

#comments


cd `dirname $0`


echo $(date) >>log/crontab_update_price.log

python update_half_book_info.py>>log/crontab_update_price.log


