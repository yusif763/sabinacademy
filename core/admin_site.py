from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = 'Sabina Academy Admin'
    site_title = 'Sabina Academy Admin Portal'
    index_title = 'Welcome to Sabina Academy Admin Panel'

admin_site = CustomAdminSite(name='custom_admin')
