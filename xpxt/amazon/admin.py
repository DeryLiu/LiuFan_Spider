# coding=utf-8
from django.contrib import admin
from .models import Category, Rank, Product, Seller

admin.AdminSite.site_header = u'星商选品系统'
admin.AdminSite.site_title = u'星商选品系统'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')

    search_fields = ('name', )

    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = u'产品数量'


class RankInline(admin.StackedInline):
    model = Rank
    readonly_fields = ('create_date',)
    fields = ('main_rank', 'other_ranks', 'create_date')
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url', 'brand', 'seller_count', 'star', 'recent_rank')

    list_filter = ('category__name', 'brand', 'star')

    search_fields = ('name', 'brand')

    inlines = [RankInline]


class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'product_count')

    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = u'产品数量'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Seller, SellerAdmin)
