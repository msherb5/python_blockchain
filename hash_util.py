import hashlib as hl
import json

def hash_string_256(string):
    return hl.sha256(string).hexdigest()#hexdigest makes dump readable

def hash_block(block):
    #join syntax to change printing from looking like a list, to a string connected by dashes
    
    #you need copy() so youre not constantly overwriting old dicts of other blocks (Use only if manipulating data)
    hashable_block = block.__dict__.copy()
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode()) 