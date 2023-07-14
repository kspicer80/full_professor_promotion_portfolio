import json
from collections import Counter

main_posts_file_path = r"database\data_prepped_for_insertion\main_post_author_mentions_unexploded.json"

with open(main_posts_file_path, "r") as f:
    main_results_data = json.load(f)

main_post_counter = 0

for dictionary in main_results_data:
    if len(dictionary.get('alias_id', '')) > 3:
        main_post_counter += 1
print(f"The total number of main posts is equal to: {len(main_results_data)}.")
print(f"The number of main posts that have more than 3 authors mentioned: {main_post_counter}.")

reply_posts_file_path = r"database\data_prepped_for_insertion\reply_post_author_mentions_unexploded.json"

with open(reply_posts_file_path, "r") as f:
    reply_results_data = json.load(f)

reply_post_counter = 0

for dictionary in reply_results_data:
    if len(dictionary.get('alias_id', '')) > 3:
        reply_post_counter += 1
print(f"The total number of reply posts is equal to: {len(reply_results_data)}.")
print(f"The number of reply posts that have more than 3 authors mentioned: {reply_post_counter}.")
print("===============================")
print(f"The percentage of main posts mentioning more than three authors is: {round(main_post_counter/len(main_results_data)*100, 2)}%")
print(f"The percentage of reply posts mentioning more than three authors is: {round(reply_post_counter/len(reply_results_data)*100, 2)}%")