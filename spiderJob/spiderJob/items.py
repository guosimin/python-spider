# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# ItemLoader
# 是分离数据的另一种方式，可以将数据的分离和提取分为两部分，
# 默认使用xpath, css数据提取方式，
# 让代码更加整洁，更加清晰。
from  scrapy.loader import ItemLoader
from scrapy.loader.processors import *

# class ArticleItemLoader(ItemLoader):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     default_output_processor = TakeFirst()

# 如果list为空则不会进行处理，这种情况需要重载MapCompose类的__call__方法
class MapComposeCustom(MapCompose):
    #自定義MapCompose，當value沒元素時傳入" "
    def __call__(self, value, loader_context=None):
        if not value:
            value.append(" ")
        values = arg_to_iter(value)
        if loader_context:
            context = MergeDict(loader_context, self.default_loader_context)
        else:
            context = self.default_loader_context
        wrapped_funcs = [wrap_loader_context(f, context) for f in self.functions]
        for func in wrapped_funcs:
            next_values = []
            for v in values:
                next_values += arg_to_iter(func(v))
            values = next_values
        return values

#TakeFirst来作为默认输出处理器，但该函数会筛掉空字符，因此重载该类的__call__
class TakeFirstCustom(TakeFirst):
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value.strip() if isinstance(value, str) else value


# 过滤空格
def cutSpace(value):
    result = str(value).replace(" ","");
    result = str(result).replace("\n", "");
    result = str(result).replace("\r", "");
    return result


class SpiderjobItem(scrapy.Item):
    t1 = scrapy.Field(
        input_processor=MapComposeCustom(cutSpace),
        output_processor=Join()
    )  # 标题
    t2 = scrapy.Field(
        input_processor = MapComposeCustom(cutSpace),
        output_processor = Join()
    )  # 标题
    t3 = scrapy.Field(
        input_processor = MapComposeCustom(cutSpace),
        output_processor = Join()
    )  # 标题
    t4 = scrapy.Field(
        input_processor=MapComposeCustom(cutSpace),
        output_processor=Join()
    )  # 标题
    pass