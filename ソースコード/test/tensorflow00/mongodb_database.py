def load_your_dic(collection_name):
    db = get_db(YOUR_DB)
    cursor = db[collection_name].find()
    df = pd.DataFrame.from_dict(list(cursor)).astype(object)
    return df