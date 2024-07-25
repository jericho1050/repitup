def get_db_uri(user, password, host, db):
    return f'postgres://{user}:{password}@{host}:5432/{db}'
    


if __name__ == "__main__":
    pass