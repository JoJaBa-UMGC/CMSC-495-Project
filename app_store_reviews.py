import requests


def get_app_id(app_name):

    key = "AIzaSyCH-_ALlgGE0iWbDNlO7MwMZOuyKYLOU8k"

    engine = "c5a5f09a33422445a"

    url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + engine + "&q=app store " + app_name

    response = requests.get(url)
    data = response.json()

    return data['items'][0]['link'].split('/')[-1]


def get_app_reviews(app_id):

    url = 'https://itunes.apple.com/us/rss/customerreviews/id=' + app_id + '/sortBy=mostRecent/json'

    response = requests.get(url)
    data = response.json()

    return ('Customer: ' + data['feed']['entry'][0]['author']['name']['label'] +
            ' says: ' + data['feed']['entry'][0]['content']['label'])


def main():

    app_name = "vain glory"

    app_id = get_app_id(app_name).split('id')[1]

    print(get_app_reviews(app_id))


if __name__ == '__main__':
    main()