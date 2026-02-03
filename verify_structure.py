import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath('.'))

print("--- Starting Verification ---")

errors = []

# 1. Check Directory Existence
required_dirs = [
    'backend', 'frontend', 'common', 'database',
    'frontend/templates', 'frontend/templates/pages', 'frontend/templates/components',
    'frontend/static'
]
for d in required_dirs:
    if not os.path.isdir(d):
        errors.append(f"Missing Directory: {d}")
    else:
        print(f"OK: Directory {d} exists")

# 2. Check Import of app.py and Blueprints
try:
    # Set dummy env vars potentially needed for imports (though code looks safe)
    os.environ['FLASK_SECRET'] = 'test'
    
    from app import app
    print("OK: Imported app.py successfully")
    
    # Check config
    # Flask validates static folder relative to root path usually, but let's check the path stored
    t_folder = os.path.abspath(app.template_folder)
    s_folder = os.path.abspath(app.static_folder)

    if not os.path.isdir(t_folder):
        errors.append(f"Config Error: template_folder resolved to '{t_folder}' which does not exist")
    else:
        print(f"OK: template_folder exists at '{t_folder}'")

    if not os.path.isdir(s_folder):
        errors.append(f"Config Error: static_folder resolved to '{s_folder}' which does not exist")
    else:
        print(f"OK: static_folder exists at '{s_folder}'")

except ImportError as e:
    errors.append(f"Import Error: {e}")
except Exception as e:
    errors.append(f"Runtime Error during import: {e}")

# 3. Check specific template files existence
required_files = [
    'frontend/templates/pages/index.html',
    'frontend/templates/pages/about.html',
    'frontend/templates/pages/product.html',
    'frontend/templates/components/navbar_secondary.html',
    'frontend/templates/components/footer.html'
]

for f in required_files:
    if not os.path.isfile(f):
         errors.append(f"Missing File: {f}")
    else:
         print(f"OK: File {f} exists")

if errors:
    print("\nXXX ERRORS FOUND XXX")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)
else:
    print("\n>>> ALL CHECKS PASSED <<<")
    sys.exit(0)
