from django.urls import path,include
from . import views


urlpatterns=[
    path('/product-form',views.productForm,name='productForm'),
    path('/add-product',views.addProduct,name='add_product'),
    path('/view-products',views.viewProducts,name='view_products'),
    path('/edit-product/<int:product_id>',views.editProduct,name='edit_product'),
    path('/update-product/<int:product_id>',views.updateProduct,name='update_product'),
    path('/delete-product/<int:product_id>',views.deleteProduct,name='delete_product'),


    path('/contact/', views.contact_view, name='contact'),
]