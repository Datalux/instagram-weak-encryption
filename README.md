# instagram-weak-encryption
Get the length of the Instagram encrypted password

# Introduction
Instagram and Facebook encrypt the password submitted at login to sending this to the server, but the encryption has not padding so it's easy to exctract the **password length** from the ciphertext.

# Encryption phases
Instagram use AES256-GCM to encrypt the password in this with an 12 byte IV and a timestamp as AD. 

We can see the current Instagram encryption configurations at this [endpoint](https://www.instagram.com/data/shared_data/).
For example:
```json
{
                                                "key_id": "0",
                                                "public_key": "c5c457c3651d97dab8ed08fb2004555cfd2143bc5ce69ed4ac196fe9545faa48",
                                                "version": "10"
                                            }
```

This is a ciphertext example:
`#PWD_INSTAGRAM_BROWSER:10:1633796717:AY5QAElzjWV0j+OJ+qAnNXpQjZ6TN7A980Y2RMlrl63z80AkALvvb1IHYpzDXeX5w/Mf1jxTbF2PVJRh/Q99+J7FXkgmnE9qOhatEbKkdyoatN952Dee/PC8CiWLJTcoFDiCFovU9uwijaIDycIQ7w==`


We can se that it have a fixed structure that can be expressed like this: 

`<app_type>:<encryption_version>:<timestamp>:<base64_ciphertext>`

In addiction we know the ciphertext structures:

`key_id|encrypted_key|tag|aes_output`


This is an encryption preudo-code example.
```
int[32] key = create_random_key();
int[12] iv = create_random_iv();
int[16] tag;
byte[] ad = get_timestamp();
string plaintext = password;

ciphertext = encrypt_aes_256_gcm(
  iv,
  key,
  tag,
  plaintext,
  ad 
);
```

# The problem

By collecting two or more ciphertexts we can see that the ciphertext length depends on the plaintext length so there is not any padding applied to the plaintext.
For example:


Password length 8: `#PWD_INSTAGRAM_BROWSER:10:1633796644:AY5QAOHhnlwGkvikhrThjD0/XSZAVlJ+dFBGNAtG4JhnP5c42slFXO0H0xpE3W2JSlcdjDEDI1O/CioKL5zXhXCfkRpL+ItOqUB0jhpl/D3EcTEI9iTq0XSpmGDvxb7fwaCvNFv2xFj4lvsv`

Password length 12: `#PWD_INSTAGRAM_BROWSER:10:1633796717:AY5QAElzjWV0j+OJ+qAnNXpQjZ6TN7A980Y2RMlrl63z80AkALvvb1IHYpzDXeX5w/Mf1jxTbF2PVJRh/Q99+J7FXkgmnE9qOhatEbKkdyoatN952Dee/PC8CiWLJTcoFDiCFovU9uwijaIDycIQ7w==`

Therefore we need to setup a way to extract the password length from the ciphertext

# Calculate the length
It's very easy to calculate the password length simply by count the ciphertext length and see the base64 padding.
We need to calculate:
1. The base64 blocks number
2. How many '=' base64 pad there are
3. The difference between the ciphertext length and a one char password ciphertext length (136 chars)

I combined these points to create a simple Python script to calculate the exact length of a password:
```Python
c = enc.split(':')[3] if ':' in enc else enc
cl = len(c)
pad = (int)((cl / 4) - 36)
pad1 = 1 if c[-1] == '=' else 0
pad2 = 1 if c[-2] == '=' else 0
pl = (len(c) - 136 - pad - pad1 - pad2)
print(pl)
```

# Impact            
To exploit this you need to read the comminication between the client and server.
I have imaginad three possibile scenario:
1. An attacker have physical access to the victim machine
2. MITM attack
3. Bad VPN that can read the traffic
