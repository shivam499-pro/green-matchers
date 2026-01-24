from fastapi import FastAPI 
import app 
 
print("=== AVAILABLE ROUTES ===") 
for route in app.app.routes: 
    if hasattr(route, "path"): 
        methods = getattr(route, 'methods', ['ANY']) 
        print(f"PATH: {route.path}") 
        print(f"  METHODS: {methods}") 
        print(f"  NAME: {getattr(route, 'name', 'N/A')}") 
        print() 
