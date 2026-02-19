import sys
import os

try:
    import zstandard
    print(f"zstandard location: {zstandard.__file__}")
    print(f"zstandard version: {getattr(zstandard, '__version__', 'NO VERSION')}")
except ImportError:
    print("zstandard not found")
except Exception as e:
    print(f"Error importing zstandard: {e}")

print("\nsys.path:")
for p in sys.path:
    print(f"  {p}")
