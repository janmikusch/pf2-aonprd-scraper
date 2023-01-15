output_folder = "out/"
regex_valid_text = '[^A-Za-z0-9]+'

# Post Request config
url = 'https://2e.aonprd.com:9200/aon/_search?track_total_hits=true'
headers = {"Content-Type": "application/json; charset=UTF-16"}

post_data_get_feats = {"size": 4000, "query": {"bool": {"filter": [
    {"query_string": {"query": "category:feat "}}]}}}
