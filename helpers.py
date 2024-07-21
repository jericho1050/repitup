def validate_non_negative(value):
    if value < 0:
        raise ValueError("Value must be non-negative")
    
def get_db_uri(user, password, host, db):
    return f'postgres://{user}:{password}@{host}:5432/{db}'

if __name__ == "__main__":
    pass