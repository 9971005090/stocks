from flask import Blueprint
import importlib
import os

api_bp = Blueprint('api', __name__, url_prefix='/api')

def auto_register_modules(bp, module_path='module'):
    base_path = os.path.join(os.path.dirname(__file__), '..', module_path)
    for module_name in os.listdir(base_path):
        module_dir = os.path.join(base_path, module_name)
        if os.path.isdir(module_dir) and os.path.exists(os.path.join(module_dir, 'routes.py')):
            module_import_path = f'{module_path}.{module_name}.routes'
            try:
                mod = importlib.import_module(module_import_path)
                if hasattr(mod, 'register'):
                    mod.register(bp)
                    print(f'✅ {module_name} 모듈 등록 완료')
            except Exception as e:
                print(f'❌ {module_name} 등록 실패: {e}')

auto_register_modules(api_bp)
