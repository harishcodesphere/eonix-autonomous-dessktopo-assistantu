import traceback
try:
    import chromadb
    print("SUCCESS: chromadb imported successfully")
    print(f"Version: {chromadb.__version__}")
except Exception:
    print("FAILURE: chromadb import failed")
    traceback.print_exc()
