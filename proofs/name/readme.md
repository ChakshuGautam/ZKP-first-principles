## Step 1: Mapping a String to a Number

Every string can be converted into a number. In cryptography we do this with a hash function. Think of a hash function 𝐻 as a black box that "scrambles" an input into a (typically) very large number in a fixed range.

$$string \ S = "Chakshu"$$

We then compute:

$$x = H("Chakshu") \mod q$$

where $q$ is a large prime (we'll choose its value later).
Here, $x$ is now a number that "represents" your name—but by itself it doesn't reveal that your name is $"Chakshu"$.

Let's assume a simple hash that maps each letter A-Z (case-insensitive) to a number 1-26, then accumulates these values in a polynomial with base 27. Or in symbolic match

$$H(s) = \sum_{i=0}^{n} a_i \cdot 27^i$$

where $a_i$ is the $i$-th letter of the string $s$ and $n$ is the length of the string. Don't read too much into this, it's just an over simplification. We will get into why this is a bad hash function later.
    
For example, "CHAKSHU" is processed as:

$$C -> 3, H -> 8, A -> 1, K -> 11, S -> 19, H -> 8, U -> 21$$

The hash is computed as:

$$21 + 8 \cdot 27^1 + 19 \cdot 27^2 + 11 \cdot 27^3 + 1 \cdot 27^4 + 8 \cdot 27^5 + 3 \cdot 27^6$$

so:

$$H("Chakshu") = 1,277,813,765$$
    
Let's choose $q = 17$:

$$x = H("Chakshu") \mod 17 \equiv 13$$

## Step 2: Setting Up a Cyclic Group
A [cyclic group](cyclic_groups.md) is like “clock arithmetic” but with a twist. Choose a large prime number $p$ and a prime $q$ such that $q$ divides $p - 1$. Then choose a generator $g$ of a subgroup of the multiplicative group modulo $p$ (denoted $\mathbb{Z}_p^*$). The magic here is that raising $g$ to an exponent “wraps around” modulo $p$.

1. Pick large primes $p$ and $q$ (with $q$ dividing $p - 1$).  
2. Pick a generator $g$ for the subgroup of $\mathbb{Z}_p^*$ of order $q$.  
3. Compute the public value:

$$y = g^x \mod p$$

This $y$ is made public while $x$ (which encodes your name) remains secret. Why do this? Because in our group the operation of exponentiation is “one-way” (it’s easy to compute $y = g^x$ but hard to recover $x$ from $y$). This is known as the discrete logarithm problem.

In our [previous example](./cyclic_groups.md), we used:

- $p = 23$ (prime)
- $\mathbb{Z}_{23}^*$ The multiplicative group of integers modulo 23
- $g = 5$ (generator)

Let's map it to the concept of the "one-way" function:

**Chakshu's Secret Process**
- His secret $x = 6$ (ignore the $13$ that came earlier, i'll change the modulus later)
- Computes public value: $y = 5^6 \mod 23 = 8$
- She makes $8$ public, keeping $6$ secret

**Verifier's Secret Process**
- His secret $x = 9$
- Computes public value: $y = 5^9 \mod 23 = 11$
- He makes $11$ public, keeping $9$ secret

**The "one-way" property**
- Anyone can easily verify that $5^6 \mod 23 = 8$
- But given only $8$, finding that $6$ was the exponent is computationally difficult (**discrete logarithm problem**)

## The Schnorr Protocol
**Proving Knowledge Without Revealing It** - Now we want to prove, in zero knowledge, that you know 
$x$ such that: $$y = g^x \mod p$$ but without revealing $x$ (or your name “Chakshu”).

### Step-by-step protocol

1. **Commitment (Prover’s Step):**
- Pick a random number $r$ from $\{0, 1, \ldots, q-1\}$.
- Compute: $t = g^r \mod p$
- Send $t$ to the verifier.

2. **Challenge (Verifier’s Step):**
- The verifier picks a random challenge $c$ from a suitable set (often $\{0, 1, \ldots, q-1\}$ or a subset thereof) and sends $c$ to you.

3. **Response (Prover’s Step):**
- Compute the response: $s = (r + c \cdot x) \mod q$
- Send $s$ to the verifier.

4. **Verification (Verifier’s Check):**
- The verifier computes: $g^s \mod p$ and also computes: $ t \cdot y^c \mod p$
- The verifier accepts the proof if: $g^s \equiv t \cdot y^c \mod p$

### Example

Using our previous values:

- $p = 23$ (prime)
- $g = 5$ (generator)
- $x = 6$ (secret - hash of "Chakshu")
- $y = 5^6 \mod 23 = 8$ (pulic value)
- $s = (r + c \cdot x) \mod q$

Here's how Chakshu proves she knows the secret 6 without revealing it:

1. **Chakshu's Commitment:**

- She picks a random $r$, say $r = 4$
- Computes $t = 5^4 \mod 23 = 4$
- Sends $t = 4$ to the verifier

2. **Verifier's Challenge:**

- Verifier picks a random challenge, say $c = 3$
- Sends $c = 3$ to Chakshu

3. **Chakshu's Response:**

- Computes $s = (4 + 3 * 6) \mod 22 = 0$
- Sends $s = 0$ to verifier

4. **Verification:**

- Verifier checks if $5^{0} \mod 23$ equals $(4 * 8^3) \mod 23$
- Both equal $1$, so verification succeeds!

## The Zero-Knowledge Property

A zero-knowledge proof has three main properties:

1. **Completeness**: If you know $x$ (i.e., if your name really is “Chakshu” and you computed $x = H("Chakshu") $), then an honest verifier will always be convinced.  
2. **Soundness**: A cheating prover (one who does not know $x$) cannot convince the verifier except with very small probability.  
3. **Zero-Knowledge**: The verifier learns nothing about $x$ (or your name) beyond the fact that you know it. In fact, there exists a “simulator” that can produce a transcript $(t, c, s)$ that is statistically indistinguishable from one generated by an honest execution—even without knowing $x$.

## Bonus: The mathematical proof
Let’s break down the verification equation step by step:

- We have: $s = r + c \cdot x$
- Then, using properties of exponentiation: $g^s = g^{r + c \cdot x} = g^r \cdot g^{c \cdot x} \ (\text{mod} \ p)$
- Recall that $y = g^x,$ so: $g^{c \cdot x} = (g^x)^c = y^c$
- Thus, we obtain: $g^s = g^r \cdot y^c \equiv t \cdot y^c \ (\text{mod} \ p)$
- Since the verifier knows $g$, $t$, and $y$, checking that $g^s \equiv t \cdot y^c \ (\text{mod} \ p)$ ensures that you indeed used your secret $x$ in the computation of $s$.
