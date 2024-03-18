import backoff
import requests
import re
from bs4 import BeautifulSoup as bs

class ForbiddenError(Exception):
    pass

@backoff.on_exception(backoff.expo, ForbiddenError, max_tries=20)

def get_user_profile(username, contest_name):
    url = f"https://www.codechef.com/users/{username}"
    r = requests.get(url)

    if r.status_code != 200:
        print(f"Failed to retrieve the user's profile. Status Code: {r.status_code}")
        return

    soup = bs(r.content, "html.parser")

    # Get the number of problems solved
    contest_section = soup.find("section", {"class": "rating-data-section problems-solved"})
    if contest_section:
        contest_names = [h5.get_text(strip=True) for h5 in reversed(contest_section.find_all('h5'))]
        matching_contests = [name for name in contest_names if contest_name.lower() in name.lower()]

        if matching_contests:
            matching_contest_name = matching_contests[0]
            matching_h5 = next((h5 for h5 in contest_section.find_all('h5') if matching_contest_name.lower() in h5.get_text(strip=True).lower()), None)

            if matching_h5:
                problems_div = matching_h5.find_parents('div', class_='content')[0]

                if problems_div:
                    span_tag = problems_div.find('p').find('span')

                    if span_tag:
                        a_tags = span_tag.find_all('a')
                        num_a_tags = len(a_tags)
                        print(f"Number of problems solved for {contest_name}: {num_a_tags}")
        else:
            print(f"Contest {contest_name} not found.")
    else:
        print("Contest section not found on the user's profile page.")

    # Get global rank
    rating_box_all = soup.find("div", {"id": "rating-box-all"})
    if rating_box_all:
        global_rank_container = rating_box_all.find('div', {'id': 'global-rank-all'})

        if global_rank_container:
            global_rank_element = global_rank_container.find('strong', {'class': 'global-rank'})

            if global_rank_element:
                global_rank = global_rank_element.get_text(strip=True)
                print(f"Global Rank for the latest contest: {global_rank}")
            else:
                print("No global rank information found.")
        else:
            print("Global Rank information not available.")
    else:
        print("Rating box information not found on the user's profile page.")

    # Get user rating and division
    rating_container = soup.find("div", {"class": "rating-container"})
    if rating_container:
        rating_element = rating_container.find('a', {'class': 'rating'})

        if rating_element:
            rating_text = rating_element.get_text(strip=True)

            # Extract rating and division from the rating string
            rating_parts = rating_text.split()
            if len(rating_parts) == 2:
                rating = rating_parts[0]
                division_part = rating_parts[1]

                # Check if the division is in the expected format
                if '(' in division_part and ')' in division_part:
                    division = division_part.strip('()')

                    # Extract division from the contest name in rating-box-all div
                    contest_name_division = soup.find("div", {"id": "rating-box-all"}).find("div", {"class": "contest-name"})
                    if contest_name_division:
                        contest_division = contest_name_division.find("a").text.strip().replace(contest_name, '').strip()
                        print(f"Overall Rating: {rating}")
                        print(f"Rating received for the latest contest: {division}")
                        print(f"Division for the latest contest: {contest_division}")
                    else:
                        print("Division information not found.")
                else:
                    print("Invalid division format.")
            else:
                print("Invalid rating format.")
        else:
            print("No rating information found.")
    else:
        print("Rating container not found on the user's profile page.")

