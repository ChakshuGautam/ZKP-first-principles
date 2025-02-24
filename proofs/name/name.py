#!/usr/bin/env python3
"""
Simplified Zero-Knowledge Proof (ZKP) using a custom simple hash.

This code demonstrates how to prove that you know a secret string (e.g., "Alice")
without revealing it. Instead of a cryptographically secure hash (like SHA-256),
we use a simple function that maps letters: A=1, B=2, …, Z=26.
The Schnorr protocol is then executed step by step.

Note: This code is for educational purposes and is NOT secure for real applications.
"""

def simple_hash(s: str, modulus: int) -> int:
    """
    A simple hash that maps each letter A-Z (case-insensitive) to a number 1-26,
    then accumulates these values using powers of 27.
    
    For example, "CHAKSHU" is processed as:
    C -> 3, H -> 8, A -> 1, K -> 11, S -> 19, H -> 8, U -> 21
    The hash is computed as: 21 + 8*27^1 + 19*27^2 + 11*27^3 + 1*27^4 + 8*27^5 + 3*27^6
    """
    h = 0
    base = 27
    s = s.upper()
    # Reverse the string to match the mathematical formula where rightmost char has power 0
    for i, char in enumerate(reversed(s)):
        if 'A' <= char <= 'Z':
            value = ord(char) - ord('A') + 1
            h += value * (base ** i)
    print(f"hash of {s} = {h}")
    return h % modulus

def main():
    print("=== Simplified Zero-Knowledge Proof Demonstration ===\n")
    
    # Step 0: Define our secret and our group parameters.
    secret = "Chakshu"  # This is the secret string we want to prove we know.
    print("Secret (to be proven):", secret)
    
    # Parameters matching the readme example
    p = 23   # prime modulus
    q = 22   # order (p-1)
    g = 5    # generator
    print(f"Group parameters: p = {p}, q = {q}, generator g = {g}\n")
    
    # Step 1: Map the secret string to a number using our simple hash
    x = 6  # Using the example value from readme for demonstration
    print("Step 1: Simple hash of secret (x) =", x)
    
    # Step 2: Compute the public key y = g^x mod p.
    y = pow(g, x, p)
    print("Step 2: Public key y = g^x mod p =", y, "\n")
    
    # --- Now we execute the Schnorr protocol ---
    # Step 3a: Prover picks a random r (from 0 to q-1).
    import random
    sys_rand = random.SystemRandom()
    r = 4  # Example random value from readme
    print("Step 3a: Prover picks random r =", r)
    
    # Step 3b: Prover computes commitment: t = g^r mod p.
    t = pow(g, r, p)
    print("Step 3b: Prover computes commitment t = g^r mod p =", t)
    
    # Step 3c: Verifier picks a random challenge c.
    c = 3  # Example challenge from readme
    print("Step 3c: Verifier picks challenge c =", c)
    
    # Step 3d: Prover computes response: s = (r + c * x) mod q.
    s = (r + c * x) % q
    print("Step 3d: Prover computes response s = (r + c * x) mod q =", s)
    
    # Step 3e: Verifier checks that g^s mod p equals t * y^c mod p.
    lhs = pow(g, s, p)
    rhs = (t * pow(y, c, p)) % p
    print("Step 3e: Verifier computes g^s mod p =", lhs)
    print("         and computes t * y^c mod p =", rhs)
    
    if lhs == rhs:
        print("\nVerification succeeded: The proof is accepted.")
    else:
        print("\nVerification failed: The proof is rejected.")

if __name__ == "__main__":
    main()
