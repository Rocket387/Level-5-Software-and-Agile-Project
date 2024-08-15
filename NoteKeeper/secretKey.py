import secrets

#### creates secret key - used by Flask and extensions to keep data safe ####

print(secrets.token_hex(16))
