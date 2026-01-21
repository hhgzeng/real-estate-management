from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.db import transaction, connection
from .models import User

@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if sender.name == 'accounts':
        # 获取 User 模型对应的数据库表名
        table_name = User._meta.db_table
        
        # 检查表是否已存在于数据库中
        if table_name in connection.introspection.table_names():
            with transaction.atomic():
                # 检查是否存在管理员账号
                admin_exists = User.objects.filter(role='admin').exists()
                
                if not admin_exists:
                    # 创建默认管理员账号
                    User.objects.create(
                        username='admin',
                        password='admin123',
                        role='admin'
                    )
                    print('Default admin account created successfully.')