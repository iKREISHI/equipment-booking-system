import os
import environ
from pathlib import Path




ENV_PATH = Path(__file__).resolve().parents[2]

env = environ.Env()

env_file = ENV_PATH / '.env'

if env_file.exists():
    environ.Env.read_env(str(env_file))

# POSTGRES
DATABASES_URL = env.db(
    'DATABASE_URL',
    default='postgres://postgres:postgres@127.0.0.1:5432/equipment-system'
)

# MINIO
MINIO_ROOT_USER = env('MINIO_ROOT_USER', default='minioroot')
MINIO_ROOT_PASSWORD = env('MINIO_ROOT_PASSWORD', default='minioroot')
MINIO_INSTANCE_ADDRESS = env('MINIO_INSTANCE_ADDRESS', default='127.0.0.1:9000')

SERVER_BACKEND_IP_ADDRESS = env('SERVER_BACKEND_IP_ADDRESS', default='127.0.0.1:8000')