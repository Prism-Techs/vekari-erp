from django.contrib import admin
from .models import *

# Register your models here.
class RawMaterialMasterAdmin(admin.ModelAdmin):
    list_display = ('rm_id', 'rm_mat_name', 'rm_mat_code', 'rm_sec_type', 'rm_size', 'rm_stock_free', 'rm_stock_res', 'created_date', 'modify_date')
    search_fields = ['rm_id', 'rm_mat_name', 'rm_mat_code', 'rm_sec_type', 'rm_size']  # Add fields you want to search
    list_filter = ['rm_sec_type', 'rm_size']  # Add fields you want to filter

admin.site.register(RawMaterialMaster, RawMaterialMasterAdmin)
class CategoryMasterAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'c_name', 'create_by', 'create_date', 'modify_by', 'modify_date', 'is_active', 'closed_by')
    search_fields = ['category_id', 'c_name']
    list_filter = ['is_active']

class PartsMasterAdmin(admin.ModelAdmin):
    list_display = ('part_id', 'product_part_no', 'product_part_name', 'product_type', 'uom', 'category', 'product_cost', 'product_source_type', 'create_by', 'create_date', 'modify_by', 'modify_date', 'closed_by', 'aproved_by', 'is_active')  # Fix the typo here
    search_fields = ['part_id', 'product_part_no', 'product_part_name']
    list_filter = ['product_type', 'is_active']

admin.site.register(CategoryMaster, CategoryMasterAdmin)
admin.site.register(PartsMaster, PartsMasterAdmin)
@admin.register(PartsVendorsMaster)
class PartsVendorsMasterAdmin(admin.ModelAdmin):
    list_display = ('get_part_no', 'get_part_name', 'vendor', 'part_vendor_make', 'part_vendor_model', 'part_vendor_cost', 'is_active')
    search_fields = ['part__product_part_no', 'vendor__v_name']
    list_filter = ['is_active']

    def get_part_no(self, obj):
        return obj.part.product_part_no

    def get_part_name(self, obj):
        return obj.part.product_part_name

    get_part_no.short_description = 'Part No'
    get_part_name.short_description = 'Part Name'

# Registering StoreLocation with the admin interface
@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ('store_location_id', 'part', 'row_no', 'rack_no', 'shelf_no', 'tub_no', 'remark')
    search_fields = ['part__product_part_no']  # Adjust based on your needs

# Registering SubpartMaster with the admin interface
@admin.register(SubpartMaster)
class SubpartMasterAdmin(admin.ModelAdmin):
    list_display = ('subpart_master_id', 'get_part_no','get_part_name', 'get_subpart_no','get_subpart_name', 'sub_part_qty', 'subpart_type', 'subpart_subtype', 'part_is_active', 'created_by', 'create_date', 'modify_by', 'modify_date')
    search_fields = ['part__product_part_no', 'sub_part__product_part_no']  # Adjust based on your needs
    list_filter = ['part_is_active']
    def get_part_no(self, obj):
        return obj.part.product_part_no

    def get_part_name(self, obj):
        return obj.part.product_part_name

    get_part_no.short_description = 'Part No'
    get_part_name.short_description = 'Part Name'    
    def get_subpart_no(self, obj):
        return obj.sub_part.product_part_no

    def get_subpart_name(self, obj):
        return obj.sub_part.product_part_name

    get_part_no.short_description = 'Part No'
    get_part_name.short_description = 'Part Name'    
    get_subpart_no.short_description = 'SubPart No'
    get_subpart_name.short_description = 'SubPart Name'    
