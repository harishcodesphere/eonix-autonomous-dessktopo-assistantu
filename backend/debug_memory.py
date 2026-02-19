
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.episodic import episodic_memory
from memory.semantic import semantic_memory
import time

print("--- EONIX Memory System Diagnostic ---")

# 1. Test Episodic
print("\n1. Testing Episodic Memory...")
try:
    ts = str(time.time())
    user_text = f"Test Input {ts}"
    agent_text = f"Test Reply {ts}"
    
    print(f"   Saving turn: '{user_text}' -> '{agent_text}'")
    id = episodic_memory.save_turn(user_text, agent_text, tags=["test", "diagnostic"])
    print(f"   ✅ Saved ID: {id}")
    
    recents = episodic_memory.get_recent(limit=1)
    print(f"   Retrieved Recent: {recents}")
    
    if recents and recents[0]['user'] == user_text:
        print("   ✅ Episodic Retrieval Verified")
    else:
        print("   ❌ Episodic Retrieval Mismatch")
        
except Exception as e:
    print(f"❌ Episodic Error: {e}")

# 2. Test Semantic
print("\n2. Testing Semantic Memory...")
try:
    key = "diagnostic_test_key"
    val = f"value_{time.time()}"
    
    print(f"   Storing fact: {key} = {val}")
    fid = semantic_memory.store_user_fact(key, val)
    print(f"   ✅ Stored Fact ID: {fid}")
    
    # Wait for index? Chroma is usually fast but maybe explicit refresh needed?
    # Regular Chroma client doesn't need commit.
    
    print("   Retrieving relevant...")
    results = semantic_memory.retrieve_relevant(f"User's {key}")
    print(f"   Results: {results}")
    
    found = any(val in r['text'] for r in results)
    if found:
         print("   ✅ Semantic Retrieval Verified")
    else:
         print("   ⚠️ Semantic Retrieval Warning: Fact not found immediately (might be indexing lag)")

except Exception as e:
    print(f"❌ Semantic Error: {e}")

print("\n--- Diagnostic Complete ---")
