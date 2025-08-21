from datetime import timedelta

class Config:
    SECRET_KEY = 'your-secret-key'
    JWT_SECRET_KEY = 'your-jwt-secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    MONGODB_SETTINGS = {
        'db': 'mukata',
        'host': 'mongodb://loeitech_admin_2:G7%23u4sK!8zWb@202.29.231.188:27019/mukata?authSource=admin'
    }